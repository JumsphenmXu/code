#!/usr/bin/python

class PyLuaTblParser(object):
	def __init__(self, luaStr="", curPos=0, totLen=0, luaLst=[], _debug=False):
		self.luaStr = luaStr
		self.curPos = curPos
		self.totLen = totLen
		self.luaLst = luaLst
		self._debug = _debug

	def setDebugMode(self, _debug):
		self._debug = _debug

	def underDebugMode(self):
		return self._debug

	def printLeftToken(self, msg):
		if self.underDebugMode() and self.curPos < self.totLen:
			print msg, self.luaStr[:self.curPos]

	def prev(self):
		if self.curPos > 0:
			i = 0
			while self.curPos - i > self.totLen:
				i += 1
			while self.curPos > i and self.luaStr[self.curPos-i-1] == ' ':
				i += 1

			return self.luaStr[self.curPos-i-1]
		return None


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
		if ch is not None:
			self.putback()

	def skipAnnotation(self):
		f = self.curPos - 2
		ch = self.next()
		if ch == '"' or ch == '\'':
			self.getStr(ch, False)
		
		while ch is not None and ch != '\n':
			ch = self.next()
		if ch is not None:
			self.putback()
		t = min(self.curPos, self.totLen)
		s = self.luaStr[:f] + self.luaStr[t:-1]
		self.luaStr = s
		self.totLen = len(self.luaStr)
		self.curPos = f

	def preprocessAnnotation(self, s):
		i, slen = 0, len(s)
		t = ''
		while i < slen:
			if s[i] == '"' or s[i] == '\'':
				f = s[i]
				t += s[i]
				i += 1
				while i < slen and (s[i] != f or s[i-1] != '\\'):
					t += s[i]
					i += 1
				if i < slen:
					t += s[i]
			elif s[i] == '-':
				if i + 1 < slen and s[i+1] == '-':
					while i < slen and s[i] != '\n':
						i += 1
				else:
					t += s[i]
			else:
				t += s[i]
			i += 1
		return t

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


	def validate2(self, flag=True):
		self.skip()
		ch = self.next()
		if ch is None or ch == ',' or ch == ';':
			return
		if ch == '}' or not flag:
			self.putback()
			return

		raise ValueError('Suppose to be an seperator like $,;}$')


	def getStr(self, quotationMark, flag=True):
		s = ''
		self.skip()
		ch1 = self.next()
		if ch1 != quotationMark:
			ch2 = self.next()
			while not (ch1 is not None and ch2 is not None and ch1 != '\\' and ch2 == quotationMark):
				s += ch1
				ch1 = ch2
				ch2 = self.next()

			s += ch1
			if ch2 != quotationMark:
				raise ValueError('Quotation mark does not match !!!')
		self.validate2(flag)

		return s

	def getNumber(self, flag=True):
		s = ''
		self.skip()
		ch = self.next()
		while PyLuaTblParser.isDigit(ch) or ch == '.' or ch == 'e' or ch == 'E' or ch == '+' or ch == '-':
			s += ch
			ch = self.next()
		self.putback()
		self.validate2(flag)

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

	def getVar(self, flag=True):
		self.skip()
		s = ''
		ch = self.next()
		while ch is not None and (PyLuaTblParser.isAlphanum(ch) or ch == '_'):
			s += ch
			ch = self.next()
		self.putback()
		self.validate2(flag)

		return s

	def getValue(self, key, flag=True):
		val = None
		self.skip()
		ch = self.next()
		if self.underDebugMode():
			print 'getValue key = %s, ch = %s.' % (key, ch)

		if ch == '"' or ch == '\'':
			val = self.getStr(ch, flag)
		elif PyLuaTblParser.isDigit(ch) or ch == '-' or ch == '+':
			self.putback()
			val = self.getNumber(flag)
		elif ch == '{':
			val = self.getItem(True)
			if self.prev() != '}':
				raise ValueError('Brackets does not match !!!')
		elif PyLuaTblParser.isAlphabet(ch):
			self.putback()
			val = self.getVar(flag)
			val, ok = self.checkSpecialStr(val)
			if not ok:
				msg = 'Illegal value $%s$ for key $%s$' % (str(val), str(key))
				raise ValueError(msg)

		return val

	def getItem(self, bracketFlag=False):
		ans = []
		while True:
			self.skip()
			ch = self.next()

			if ch is None:
				if bracketFlag:
					raise ValueError('Illegal expression !!!')
				else:
					break

			if ch == '}':
				if not bracketFlag:
					raise ValueError('Brackets does not match !!!')
				if len(ans) == 1 and ans[0] != []:
					ans = ans[0]

				if self.underDebugMode():
					print '#1 Finally ans =', ans
					self.printLeftToken('#1 Already parsed:')
				return ans

			if ch == '{':
				self.printLeftToken('#2 Already parsed:')
				item = self.getItem(True)
				if self.prev() != '}':
					raise ValueError('Brackets does not match !!!')
				self.skip()
				ch = self.next()
				if ch is None and not bracketFlag:
					ans.append(item)
					if len(ans) == 1 and ans[0] != []:
						ans = ans[0]
					return ans
				else:
					self.putback()
				self.validate2(True)
				ans.append(item)
			elif ch == '"' or ch == '\'':
				s = self.getStr(ch, True)
				ans.append(s)
			elif ch == '[':
				self.skip()
				ch = self.next()
				key, val = None, None
				if ch == '"' or ch == '\'':
					key = self.getStr(ch, False)
				else:
					self.putback()
					key = self.getNumber(False)

				self.skip()
				if self.next() != ']':
					raise ValueError('Square brackets does not match !!!')
				self.skip()
				if self.next() != '=':
					raise ValueError('Dict should in the pattern KEY=VAL !!!')
				self.skip()
				val = self.getValue(key, True)
				if self.underDebugMode():
					print '[\'key\'] = %s, val = %s' % (str(key), str(val))

				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')

				if val is not None or type(key) is int:
					ans.append({key: val})
			elif PyLuaTblParser.isDigit(ch) or ch == '+' or ch == '-':
				self.putback()
				num = self.getNumber(True)
				ans.append(num)
			elif PyLuaTblParser.isAlphabet(ch) or ch == '_':
				self.putback()
				key = self.getVar(False)
				key, spFlag = self.checkSpecialStr(key)
				if spFlag:
					if type(key) is bool:
						ans.append(key)
					continue

				self.skip()
				ch = self.next()
				if ch != '=':
					if ch != ',' or ch != ',':
						self.putback()
					continue
					# raise ValueError('Dict should in the pattern KEY=VAL !!!')
				self.skip()
				val = self.getValue(key, True)
				if self.underDebugMode():
					print 'key = %s, val = %s' % (str(key), str(val))
				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')
				if val is not None:
					ans.append({key: val})
			else:
				msg = 'Invalid lua table string: $%s$, current character is $%s$.' % (self.luaStr[0:self.curPos], ch)
				raise ValueError(msg)
		
		if len(ans) == 1 and ans[0] != []:
			ans = ans[0]
		return ans


	def load(self, s):
		s = self.preprocessAnnotation(s)
		if self.underDebugMode():
			print 'After preprocessing, SRC =', s
		self.luaStr = s
		self.curPos = 0
		self.totLen = len(s)
		self.luaLst = self.getItem()
		if type(self.luaLst) is not list:
			self.luaLst = [self.luaLst]
		if self.underDebugMode():
			print 'self.luaLst =', self.luaLst


	def dumpList2String(self, data):
		if self.underDebugMode():
			print 'dumpList2String data =', data
		assert type(data) is list

		datalen = len(data)
		s = ""
		if datalen == 1 and type(data[0]) is list:
			s += "{" +  self.dumpList2String(data[0]) + "}"
			return s

		s += "{"
		for i in xrange(datalen):
			if type(data[i]) is dict:
				s += self.dumpDict2String(data[i]) + ","
			elif type(data[i]) is list:
				s += self.dumpList2String(data[i]) + ","
			else:
				try:
					f = float(data[i])
				except ValueError:
					if data[i] == "nil" or data[i] == "false" or data[i] == "true":
						s += str(data[i]) + ","
					else:
						s += "'" + str(data[i]) + "',"
				else:
					s += str(data[i]) + ","

		if len(s) > 0 and s[-1] == ",":
			s = s[:-1]
		s += "}"
		return s

	def dumpDict2String(self, data):
		if self.underDebugMode():
			print 'dumpDict2String data =', data

		assert type(data) is dict
		keys = data.keys()
		s = ""
		if (len(keys)) > 1:
			s += "{";

		for key in keys:
			value = data[key]

			try:
				f = float(key)
			except ValueError:
				s += "['" + str(key) + "']="
			else:
				s += "[" + str(key) + "]="

			if type(value) is dict:
				s += self.dumpDict2String(value) + ","
			elif type(value) is list:
				s += self.dumpList2String(value) + ","
			else:
				try:
					f = float(value)
				except ValueError:
					if value == "nil" or value == "false" or value == "true":
						s += str(value) + ","
					else:
						s += "'" + str(value) + "',"
				else:
					s += str(value) + ","

		s = s[:-1]
		if len(keys) > 1:
			s += "}"
		return s

	def dump(self):
		return self.dumpList2String(self.luaLst)

	def loadLuaTable(self, f):
		fp = open(f, "rb")
		line = fp.read()
		fp.close()
		self.load(line)

	def dumpLuaTable(self, f):
		self.luaStr = self.dump()
		fp = open(f, "wb")
		fp.write(self.luaStr)
		fp.close()

	def loadFromList(self, lst):
		assert type(lst) is list
		res = []
		for i in xrange(len(lst)):
			item = None
			if type(lst[i]) is dict:
				item = self.loadFromDict(lst[i])
			elif type(lst[i]) is list:
				item = self.loadFromList(lst[i])
			else:
				if type(lst[i]) is bool:
					item = str(lst[i]).lower()
				elif type(lst[i]) is str and lst[i] == "nil":
					item = None
				else:
					item = lst[i]

			if item is not None or lst[i] == "nil":
				if type(item) is list and len(item) == 1:
					item = item[0]
				res.append(item)

			if self.underDebugMode():
					print '#1# loadFromList: lst[i]=', lst[i]
					print '#1# loadFromList: res=', res

		if self.underDebugMode():
			print 'loadFromList return:', res
		return res


	def loadFromDict(self, d):
		assert type(d) is dict
		listTmp = []
		index = 1
		keys = d.keys()

		for key in keys:
			item = None
			if type(d[key]) is list:
				item = self.loadFromList(d[key])
			elif type(d[key]) is dict:
				item = self.loadFromDict(d[key])
			else:
				if d[key] == "nil":
					continue
				elif type(d[key]) is bool:
					item = str(item).lower()
				else:
					item = d[key]

			if type(item) is list and len(item) == 1 and type(item[0]) is not list:
				item = item[0]

			if type(key) is int and key == index:
				listTmp.append(item)
				index += 1
			else:
				listTmp.append({key: item})
		return listTmp


	def loadDict(self, d):
		self.luaLst = self.loadFromDict(d)
		if self.underDebugMode():
			print 'loadDict(self, d) -->', self.luaLst


	def xtransfer(self, dct):
		assert type(dct) is dict
		flag = True
		keys = dct.keys()
		keys.sort()
		maxkey = -1

		for i in xrange(len(keys)):
			if type(keys[i]) is not int or dct[keys[i]] == {}:
				flag = False
				break
			if maxkey < keys[i]:
				maxkey = keys[i]
		
		res = []
		if flag and maxkey == len(keys):
			for i in xrange(len(keys)):
				res.append(dct[keys[i]])
			
			if len(res) == 1:
				return res[0]
			else:
				return res

		return dct


	def dumpInnerDict2PythonDict(self, data):
		assert type(data) is dict
		res = {}

		for k, v in data.items():
			if type(v) is list:
				res[k] = self.dumpInnerList2PythonDict(v)
			elif type(v) is dict:
				res[k] = self.xtransfer(self.dumpInnerDict2PythonDict(v))
			else:
				if type(v) is str:
					if v == 'false':
						res[k] = False
					elif v == 'true':
						res[k] = True
					elif v == 'nil':
						continue
					elif len(v) > 1 and v[0] == v[-1] and v[0] == '\'' or v[0] == '"':
						res[k] = v[1:-1]
					else:
						res[k] = v
				else:
					res[k] = v
			if type(res[k]) is str and res[k] == 'nil':
				res.pop(k)

		return res


	def dumpInnerList2PythonDict(self, data):
		assert type(data) is list
		dlen = len(data)

		if dlen == 0:
			return {}

		res = {}
		for i in xrange(dlen):
			item = data[i]
			if type(item) is dict:
				for k, v in item.items():
					kd = self.dumpInnerDict2PythonDict({k:v})
					if k in kd.keys():
						if type(kd[k]) is dict:
							res[k] = self.xtransfer(kd[k])
						else:
							res[k] = kd[k]
			elif type(item) is list:
				tmp = self.dumpInnerList2PythonDict(item)
				if type(tmp) is dict:
					tmp = self.xtransfer(tmp)
				res[i+1] = tmp
				if type(res[i+1]) is str and res[i+1] == 'nil':
					res.pop(i+1)
			else:
				if type(item) is str:
					if item == 'false':
						res[i+1] = False
					elif item == 'true':
						res[i+1] = True
					elif item == 'nil':
						res[i+1] = None
					elif len(item) > 1 and item[0] == item[-1] and item[0] == '\'' or item[0] == '"':
						res[i+1] = item[1:-1]
					else:
						res[i+1] = item
				else:
					res[i+1] = item
				if type(res[i+1]) is str and res[i+1] == 'nil':
					res.pop(i+1)

		return res

	def dumpDict(self):
		return self.dumpInnerList2PythonDict(self.luaLst)


if __name__ == '__main__':
	s = '{"hello",key="value", {"in", 3, 4, [1.23]=56, nil, {mixed="inin", nice={0,9,8}}}, 1, 2} --hello'
	s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {{}}, [1]=678, ["yada,had"]="nice", hello="worl,[]\\\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	s = '{{{}},{1, 2, 3,}, hello="world"}  -- i am xuxinhui '
	# s = '"hello"}'
	# s = "{['array']={65,23,5,{1,2,3},{{}},[1]=78,['yada,had']='nice',['hello']='worl,[]\"ddefj'},['dict']={['mixed']={43,54.33,9,['string']={'value]','hello',{11,22}}},['array']={3,6,4},['string']='value'}}"
	# s = '{1, 2}'
	s = '{{hello="world"}, hel=1}'
	parser = PyLuaTblParser()
	parser.setDebugMode(True)

	parser.load(s)
	print 'luaLst:', parser.luaLst
	s = parser.dump()
	d = parser.dumpDict()
	print 'd =', d
	print 's =', s
	parser.load(s)
	print 'luaLst:', parser.luaLst
	print '--', parser.dump()
	print 'd =', parser.dumpDict()

	parser.loadDict(d)
	print '-----loadDict-----'
	print 'luaLst:', parser.luaLst
	s = parser.dump()
	d = parser.dumpDict()
	print 'd =', d
	print 's =', s