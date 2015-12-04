#!/usr/bin/python

class PyLuaTblParser(object):
	def __init__(self, luaStr="", curPos=0, totLen=0, _debug=False):
		self.luaStr = luaStr
		self.curPos = curPos
		self.totLen = totLen
		self._debug = _debug

	def setDebugMode(self, _debug):
		self._debug = _debug


	def underDebugMode(self):
		return self._debug

	def eliminateAnnotation(self, s):
		i, slen, t = 0, len(s), ''
		while i < slen:
			if s[i] == '"' or s[i] == '\'':
				f = s[i]
				t += s[i]
				i += 1
				while i < slen:
					t += s[i]
					if s[i] == f and i > 0 and s[i-1] != '\\':
						break
					i += 1
			elif s[i] == '-' and i + 1 < slen and s[i+1] == '-':
				if i + 2 < slen and s[i+2] == '[':
					# --[[annotation]]
					if i + 3 < slen and s[i+3] == '[':
						i += 4
						while i < slen:
							if s[i] == ']' and i + 1 < slen and s[i+1] == ']':
								i += 1
								break
							i += 1
					# --[====[annotation]====]
					elif i + 3 < slen and s[i+3] == '=':
						lcnt, rcnt = 0, 0
						i += 3
						while i < slen and s[i] == '=':
							lcnt += 1
							i += 1
						if i < slen and s[i] == '[':
							i += 1
							while i < slen:
								if s[i] == ']':
									j = i + 1
									rcnt = 0
									while j < slen and s[j] == '=':
										rcnt += 1
										j += 1

									i = j
									if lcnt == rcnt and j < slen and s[j] == ']':
										# match the pattern --[===[]===]
										break
								else:
									i += 1
						# this part does not match the pattern --[==[, which indicates the whole line is annotation
						else:
							break
					# this part does not even match the pattern --[=, which indicates the whole line is annotation
					else:
						break
				# this part does not match either --[[ or --[==[, so the whole line is annotation
				else:
					break
			else:
				t += s[i]

			i += 1
		return t


	def next(self):
		if self.curPos < self.totLen:
			ch = self.luaStr[self.curPos]
			self.curPos += 1
			return ch
		else:
			self.curPos += 1
			return None


	def putback(self):
		if self.curPos > 0:
			self.curPos -= 1
		else:
			print 'Index out of bound for curPos = %d' % self.curPos


	def skip(self):
		ch = self.next()
		while ch is not None and ch == ' ':
			ch = self.next()
		self.putback()


	@staticmethod
	def isDigit(ch):
		if '0' <= ch and ch <= '9':
			return True
		return False


	@staticmethod
	def isAlphabet(ch):
		if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
			return True
		return False


	@staticmethod
	def isAlphanum(ch):
		return PyLuaTblParser.isDigit(ch) or PyLuaTblParser.isAlphabet(ch)

	@staticmethod
	def validate(ch):
		flag = ch is None or ch == ',' or ch == ';' or ch == '}'
		if not flag:
			print 'Current character is $%s$.' % ch
			raise ValueError('Failed to found seperator comma of semicolon !!!')

	def getStr(self, quotationMark):
		s = ''
		self.skip()
		ch1 = self.next()
		if ch1 == quotationMark:
			return s

		ch2 = self.next()
		while not (ch1 is not None and ch2 is not None and ch1 != '\\' and ch2 == quotationMark):
			s += ch1
			ch1 = ch2
			ch2 = self.next()

		s += ch1
		if ch2 != quotationMark:
			raise ValueError('Quotation mark does not match !!!')
		# print 'getStr s =', s
		return s

	def getNumber(self):
		s = ''
		self.skip()
		ch = self.next()
		while PyLuaTblParser.isDigit(ch) or ch == '.' or ch == 'e' or ch == 'E' or ch == '+' or ch == '-':
			s += ch
			ch = self.next()
		self.putback()
		f = float(s)
		try:
			i = int(s)
		except ValueError:
			return f
		else:
			return i


	def checkSpecialStr(self, s):
		if s == 'nil':
			return None, True
		elif s == 'false':
			return False, True
		elif s == 'true':
			return True, True
		else:
			return s, False

	def getVar(self):
		self.skip()
		s = ''
		ch = self.next()
		while ch is not None and PyLuaTblParser.isAlphanum(ch):
			s += ch
			ch = self.next()
		self.putback()
		return s

	def getValue(self, key):
		val = None
		self.skip()
		ch = self.next()
		if self.underDebugMode():
			print 'getValue key = %s, ch = %s.' % (key, ch)
		if ch == '"' or ch == '\'':
			val = self.getStr(ch)
		elif PyLuaTblParser.isDigit(ch) or ch == '-' or ch == '+':
			val = self.getNumber()
		elif ch == '{':
			val = self.getItem()
		elif PyLuaTblParser.isAlphanum(ch):
			self.putback()
			val = self.getVar()
			val, ok = self.checkSpecialStr(val)
			if not ok:
				msg = 'Illegal value $%s$ for key $%s$' % (str(val), str(key))
				raise ValueError(msg)

		return val


	def getItem(self):
		ans = []
		while True:
			self.skip()
			ch = self.next()

			if ch is None:
				break

			if ch == '}':
				if len(ans) == 1 and ans[0] != {}:
					ans = ans[0]
				return ans

			if ch == '{':
				item = self.getItem()
				self.skip()
				ch = self.next()
				if ch != '}':
					PyLuaTblParser.validate(ch)
				else:
					self.putback()
				ans.append(item)
				if self.underDebugMode():
					print '{-->ans =', ans
			elif ch == '"' or ch == '\'':
				s = self.getStr(ch)
				self.skip()
				ch = self.next()
				if ch != '}':
					PyLuaTblParser.validate(ch)
				else:
					self.putback()
				ans.append(s)
				if self.underDebugMode():
					print '"-->ans =', ans
			elif ch == '[':
				self.skip()
				ch = self.next()
				key, val = None, None
				if ch == '"' or ch == '\'':
					key = self.getStr(ch)
				else:
					self.putback()
					key = self.getNumber()

				self.skip()
				if self.next() != ']':
					raise ValueError('Square brackets does not match !!!')
				self.skip()
				if self.next() != '=':
					raise ValueError('Dict should in the pattern KEY=VAL !!!')
				self.skip()
				val = self.getValue(key)
				if self.underDebugMode():
					print 'key = %s, val = %s' % (str(key), str(val))
				self.skip()
				ch = self.next()
				if ch != '}':
					PyLuaTblParser.validate(ch)
				else:
					self.putback()
				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')
				ans.append({key: val})
				if self.underDebugMode():
					print '[-->ans =', ans
			elif PyLuaTblParser.isDigit(ch) or ch == '+' or ch == '-':
				if ch == '-' and self.next() == '-':
					ch = self.next()
					while ch is not None and ch != '\n':
						ch = self.next()
					continue
					# self.putback()
				else:
					self.putback()
					num = self.getNumber()
					self.skip()
					ch = self.next()
					if ch != '}':
						PyLuaTblParser.validate(ch)
					else:
						self.putback()
					ans.append(num)
				if self.underDebugMode():
					print 'N-->ans =', ans
			elif PyLuaTblParser.isAlphabet(ch) or ch == '_':
				key = ''
				while PyLuaTblParser.isAlphanum(ch):
					key += ch
					ch = self.next()
				self.putback()
				self.skip()

				key, spFlag = self.checkSpecialStr(key)
				if spFlag:
					self.skip()
					ch = self.next()
					if ch != '}':
						PyLuaTblParser.validate(ch)
					else:
						self.putback()
					continue

				if self.next() != '=':
					raise ValueError('Dict should in the pattern KEY=VAL !!!')
				val = self.getValue(key)
				if self.underDebugMode():
					print 'key = %s, val = %s' % (str(key), str(val))
				self.skip()
				ch = self.next()
				if ch != '}':
					if self.underDebugMode():
						print 'Already parsed $%s$.' % self.luaStr[:self.curPos]
					PyLuaTblParser.validate(ch)
				else:
					self.putback()

				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')
				ans.append({key: val})
				if self.underDebugMode():
					print 'K-->ans =', ans
			else:
				msg = 'Invalid lua table string: $%s$, current character is $%s$.' % (self.luaStr[0:self.curPos], ch)
				raise ValueError(msg)
		
		if len(ans) == 1 and ans[0] != {}:
			ans = ans[0]

		return ans		


	def load(self, s):
		s = self.eliminateAnnotation(s)
		if self.underDebugMode():
			print 'After preprocessing, SRC =', s
		self.luaStr = s
		self.curPos = 0
		self.totLen = len(s)
		print 'luaStr =', self.luaStr
		print self.getItem()

if __name__ == '__main__':
	s = '{"hello",key="value", {"in", 3, 4, [1.23]=56, nil, {mixed="inin", nice={0,9,8}}}, 1, 2} --hello'
	s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {{}}, [1]=678, ["yada,had"]="nice", hello="worl,[]\\\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	parser = PyLuaTblParser()
	# parser.setDebugMode(True)
	parser.load(s)