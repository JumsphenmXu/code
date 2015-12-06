#!/usr/bin/python

class PyLuaTblParser(object):
	def __init__(self, luaStr="", curPos=0, totLen=0, luaLst=[]):
		self.luaStr = luaStr
		self.curPos = curPos
		self.totLen = totLen
		self.luaLst = luaLst

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

	def preprocessAnnotation(self, s):
		i, slen = 0, len(s)
		t = ''
		while i < slen:
			if s[i] == '"' or s[i] == '\'':
				f = s[i]
				t += s[i]
				i += 1
				while i < slen and (s[i] != f or s[i-1] == '\\'):
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


	def isDigit(self, ch):
		if '0' <= ch and ch <= '9':
			return True
		return False

	def isAlphabet(self, ch):
		if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
			return True
		return False

	def isAlphanum(self, ch):
		return self.isDigit(ch) or self.isAlphabet(ch)

	def getStr(self, quotationMark):
		s = ''
		prev = None
		cur = self.next()
		while cur is not None:
			if cur == quotationMark and prev != '\\':
				break
			s += cur
			prev = cur
			cur = self.next()

		if cur != quotationMark:
			raise ValueError('Quotation mark does not match !!!')

		return s

	def getNumber(self, flag=True):
		s = ''
		cur = self.next()

		while self.isDigit(cur) or cur == '.' or cur == 'e' or cur == 'E' or cur == '+' or cur == '-':
			s += cur
			cur = self.next()

		self.putback()
		try:
			i = int(s)
		except ValueError:
			return float(s)
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
			flag = True
			for i in xrange(len(s)):
				if s[i] != '_' and not self.isAlphanum(s[i]):
					flag = False
					break
			return s, flag

	def getVar(self, flag=True):
		s = ''
		ch = self.next()
		while ch is not None and (self.isAlphanum(ch) or ch == '_'):
			s += ch
			ch = self.next()

		self.putback()
		return s


	def getValue(self):
		val = None
		self.skip()
		ch = self.next()

		if ch == '"' or ch == '\'':
			val = self.getStr(ch)
		elif self.isDigit(ch) or ch == '-' or ch == '+':
			self.putback()
			val = self.getNumber()
		elif ch == '{':
			val = self.getItem(True)
		elif self.isAlphabet(ch) or ch == '_':
			self.putback()
			val = self.getVar()
			val, ok = self.checkSpecialStr(val)
			if not ok:
				msg = 'Value #%s# is illegal !!!' % str(val)
				raise ValueError(msg)

		return val


	def trailing(self, selector):
		if selector == 0:
			return

		self.skip()
		ch = self.next()
		if selector == 1:
			if ch is None or ch == ',' or ch == ';':
				return
			elif ch == '}':
				self.putback()
			else:
				raise ValueError('Illegal lua string !!!')
		elif selector == 2:
			if ch == ',' or ch == ';':
				return
			elif ch == '}':
				self.putback()
			else:
				raise ValueError('Illegal lua string !!!')

	def getItem(self, bracketFlag=False):
		ans = []
		while True:
			self.skip()
			ch = self.next()
			selector = 0

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
				return ans

			if ch == '{':
				item = self.getItem(True)
				self.skip()
				ch = self.next()
				if ch is None and not bracketFlag:
					ans.append(item)
					if len(ans) == 1 and ans[0] != []:
						ans = ans[0]
					return ans
				else:
					self.putback()
				ans.append(item)
				selector = 1
			elif ch == '"' or ch == '\'':
				s = self.getStr(ch)
				ans.append(s)
				selector = 2
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
					raise ValueError('Illegal expression #equal symbol(=) missed# !!!')

				self.skip()
				val = self.getValue()

				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')

				if val is not None or type(key) is int:
					ans.append({key: val})
				selector = 2
			elif self.isDigit(ch) or ch == '+' or ch == '-':
				self.putback()
				num = self.getNumber()
				ans.append(num)
				selector = 2
			elif self.isAlphabet(ch) or ch == '_':
				self.putback()
				key = self.getVar()
				key, spFlag = self.checkSpecialStr(key)

				self.skip()
				ch = self.next()
				if (ch == ',' or ch == ';' or ch == '}') and spFlag:
					if ch == '}':
						self.putback()
					if type(key) is not str:
						ans.append(key)
					continue
				elif ch != '=':
					raise ValueError('Illegal expression #equal symbol(=) missed# !!!')

				val = self.getValue()
				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')
				if val is not None:
					ans.append({key: val})
				selector = 2
			else:
				raise ValueError('Invalid lua table string')
	
			self.trailing(selector)
		
		if len(ans) == 1 and ans[0] != []:
			ans = ans[0]
		return ans


	def load(self, s):
		s = self.preprocessAnnotation(s)
		print 'After preprocessing, SRC =', s
		self.luaStr = s
		self.curPos = 0
		self.totLen = len(s)
		self.luaLst = self.getItem()
		if type(self.luaLst) is not list:
			self.luaLst = [self.luaLst]


	def dumpList2String(self, data):
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
			elif data[i] is None:
				s += "nil,"
			elif type(data[i]) is bool:
				s += str(data[i]).lower() + ","
			else:
				try:
					f = float(data[i])
				except ValueError:
					s += "'" + str(data[i]) + "',"
				else:
					s += str(data[i]) + ","

		if len(s) > 0 and s[-1] == ",":
			s = s[:-1]
		s += "}"
		return s

	def dumpDict2String(self, data):
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
			elif type(value) is bool:
				s += str(value).lower()
			else:
				try:
					f = float(value)
				except ValueError:
					s += "'" + str(value) + "',"
				else:
					s += str(value) + ","

		s = s[:-1]
		if len(keys) > 1:
			s += "}"
		return s

	def dump(self):
		self.luaStr = self.dumpList2String(self.luaLst)
		return self.luaStr

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
				item = lst[i]

			if item is not None:
				if type(item) is list and len(item) == 1:
					item = item[0]
			res.append(item)
		return res


	def loadFromDict(self, d):
		assert type(d) is dict
		lst = []
		index = 1
		for key in d.keys():
			item = None
			if type(d[key]) is list:
				item = self.loadFromList(d[key])
			elif type(d[key]) is dict:
				item = self.loadFromDict(d[key])
			elif d[key] is not None:
				item = d[key]

			if type(item) is list and len(item) == 1 and type(item[0]) is not list:
				item = item[0]

			if type(key) is int and key == index:
				lst.append(item)
				index += 1
			else:
				lst.append({key: item})
		return lst


	def loadDict(self, d):
		self.luaLst = self.loadFromDict(d)

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


	def dumpDct2Dct(self, data):
		assert type(data) is dict
		res = {}
		for k, v in data.items():
			if type(v) is list:
				res[k] = self.dumpLst2Dct(v)
			elif type(v) is dict:
				res[k] = self.xtransfer(self.dumpDct2Dct(v))
			else:
				if v is not None:
					res[k] = v
			if type(res[k]) is None:
				res.pop(k)
		return res

	def dumpLst2Dct(self, data):
		assert type(data) is list
		dlen = len(data)
		if dlen == 0:
			return {}

		res = {}
		for i in xrange(dlen):
			item = data[i]
			if type(item) is dict:
				for k, v in item.items():
					kd = self.dumpDct2Dct({k:v})
					if k in kd.keys():
						if type(kd[k]) is dict:
							res[k] = self.xtransfer(kd[k])
						else:
							res[k] = kd[k]
			elif type(item) is list:
				tmp = self.dumpLst2Dct(item)
				if type(tmp) is dict:
					tmp = self.xtransfer(tmp)
				if tmp is not None:
					res[i+1] = tmp
			else:
				res[i+1] = item
		return res

	def dumpDict(self):
		return self.dumpLst2Dct(self.luaLst)


if __name__ == '__main__':
	s = '{"hello",key="value", {"in", 3, 4, [1.23]=56, nil, {mixed="inin", nice={0,9,8}}}, 1, 2} --hello'
	s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {{}}, [1]=678, ["yada,had"]="nice", hello="worl,[]\\\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	s = '{{{}},{1, 2, 3,}, hello="world"}  -- i am xuxinhui '
	# s = '"hello"}'
	# s = "{['array']={65,23,5,{1,2,3},{{}},[1]=78,['yada,had']='nice',['hello']='worl,[]\"ddefj'},['dict']={['mixed']={43,54.33,9,['string']={'value]','hello',{11,22}}},['array']={3,6,4},['string']='value'}}"
	# s = '{1, 2}'
	# s = '{{hello="world"}, hel=1}'
	parser = PyLuaTblParser()

	parser.load(s)
	print 'luaLst:', parser.luaLst

	s = parser.dump()
	print 'luaStr:', parser.luaStr

	d = parser.dumpDict()
	print 'd =', d

	parser.loadDict(d)
	print 'loadDict luaLst:', parser.luaLst

	s = parser.dump()
	print 'luaStr:', s

	d = parser.dumpDict()
	print 'd =', d