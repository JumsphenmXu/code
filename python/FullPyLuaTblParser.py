#!/usr/bin/python

# Author: XU Xinhui
# Email: xuxh13@163.com

class PyLuaTblParser(object):
	"""
	Python Lua Table Parser:
		1. load(self, s): 
			@Param s: a lua-formatted string
			@Description: Given a string s which represents a lua-formatted table,
				parse the string s into the python-formatted dict.
			@RETURN: no return
		2. dump(self):
			@Description: Given the data (i.e. dict formatted) in class PyLuaTblParser, 
				format it as a lua-table.
			@RETURN: lua table string
		3. loadLuaTable(self, f):
			@Param f: file path
			@Description: Given a file path f which stores a lua-formatted table,
				read the file and parse it into the python-formatted dict.
			@RETURN: no return 
		4. dumpLuaTable(self, f):
			@Param f: file path
			@Description: Given the data (i.e. dict formatted) in class PyLuaTblParser, 
				format it as a lua-table, and write the lua-formatted result back to the file
			@RETURN: no return
		5. loadDict(self, d):
			@Param d: the data dict
			@Description: Give the data dict d, put the data in d into the PyLuaTblParser attributes.
			@RETURN: no return
		6. dumpDict(self):
			@Description: Format the data in class PyLuaTblParser to a python dict.
			@RETURN: a python dict
		7. update(self, d):
			@Param d: the data dict
			@Description: using the dict to update the inner data structure
			@RETURN: no return
		8. __getitem__(self, key), __setitem__(self, key, value):
			@Param key: the key to operate 
			@Param value: data to set
			@Description: By PyLuaTblParser[key], return the inner data indexed by @key,
				when given PyLuaTblParser[key]=value, update the @key by @value.
			@RETURN: --

	"""

	# parse item status, let it be class attribute,
	# normally, we should not change the value of class attribute.
	KLASS_ISLIST = 0
	KLASS_ISDICT = 1
	KLASS_ISBOOL = 2
	KLASS_ISNIL = 3
	KLASS_ISSTR = 4
	KLASS_ISINT = 5
	KLASS_ISFLT = 6
	KLASS_ISOTHER = 7
	__CONF_DEBUG_ = False
	# __CONF_DEBUG_ = True

	lDelis = ['"', '\'', '[']
	rDelis = {'"': '"', '\'': '\'', '[': ']'}

	# PyLuaTblParser class inner data structure: luaTblList
	def __init__(self, luaTblList=[]):
		self.luaTblList = luaTblList

	# Here @s is the source string, @index is the position where start to search,
	# @deli is the delimiter to match, @flag indicates whether the result is found.
	def __delimitMatcher(self, s, index, deli, flag):
		i, slen = index + 1, len(s)
		res = -1
		while i < slen:
			while i < slen and s[i] == deli:
				res = i
				flag = True
				i = self.__delimitMatcher(s, i, deli, flag)
			if res != -1:
				i = res
				break
			else:
				i += 1

		if i == slen and not flag:
			print 'Square bracket expression ###%s### represents a error.' % s[index: i-1]
			raise ValueError

		return i


	def __eliminate_whitespace(self, s):
		i, slen, t = 0, len(s), ''
		while i < slen:
			if s[i] != ' ':
				t += s[i]
			i += 1

		return t


	def __eliminate_annotation(self, s):
		i, slen, t = 0, len(s), ''
		while i < slen:
			if s[i] == '"' or s[i] == '\'':
				f = s[i]
				t += s[i]
				i += 1
				while i < slen:
					t += s[i]
					if s[i] == f and i > 1 and s[i-1] != '\\':
						break
					i += 1
			elif s[i] == '-':
				if i + 1 < slen and s[i+1] == '-':
					if i + 2 < slen and s[i+2] == '[':
						# --[[annotation]]
						if i + 3 < slen and s[i+3] == '[':
							i += 4
							while i < slen:
								if s[i] == ']' and i + 1 < slen and s[i+1] == ']':
									if i > 0 and s[i-1] != '\\':
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
			else:
				t += s[i]

			i += 1

		return t
				


	# STAGE 1: preprocessing the source string
	def __partition(self, s):
		# s = self.__eliminate_whitespace(s)
		start, lbc, rbc, i, slen = 0, 0, 0, 0, len(s)
		if slen > 0 and s[0] == '{' and s[slen-1] == '}':
			s = s[1: -1]

		if len(s) > 0 and (s[-1] == ',' or s[-1] == ';'):
			s = s[:-1]
		slen = len(s)
		parts = []
		i = 0
		if PyLuaTblParser.__CONF_DEBUG_:
			print 'start to partition, source string:', s
		while i < slen:
			if s[i] == '{':
				lbc += 1
			elif s[i] == '}':
				rbc += 1
				if i == slen - 1 and lbc == rbc:
					parts.append(s[start: i+1])
					return parts
			elif (s[i] == '"' or s[i] == '\'') and (i == 0 or (i > 0 and s[i-1] != '\\')):
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#1# s[%d:%d] = %s' % (start, i, s[start: i])
				f = s[i]
				i += 1
				while i < slen:
					if s[i] != f or s[i-1] == '\\':
						i += 1
						continue
					if i == slen - 1:
						parts.append(s[start: slen])
						return parts
					if i+1 < slen and (s[i+1] == ',' or s[i+1] == ';' or s[i+1] == '}'):
						break
					i += 1
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#2# s[%d:%d] = %s' % (start, i, s[start: i])
			elif s[i] == '[':
				f = ''
				i += 1
				if i < slen:
					if s[i] == '"' or s[i] == '\'':
						f = s[i]
				if f != '':
					while i < slen:
						i += 1
						if i < slen and s[i] != f or s[i-1] == '\\':
							continue
						end = i < slen and s[i] == f and i+1 < slen and s[i+1] == ']' and i+2 < slen and s[i+2] == '='
						if end:
							i += 2
							break
				else:
					while i < slen and s[i] != ']':
						i += 1			
			elif i == slen - 1 or s[i] == ',' or s[i] == ';':
				if PyLuaTblParser.__CONF_DEBUG_:
					print 'lbc = %d, rbc = %d' % (lbc, rbc)
				if lbc != rbc:
					if i == slen - 1:
						print 'Failed to partition %s, the brackets do not match!' % s
						raise ValueError
					else:
						i += 1
						continue
				else:
					# add to the parts
					if i == slen - 1:
						i = i + 1
					parts.append(s[start: i])
					if PyLuaTblParser.__CONF_DEBUG_:
						print '#3# s[%d:%d] = %s' % (start, i, s[start: i])
					start = i + 1
					lbc, rbc = 0, 0
			i += 1
		# end main while loop
		if PyLuaTblParser.__CONF_DEBUG_:
			print "parts =", parts
		return parts

	# STAGE 2: after the STAGE 1, we get items to do further determination,
	# 	namely, we validate the item type (numeric, bool, nil, array, dict, string etc.),
	#	and pick out the invalid items and raise ValueError to notify the caller.
	def __itemParse(self, s):
		# print "__itemParse s =", s
		# remove the leading and trailing whitespace
		# s = self.__eliminate_whitespace(s)
		if PyLuaTblParser.__CONF_DEBUG_:
			print '__itemParse after __eliminate_whitespace s =', s
		if len(s) == 0:
			return None, PyLuaTblParser.KLASS_ISNIL
		# remove the leading and trailing brackets
		i, j = 0, len(s) - 1
		while i < j:
			if s[i] == "{" and s[j] == "}":
				i += 1
				j -= 1
			else:
				break

		t = s[i:j+1]
		if PyLuaTblParser.__CONF_DEBUG_:
			print '__itemParse: s =', s
			print '__itemParse: t =', t
		if len(t) == 0:
			rs = []
			s = s[1:-1]
			result, status = self.__itemParse(s)
			if status != PyLuaTblParser.KLASS_ISNIL:
				rs.append(result)
			return rs, PyLuaTblParser.KLASS_ISLIST
		res = None
		# if we have PATTERN like {member1, member2, member3, ..., membern},
		# we parse it as a list.
		if len(t) != len(s):
			ret = []
			resTmp = self.__partition(t)
			if PyLuaTblParser.__CONF_DEBUG_:
				print '__itemParse resTmp =',resTmp
			for item in resTmp:
				if PyLuaTblParser.__CONF_DEBUG_:
					print '__itemParse item =',item
				ans, status = self.__itemParse(item)
				if status != PyLuaTblParser.KLASS_ISNIL:
					ret.append(ans)
			
			if PyLuaTblParser.__CONF_DEBUG_:
				print '__itemParse ret =',ret
				print '__itemParse res =', res
			return ret, PyLuaTblParser.KLASS_ISLIST

		# if we have PATTERN like '"string values"' or "'string values'",
		# we parse it as a string value
		if t[0] == '"' or t[0] == '\'':
			f = t[0]
			if t[-1] == f and t[-2] != '\\':
				return t[1:-1], PyLuaTblParser.KLASS_ISSTR
			else:
				print 'Failed to parse item #%s# as a string.' % t
				raise ValueError

		if PyLuaTblParser.__CONF_DEBUG_:
			print 'Dict t =', t
		equalIdx = t.find("=")
		# if we find PATTERN like key = {value1, value2, value3, ..., valuen},
		# we parse it as a dict
		if equalIdx == -1:
			# The PATTERN IS NOT a dict, we should check the special value false and nil
			if t == "false" or t == "true":
				return t, PyLuaTblParser.KLASS_ISBOOL
			if t == "nil":
				return t, PyLuaTblParser.KLASS_ISNIL

			# Here we try to validate the PATTERN as a numeric (int or float),
			# if the validation failed, we flag a ValueError to notify the caller.
			if t.find(".") >= 0:
				return float(t), PyLuaTblParser.KLASS_ISFLT
			else:
				return int(t), PyLuaTblParser.KLASS_ISINT
		else:
			leftPart = t[0: equalIdx]
			rightPart = t[equalIdx+1: len(t)]

			if leftPart == "nil" or len(leftPart) == 0 or len(rightPart) == 0:
				print 'Failed to parse item #%s# as a python dict !!!' % t
				raise ValueError

			if rightPart == "nil":
				return None, PyLuaTblParser.KLASS_ISNIL

			if PyLuaTblParser.__CONF_DEBUG_:
				print 'leftPart = %s, rightPart = %s' % (leftPart, rightPart)
			if len(leftPart) > 0:
				if leftPart[0] == '[':
					if leftPart[-1] != ']':
						print 'Failed to parse item #%s# as a dict !!!' % t
						raise ValueError
					tf = leftPart[1]
					if tf == '"' or tf == '\'':
						if leftPart[-2] != tf:
							print 'Failed to parse item #%s# as a dict !!!' % t
							raise ValueError
						else:
							leftPart = leftPart[2: -2]
					else:
						leftPart = leftPart[1: -1]
						if leftPart.find(".") >= 0:
							leftPart = float(leftPart)
						else:
							leftPart = int(leftPart)
			res = {}
			rightPartList = self.__loadFromString(rightPart)
			if len(rightPartList) == 1:
				res[leftPart] = rightPartList[0]
			else:
				res[leftPart] = rightPartList

			if PyLuaTblParser.__CONF_DEBUG_:
				print 'res[%s] = %s' % (str(leftPart), res[leftPart])
			if res[leftPart] == "nil":
				return None, PyLuaTblParser.KLASS_ISNIL

			return res, PyLuaTblParser.KLASS_ISDICT

		return None, PyLuaTblParser.KLASS_ISNIL


	def __loadFromString(self, s):
		# s = self.__eliminate_whitespace(s)
		parts = self.__partition(s)

		if PyLuaTblParser.__CONF_DEBUG_:
			print '__loadFromString: parts =', parts
		dictTmp = {}
		listTmp = []
		for item in parts:
			res, status = self.__itemParse(item)
			if status == PyLuaTblParser.KLASS_ISNIL:
				continue
			if status != PyLuaTblParser.KLASS_ISDICT:
				listTmp.append(res)
			else:
				key, val = res.keys()[0], res.values()[0]
				if key in dictTmp.keys():
					if type(key) is not int:
						print "Key #%s# conflicts occurred in table %s." % (key, s)
						raise ValueError
				else:
					dictTmp[key] = val

		for k, v in dictTmp.items():
			if type(k) is int and k < len(listTmp):
				continue
			else:
				listTmp.append({k: v})

		return listTmp


	def load(self, s):
		s = self.__eliminate_whitespace(s)
		s = self.__eliminate_annotation(s)
		print 'After preprocessing, s = ', s
		self.luaTblList = self.__loadFromString(s)
		if PyLuaTblParser.__CONF_DEBUG_:
			print 'load(self, s) -->', self.luaTblList


	def __dumpList2String(self, data):
		if PyLuaTblParser.__CONF_DEBUG_:
			print '__dumpList2String data =', data
		assert type(data) is list

		datalen = len(data)
		s = ""
		if datalen == 1 and type(data[0]) is list:
			s += "{" +  self.__dumpList2String(data[0]) + "}"
			return s

		s += "{"
		for i in xrange(datalen):
			if type(data[i]) is dict:
				s += self.__dumpDict2String(data[i]) + ","
			elif type(data[i]) is list:
				s += self.__dumpList2String(data[i]) + ","
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

	def __dumpDict2String(self, data):
		if PyLuaTblParser.__CONF_DEBUG_:
			print '__dumpDict2String data =', data

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
				s += self.__dumpDict2String(value) + ","
			elif type(value) is list:
				s += self.__dumpList2String(value) + ","
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
		lst = self.luaTblList
		s = self.__dumpList2String(lst)
		return s


	def loadLuaTable(self, f):
		fp = open(f, "rb")
		line = fp.read()
		fp.close()
		self.load(line)

	def dumpLuaTable(self, f):
		s = self.dump()
		fp = open(f, "wb")
		fp.write(s)
		fp.close()


	def __loadFromList(self, lst):
		assert type(lst) is list
		res = []
		for i in xrange(len(lst)):
			item = None
			if type(lst[i]) is dict:
				item = self.__loadFromDict(lst[i])
			elif type(lst[i]) is list:
				item = self.__loadFromList(lst[i])
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

			if PyLuaTblParser.__CONF_DEBUG_:
					print '#1# __loadFromList: lst[i]=', lst[i]
					print '#1# __loadFromList: res=', res

		if PyLuaTblParser.__CONF_DEBUG_:
			print '__loadFromList return:', res
		return res


	def __loadFromDict(self, d):
		assert type(d) is dict
		listTmp = []
		index = 1
		keys = d.keys()

		for key in keys:
			item = None
			if type(d[key]) is list:
				item = self.__loadFromList(d[key])
			elif type(d[key]) is dict:
				item = self.__loadFromDict(d[key])
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

			if PyLuaTblParser.__CONF_DEBUG_:
				print '#1# __loadFromDict: key =', key
				print '#1# __loadFromDict: d[key] =', d[key]
				print '#1# __loadFromDict: listTmp =', listTmp

		return listTmp


	def loadDict(self, d):
		self.luaTblList = self.__loadFromDict(d)
		if PyLuaTblParser.__CONF_DEBUG_:
			print 'loadDict(self, d) -->', self.luaTblList


	def __xtransfer(self, dct):
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


	def __dumpInnerDict2PythonDict(self, data):
		# print '__dumpInnerDict2PythonDict data =', data
		assert type(data) is dict
		res = {}

		for k, v in data.items():
			if type(v) is list:
				res[k] = self.__dumpInnerList2PythonDict(v)
			elif type(v) is dict:
				res[k] = self.__xtransfer(self.__dumpInnerDict2PythonDict(v))
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


	def __dumpInnerList2PythonDict(self, data):
		# print '__dumpInnerList2PythonDict data =', data
		assert type(data) is list
		dlen = len(data)

		if dlen == 0:
			return {}

		res = {}
		for i in xrange(len(data)):
			item = data[i]
			# print 'item = ', item

			if type(item) is dict:
				for k, v in item.items():
					kd = self.__dumpInnerDict2PythonDict({k:v})
					if k in kd.keys():
						if type(kd[k]) is dict:
							res[k] = self.__xtransfer(kd[k])
						else:
							res[k] = kd[k]
			elif type(item) is list:
				tmp = self.__dumpInnerList2PythonDict(item)
				# print 'tmp = ', tmp
				if type(tmp) is dict:
					tmp = self.__xtransfer(tmp)
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
		return self.__dumpInnerList2PythonDict(self.luaTblList)


	def update(self, d):
		dct = self.dumpDict(self.luaTblList)
		dct.update(d)
		self.loadDict(dct)


	# for the index operator functionalities,
	# overloading __getitem__, __setitem__ function
	def __getitem__(self, key):
		dct = self.dumpDict(self.luaTblList)
		if key not in dct.keys():
			raise KeyError

		return dct[key]


	def __setitem__(self, key, value):
		dct = self.dumpDict(self.luaTblList)
		dct[key] = value
		self.loadDict(dct)


if __name__ == '__main__':
	s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {{}}, [1]=678, ["yada,had"]="nice", hello="worl,[]\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	# s = '{[10]="a"}'
	# s = '{"abc", nil, hello="nice", 345}'
	# s = '{array = {65,23,5,{1, 2, 3}, [1]=678, hello="worlddefj"},dict = {mixed = {43,54.33,"hello",yy={11,22,}},array = {3,6,4}}}'
	# s = '{{{}}}'
	# s = '{1, 2, 3}'
	# s = '{"abc", 2, 3}'
	# s = '{[--[[nice a]]"a"] = 1, "hello", --[[annotation]]} --hello'
	s = '{--[==[nice annotation]==]   1,hello="when"; "{hakd"}'
	parser = PyLuaTblParser()
	parser.load(s)

	print 'luaTblList =', parser.luaTblList

	luaTblDumpedStr = parser.dump()
	print 'luaTblDumpedStr =', luaTblDumpedStr

	luaTblDumpedDict = parser.dumpDict()
	print 'luaTblDumpedDict =', luaTblDumpedDict

	parser.loadDict(luaTblDumpedDict)
	print 'After loadDict, luaTblList =', parser.luaTblList	
	print 'parser dump after loadDict:', parser.dump()

# 	# set newAttributeList to a list
# 	parser['newAttributeList'] = [10, "I am XU", {"newKey": "newValue"}]

# 	# set newAttributeDict to a dict
# 	parser['newAttributeDict'] = {"DKey1": [{"Dkey2": "DVal2"}, [100, 1000, {"NICE": "GOOD"}], "I am Xin"], "LastName": "HUI"}

# 	print 'luaTblDumpedDict after setting some new features:', parser.dumpDict()
# 	print 'luaTblStr after setting some new features:', parser.dump()

	# print 'get array attribute in PyLuaTblParser:', parser["array"]