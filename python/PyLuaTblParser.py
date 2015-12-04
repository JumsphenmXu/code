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

	# PyLuaTblParser class inner data structure: luaTblDict
	def __init__(self, luaTblDict={}):
		self.luaTblDict = luaTblDict

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

	# STAGE 1: preprocessing the source string
	def __partition(self, s):
		s = self.__eliminate_whitespace(s)
		start, lbc, rbc, i, slen = 0, 0, 0, 0, len(s)
		if slen > 0 and s[0] == '{' and s[slen-1] == '}':
			s = s[1: -1]

		if len(s) > 0 and s[-1] == ',':
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
			elif s[i] == '"' or s[i] == '\'':
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#1# s[%d:%d] = %s' % (start, i, s[start: i])
				f = s[i]
				i += 1
				while i < slen:
					if s[i] != f or s[i-1]=='\\':
						i += 1
						continue
					if i == slen - 1:
						parts.append(s[start: slen])
						return parts
					if i+1 < slen and (s[i+1] == ',' or s[i+1] == '}'):
						break
					i += 1
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#2# s[%d:%d] = %s' % (start, i, s[start: i])
			elif s[i] == '[':
				f = ''
				i += 1
				if i < slen:
					f = '"' if s[i] == '"' else ('\'' if s[i] == '\'' else '')
				if f != '':
					while i < slen:
						i += 1
						if i < slen and s[i] != f or s[i-1] == '\\':
							continue
						end = i < slen and s[i] == f and i+1 < slen and s[i+1] == ']' and i+2 < slen and s[i+2] == '='
						if not end:
							i += 1
						else:
							i += 2
							break
				else:
					while i < slen and s[i] != ']':
						i += 1			
			elif i == slen - 1 or s[i] == ',':
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
		s = self.__eliminate_whitespace(s)
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
			
			res = {}
			for i in xrange(len(ret)):
				res[i+1] = ret[i]

			if PyLuaTblParser.__CONF_DEBUG_:
				print '__itemParse ret =',ret
				print '__itemParse res =', res
			return res, PyLuaTblParser.KLASS_ISLIST

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
			res[leftPart] = self.__loadFromString(rightPart)
			if PyLuaTblParser.__CONF_DEBUG_:
				print 'res[%s] = %s' % (str(leftPart), res[leftPart])
			if res[leftPart] == "nil":
				return None, PyLuaTblParser.KLASS_ISNIL

		return res, PyLuaTblParser.KLASS_ISDICT 


	def __loadFromString(self, s):
		index = 1
		s = self.__eliminate_whitespace(s)
		parts = self.__partition(s)

		if PyLuaTblParser.__CONF_DEBUG_:
			print '__loadFromString: parts =', parts
		dictTmp = {}
		for item in parts:
			res, status = self.__itemParse(item)
			if status == PyLuaTblParser.KLASS_ISNIL:
				continue

			if status != PyLuaTblParser.KLASS_ISDICT:
				dictTmp[index] = res
				index += 1
			else:
				key, val = res.keys()[0], res.values()[0]
				if key in dictTmp.keys():
					if type(key) is not int:
						print "Key #%s# conflicts occurred in table %s." % (key, s)
						raise ValueError
				else:
					dictTmp[key] = val

		return dictTmp


	def load(self, s):
		self.luaTblDict = self.__loadFromString(s)
		if PyLuaTblParser.__CONF_DEBUG_:
			print 'load(self, s) -->', self.luaTblDict


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
				if str(key).find(".") >= 0:
					s += "[" + str(key) + "]="
				# s += "[" + str(key) + "]="

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
		dictTmp = self.luaTblDict
		s = ''
		if len(dictTmp.keys()) == 1:
			s = '{' + self.__dumpDict2String(dictTmp) + '}'
		else:
			s = self.__dumpDict2String(dictTmp)
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
		res = {}
		index = 1
		for i in xrange(len(lst)):
			if type(lst[i]) is dict:
				for k, v in lst[i].items():
					res[k] = self.__loadFromDict({k: v})[k]
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#1# __loadFromList: lst[i]=', lst[i]
					print '#1# __loadFromList: res=', res
			elif type(lst[i]) is list:
				res[index] = self.__loadFromList(lst[i])
				if PyLuaTblParser.__CONF_DEBUG_:
					print 'type is list: lst[i] =', lst[i]
					print 'type is list: res[index] =', res[index]
				index += 1
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#2# __loadFromList: lst[i]=', lst[i]
					print '#2# __loadFromList: res=', res
			else:
				if type(lst[i]) is bool:
					res[index] = str(lst[i]).lower()
				else:
					res[index] = lst[i]
				index += 1

		if PyLuaTblParser.__CONF_DEBUG_:
			print '__loadFromList return:', res
		return res


	def __loadFromDict(self, d):
		assert type(d) is dict
		dictTmp = {}
		keys = d.keys()
		for key in keys:
			if type(d[key]) is list:
				dictTmp[key] = self.__loadFromList(d[key])
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#1# __loadFromDict: key=', key
					print '#1# __loadFromDict: d[key]=', d[key]
					print '#1# __loadFromDict: dictTmp[key]=', dictTmp[key]
			elif type(d[key]) is dict:
				dictTmp[key] = self.__loadFromDict(d[key])
				if PyLuaTblParser.__CONF_DEBUG_:
					print '#1# __loadFromDict: key=', key
					print '#2# __loadFromDict:', d[key]
					print '#2# __loadFromDict: dictTmp[key]=', dictTmp[key]
			else:
				if d[key] == False:
					dictTmp[key] = "false"
				elif d[key] == True:
					dictTmp[key] = "true"
				else:
					if type(d[key]) is int or type(d[key]) is float:
						dictTmp[key] = {1: d[key]}
					else:
						dictTmp[key] = {1: str(d[key])}

		return dictTmp


	def loadDict(self, d):
		self.luaTblDict = self.__loadFromDict(d)
		if PyLuaTblParser.__CONF_DEBUG_:
			print 'loadDict(self, d) -->', self.luaTblDict


	def __xtransfer(self, lst):
		assert type(lst) is list
		flag = True
		for i in xrange(len(lst)):
			if not type(lst[i]) is dict:
				flag = False
				return lst

		res = {}
		if flag:
			for i in xrange(len(lst)):
				key = lst[i].keys()[0]
				val = lst[i][key]
				res[key] = val
		return res


	def __dumpInnerDict2PythonDict(self, d):
		dictTmp = {}
		keys = d.keys()

		for key in keys:
			if type(d[key]) is dict:
				dkeys = d[key].keys()
				if len(dkeys) == 1:
					dictTmp[key] = d[key][dkeys[0]]
					continue

				dictTmp[key] = []
				print 'd[key] =', d[key]
				for k in dkeys:
					print 'k =', k
					item = self.__dumpInnerDict2PythonDict({k:d[key][k]})
					print 'item =', item
					if type(k) is int:
						dictTmp[key].append(item[k])
					else:
						dictTmp[key].append(item)
				dictTmp[key] = self.__xtransfer(dictTmp[key])
			elif type(d[key]) is list:
				pass
			else:
				# Firstly, process the special cases like nil, bool
				# if d[key] == "nil":
				# 	if type(key) is int:
				# 		dictTmp[key] = None
				# 	continue
				if d[key] == "false":
					dictTmp[key] = False
					continue

				if d[key] == "true":
					dictTmp[key] = True
					continue

				# Secondly, parse the numeric value, i.e. a float or an int
				try:
					f = float(d[key])
				except ValueError:
					dictTmp[key] = d[key]
				else:
					if str(d[key]).find(".") >= 0:
						dictTmp[key] = float(d[key])
					else:
						dictTmp[key] = int(d[key])
		if not dictTmp:
			dictTmp = {1: {}}		
		return dictTmp


	def dumpDict(self):
		return self.__dumpInnerDict2PythonDict(self.luaTblDict)


	def update(self, d):
		self.luaTblDict[key] = self.__loadFromDict(d)


	# for the index operator functionalities,
	# overloading __getitem__, __setitem__ function
	def __getitem__(self, key):
		keys = self.luaTblDict.keys()
		if key not in keys:
			raise KeyError

		return self.luaTblDict[key]


	def __setitem__(self, key, value):
		self.luaTblDict[key] = {}
		if type(value) is list:
			self.luaTblDict[key] = self.__loadFromList(value)
		elif type(value) is dict:
			self.luaTblDict[key] = self.__loadFromDict(value)
		else:
			self.luaTblDict[key] = {1: value}


if __name__ == '__main__':
	s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {}, [1]=678, ["yada,had"]="nice", hello="worl,[]\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	# s = '{[10]="a"}'
	# s = '{"abc"}'
	parser = PyLuaTblParser()
# 	parts = parser._PyLuaTblParser__partition(s)
# 	print parts
	parser.load(s)
	print parser.luaTblDict
	luaTblDumpedStr = parser.dump()
	print 'luaTblDumpedStr =', luaTblDumpedStr

	luaTblDumpedDict = parser.dumpDict()
	print 'luaTblDumpedDict =', luaTblDumpedDict

	parser.loadDict(luaTblDumpedDict)
	print 'parser dump after loadDict:', parser.dump()

	print '----', parser.luaTblDict

# 	# set newAttributeList to a list
# 	parser['newAttributeList'] = [10, "I am XU", {"newKey": "newValue"}]

# 	# set newAttributeDict to a dict
# 	parser['newAttributeDict'] = {"DKey1": [{"Dkey2": "DVal2"}, [100, 1000, {"NICE": "GOOD"}], "I am Xin"], "LastName": "HUI"}

# 	print 'luaTblDumpedDict after setting some new features:', parser.dumpDict()
# 	print 'luaTblStr after setting some new features:', parser.dump()

	# print 'get array attribute in PyLuaTblParser:', parser["array"]