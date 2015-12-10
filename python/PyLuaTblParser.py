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

	def prev(self):
		if 1 < self.curPos <= self.totLen:
			return self.luaStr[self.curPos-2]
		return None

	# skip the whitespace which includes \t\n\r\b\f\v and ' '
	def skip(self):
		ch = self.next()
		escape = '\t\n\r\b\f\v\a'
		while ch is not None and (ch == ' ' or ch in escape):
			ch = self.next()
		if ch is not None:
			self.putback()

	def annotation(self):
		self.skip()
		ch = self.next()
		if ch != '-':
			self.putback()
			return
		elif self.next() != '-':
			self.putback()
			self.putback()
			return

		ch = self.next()
		if ch != '[':
			while ch is not None and ch != '\n':
				ch = self.next()
			# check cascading annotation like lua table = {--[[annotation1]]  --[[annotation2]] 1,2}
			self.annotation()
			return

		ch = self.next()
		lEqCnt, rEqCnt = 0, 0
		while ch is not None and ch == '=':
			lEqCnt += 1
			ch = self.next()
		if ch != '[':	# if it does not have pattern --[==[
			while ch is not None and ch != '\n':
				ch = self.next()
		else:	# if it has pattern --[==[, we are now try to find ]==]
			while True:
				ch = self.next()
				if ch is None:
					break
				while ch is not None and ch != ']':
					ch = self.next()
				if ch is None:
					break
				ch = self.next()
				while ch is not None and ch == '=':
					rEqCnt += 1
					ch = self.next()
				if ch == ']':
					if lEqCnt == rEqCnt:
						break
					else:
						self.putback()
				rEqCnt = 0
		# check cascading annotation like lua table = {--[==[annotation1]==]  --[[annotation2]] 1,2}
		self.annotation()

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

	# get string which formatted as "string" or 'string'
	def getStr(self, quotationMark):
		s = ''
		mp = {'"': '"', '\'': '\'', 'a': '\a', 'b': '\b', 't': '\t', 'r': '\r', 'n': '\n', 'f': '\f', 'v': '\v'}
		prev = None
		cur = self.next()
		while cur is not None:
			if cur == quotationMark and prev != '\\':
				break

			if cur in '\'\"abtrfnv' and prev == '\\':
				# if we have \\\'(\\\"), then let it be \'(\")
				s = s[:-1] + mp[cur]
				prev = cur
				cur = self.next()
				continue

			s += cur
			prev = cur
			cur = self.next()

		if cur != quotationMark:
			raise ValueError('Quotation mark does not match !!!')
		# print 'return s =', s
		return s

	# get the number which includes float and int
	def getNumber(self, flag=True):
		s = ''
		cur = self.next()
		exp = ".+-*/aAbBcCdDeEfFxX"
		while cur is not None and (self.isDigit(cur) or cur in exp):
			s += cur
			cur = self.next()

		if cur is not None:
			self.putback()

		return eval(s)

	# check special string nil|false|true
	def checkSpecialStr(self, s):
		if s == 'nil':
			return None
		elif s == 'false':
			return False
		elif s == 'true':
			return True

		return s

	# get variable which begins with a-z or A-Z or _
	# and the following can be a-z or A-Z or 0-9 or _
	def getVar(self, flag=True):
		s = ''
		ch = self.next()
		while ch is not None and (self.isAlphanum(ch) or ch == '_'):
			s += ch
			ch = self.next()

		if ch is not None:
			self.putback()
		return s

	# get value which can be table|number|string|variable
	def getValue(self):
		val = None
		self.annotation()
		self.skip()
		ch = self.next()
		if ch == '"' or ch == '\'':
			val = self.getStr(ch)
		elif self.isDigit(ch) or ch in '.-':
			self.putback()
			val = self.getNumber()
		elif ch == '{':
			val = self.getItem(True)
		elif self.isAlphabet(ch) or ch == '_':
			self.putback()
			val = self.getVar()
			val = self.checkSpecialStr(val)
		else:
			self.xTraceError(ch)

		return val

	def xTraceError(self, ch):
		if ch is None:
			raise ValueError
		if self.isDigit(ch):
			raise ValueError
		if self.isAlphabet(ch) or ch == '_':
			if ch in 'eE':
				raise ValueError
			raise ValueError
		if ch in ',;':
			raise ValueError
		if ch in '+-*/=%':
			if ch == '=':
				raise ValueError
			if ch == '-':
				raise ValueError
			raise ValueError
		if ch in '.$#@^&?|"`~:\'':
			if ch == '.':
				raise ValueError
			if ch == '"':
				raise ValueError
			if ch == '\'':
				raise ValueError
			raise ValueError
		if ch in '[]{':
			if ch == '[':
				raise ValueError
			if ch == ']':
				raise ValueError
			if ch == '{':
				raise ValueError
		if ch in '\t\r\n\a\v\f\b ':
			if ch == '\n':
				raise ValueError
			if ch == ' ':
				raise ValueError
			raise ValueError
		if ch == '\\':
			raise ValueError

		if ch == '}':
			raise ValueError

		raise ValueError

	# process the trailing , or ; or }
	def trailing(self, selector):
		if selector == 0:
			return

		self.annotation()
		self.skip()
		ch = self.next()
		if (selector == 1 and ch is None) or ch == ',' or ch == ';':
			return
		elif ch == '}':
			self.putback()
		else:
			self.xTraceError(ch)

	# parse the input string as lua table
	def getItem(self, bracketFlag=False):
		ans = []
		while True:
			self.annotation()
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
				return ans

			if ch == '{':
				item = self.getItem(True)
				self.skip()
				ch = self.next()
				if ch is None and not bracketFlag:
					ans.append(item)
					if len(ans) == 1:
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
				self.annotation()
				key, val = None, None

				self.skip()
				ch = self.next()
				# the key is either string or number
				if ch == '"' or ch == '\'':
					key = self.getStr(ch)
				else:
					self.putback()
					key = self.getNumber()

				self.annotation()
				self.skip()
				ch = self.next()
				if ch != ']':
					raise ValueError('Square brackets does not match !!!')

				self.annotation()
				self.skip()
				if self.next() != '=':
					raise ValueError('Illegal expression #equal symbol(=) missed# !!!')

				val = self.getValue()
				if key is None or key == '':
					raise ValueError('Key can not be Empty or None !!!')

				if val is not None or type(key) is int:
					ans.append({key: val})
				selector = 2
			elif self.isDigit(ch) or ch in '.-':
				self.putback()
				num = self.getNumber()
				ans.append(num)
				selector = 2
			elif self.isAlphabet(ch) or ch == '_':
				self.putback()
				key = self.getVar()
				key = self.checkSpecialStr(key)

				self.annotation()
				self.skip()
				ch = self.next()
				if ch in ',;}':
					if ch == '}':
						self.putback()
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
				msg = 'Invalid lua table string, ch = %s' % ch
				raise ValueError(msg)
			# processing trailing , or ; or }
			self.trailing(selector)
		
		if len(ans) == 1:
			ans = ans[0]
		return ans


	def load(self, s):
		self.luaStr = s
		self.curPos = 0
		self.totLen = len(s)
		self.luaLst = self.getItem()
		if type(self.luaLst) is not list:
			self.luaLst = [self.luaLst]

	def strValue(self, s):
		mp = {'"': '\\\"', '\'': '\\\'', '\a': '\\a', '\b': '\\b', '\t': '\\t', '\r': '\\r', '\n': '\\n', '\f': '\\f', '\v': '\\v'}
		t, i, slen = '', 0, len(s)
		while i < slen:
			if s[i] in '\'\"\a\b\f\v\t\r\n':
				t += mp[s[i]]
			else:
				t += s[i]
			i += 1
		return t

	def dumpList2String(self, data):
		assert type(data) is list
		datalen = len(data)
		s = "{"
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
					s += "'" + self.strValue(str(data[i])) + "',"
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
				s += "['" + self.strValue(str(key)) + "']="
			else:
				s += "[" + str(key) + "]="

			if type(value) is dict:
				s += self.dumpDict2String(value) + ","
			elif type(value) is list:
				s += self.dumpList2String(value) + ","
			elif type(value) is bool:
				s += str(value).lower()
			elif value is None:
				s += "nil,"
			else:
				try:
					f = float(value)
				except ValueError:
					s += "'" + self.strValue(str(value)) + "',"
				else:
					s += str(value) + ","
		if len(s) > 0 and s[-1] == ',':
			s = s[:-1]
		if len(keys) > 1:
			s += "}"
		return s

	def dump(self):
		if self.luaLst == []:
			self.luaStr = '{}'
		else:
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
				if type(item) is not list:
					item = [item]
			else:
				item = lst[i]
			res.append(item)
		return res


	def loadFromDict(self, d):
		assert type(d) is dict
		lst = []
		index = 1
		keys = d.keys()
		for key in keys:
			item = None
			if type(d[key]) is list:
				item = self.loadFromList(d[key])
			elif type(d[key]) is dict:
				item = self.loadFromDict(d[key])
			elif d[key] is not None:
				item = d[key]

			if type(key) is int and key == index:
				lst.append(item)
				index += 1
			else:
				lst.append({key: item})
		return lst


	def loadDict(self, d):
		self.luaLst = self.loadFromDict(d)

	# transform dict in pattern like {1:1, 2:2, 3:3...., n:n} to list like [1,2,3...n]
	def xtransferHelper(self, val):
		if type(val) is dict:
			return self.xtransfer(val)

		return val


	def xtransfer(self, dct):
		if type(dct) is not dict:
			return dct

		maxKey = -1
		flag = True
		for key, val in dct.items():
			if type(key) is not int:
				flag = False
			else:
				maxKey = max(maxKey, key)
			dct[key] = self.xtransferHelper(val)

		if not flag or maxKey != len(dct.items()):
			return dct

		res = []
		for i in xrange(len(dct.items())):
			res.append(dct[i+1])
		return res

	def dumpDct2Dct(self, d):
		assert type(d) is dict
		res = {}
		for k, v in d.items():
			if type(v) is list:
				res[k] = self.dumpLst2Dct(v)
			elif type(v) is dict:
				res[k] = self.dumpDct2Dct(v)
			elif v is not None:
				res[k] = v
			if k in res.keys() and res[k] is None:
				res.pop(k)
			
		return res

	def dumpLst2Dct(self, lst):
		assert type(lst) is list
		dlen = len(lst)
		index = 1
		res = {}
		for i in xrange(dlen):
			item = lst[i]
			if type(item) is dict:
				r = self.dumpDct2Dct(item)
				for k, v in r.items():
					if v is not None:
						res[k] = v
			elif type(item) is list:
				r = self.dumpLst2Dct(item)
				r = self.xtransfer(r)
				if r is not None:
					res[index] = r
					index += 1
			else:
				if item is not None:
					res[index] = item
				index += 1
		ret = {}
		for k, v in res.items():
			ret[k] = self.xtransfer(v)

		return ret

	def dumpDict(self):
		return self.dumpLst2Dct(self.luaLst)


if __name__ == '__main__':
	s = '{"hello",key="value", {"in", 3, 4, [1.23]=56, nil, {mixed="inin", nice={0,9,8}}}, 1, 2} --hello'
	s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {{}}, [1]=678, ["yada,had"]="nice", hello="worl,[]\\\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	# s = '{{{}},{1, 2, 3,}, hello="world"}, "hh"'
	# s = '"hello"'
	s = "{['array']={65,23,5,{1,2,3},{{11,22,33}},{{}},[1]=78,['yada,had']='nice',['hello']='worl,[]\"ddefj'},['dict']={['mixed']={43,54.33,9,['string']={'value]','hello',{11,22}}},['array']={3,6,4},['string']='value'}}"
	# s = '{{1, 2}, {{{{}}}}}'
	# s = '{hello="world"; {hhh=2, [4]=1},{{}}, hel=1,nil, false, true,s 2, .123, "#, 0xea, \t\r\n\\\\,k"}'
	# s = '{1, 2, array={2, 3, 4, "hi"}}'
	# s = '{{{{1, 2, 3}, 4}}}'
	s = '{["hel\\\'\\\'\\\'\\\'\\\'l"]=1}'
	# s = '{h=1,o=1,k=3}'
	# s = '{{11,22,33}, 4, {{{5, 6, 7}}}, hel=0}'
	# s = '{1, 2, 3, hl="aa",		yi="dd"}'
	# s = '{array={1, 2, 3, true}, [4]=9, false}'
	# s = '{abc}'
	# s = '{var={{var=1}}} --}'
	# s = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
	# s = '{abc}'
	# s = '{a = 1,{["object with 1 member"] = {"array with 1 element",},},"test"}'
	# s = '{23,.24,-0.98e1,-.1}'
	# s = '{{[1] = "nil", nil, nil, [3] = 34, {},--[[yy]]--[===[kk]===][6] --[=[tt]=]= --[[dd]]nil, io --[[oo]]= 90,--[[name]]-.23}}'
	# s = '{[\'u\\\'root\\\'\'] = {5,4,6},1,6,7,string = \'value\',}'
	# s = '{array = \'abc\\\"bca!@#$%^&*()+_| \',1,4,\'d\'}'
	# s = '{[\'seperate name test\']=123, [\"seperate name 2\"]= {[\'seperate name 3\'] = 321},}'
	# s = '{[--[==[comment]=]==]1]=1}'
	# s = '{[34]=1, name={helo=1}}'
	# s = '{a = 1,{["object with 1 member"] = {"array with 1 element",},},"test"}'
	# s = "{{1.123,-415,-64.13},{},root=123}"
	# s = '{1, 2, 3}'
	# s = '{{{{}}}}'
	# s = '{[\'u\\\'root\\\'\'] = {5,4,6},1,6,7,string = \'value\',}'
	s = '{[\'u\\\'root\\\'\'] = {5,4,6},1,6,7,string = \'value\',}'
	s = '{array = \'abc\\\"bca!@#$%^&*()+_| \',1,4,\'d\'}'
	# s = '{var={"val", {["key"]="val"},}, {}, [11]=-1, var, arb, }'
	# s = '{{[1] = "nil", nil, nil, [3] = 34, {},[6] = nil, io = 90}}'
	parser = PyLuaTblParser()

	print 'SOURCE s =', s
	parser.load(s)
	print 'luaLst:', parser.luaLst

	s = parser.dump()
	print 'luaStr:', parser.luaStr

	d = parser.dumpDict()
	print 'luaDct:', d

	parser.loadDict(d)
	print 'loadDict luaLst:', parser.luaLst

	s = parser.dump()
	print 'luaStr:', s

	parser.load(s)
	print parser.luaLst
	d = parser.dumpDict()
	print 'd =', d

	s = parser.dump()
	print s
	parser.load(s)