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
	KLASS_OTHERS = 2

	# PyLuaTblParser class inner data structure: luaTblDict
	def __init__(self, luaTblDict={}):
		self.luaTblDict = luaTblDict

	# STAGE 1: preprocessing the source string
	def __partition(self, s):
		# remove leading and trailing whitespace
		s = s.strip()

		# remove the redundant leading and trailing brackets
		i, j = 0, len(s) - 1
		while i < j:
			if s[i] == "{" and s[j] == "}":
				i += 1
				j -= 1
			else:
				break

		# remove the redundant trailing comma
		if s[j] == ",":
			j -= 1

		# get the final string we do the further processing
		t = s[i:j+1]
		if len(t) == 0:
			return None

		# partition starts here
		start = 0
		leftBracketsCnt = 0
		rightBracketsCnt = 0
		parts = []
		for i in xrange(len(t)):
			if t[i] == '{':
				leftBracketsCnt += 1
			elif t[i] == '}':
				rightBracketsCnt += 1
				if i == len(t) - 1 and leftBracketsCnt == rightBracketsCnt:
					parts.append(t[start:i+1].strip())
					return parts
			elif t[i] == ',' or i == len(t) - 1:
				if leftBracketsCnt != rightBracketsCnt:
					if i == len(t) - 1:
						print 'Failed to partition %s, the brackets do not match!' % t
						raise ValueError
					else:
						continue

				if i == len(t) - 1:
					i = i + 1
				parts.append(t[start: i].strip())
				start = i + 1
				leftBracketsCnt = 0
				rightBracketsCnt = 0
		# end of for loop
		return parts

	# STAGE 2: after the STAGE 1, we get items to do further determination,
	# 	namely, we validate the item type (numeric, bool, nil, array, dict, string etc.),
	#	and pick out the invalid items and raise ValueError to notify the caller.
	def __itemParse(self, s):
		# print "__itemParse s =", s
		# remove the leading and trailing whitespace
		s = s.strip()

		# remove the leading and trailing brackets
		i, j = 0, len(s) - 1
		while i < j:
			if s[i] == "{" and s[j] == "}":
				i += 1
				j -= 1
			else:
				break

		t = s[i:j+1]
		res = None
		# if we have PATTERN like {member1, member2, member3, ..., membern},
		# we parse it as a list.
		if len(t) != len(s):
			ret = []
			resTmp = self.__partition(t)
			for item in resTmp:
				ans, status = self.__itemParse(item)
				ret.append(ans)
		
			res = {}
			for i in xrange(len(ret)):
				res[i+1] = ret[i]
			return res, PyLuaTblParser.KLASS_ISLIST

		# if we have PATTERN like '"string values"' or "'string values'",
		# we parse it as a string value
		if t[0] == '"':
			if t[len(t)-1] == '"':
				return t[1:-1], PyLuaTblParser.KLASS_OTHERS
			else:
				print 'Failed to parse item #%s#, element expected to be a string.' % t
				raise ValueError
		if t[0] == "'":
			if t[len(t)-1] == "'":
				return t[1:-1], PyLuaTblParser.KLASS_OTHERS
			else:
				print 'Failed to parse item #%s#, element expected to be a string.' % t
				raise ValueError

		equalIdx = t.find("=")
		# if we find PATTERN like key = {value1, value2, value3, ..., valuen},
		# we parse it as a dict
		if equalIdx == -1:
			# The PATTERN IS NOT a dict, we should check the special value false and nil
			if t == "false" or t == "nil" or t == "true":
				return t, PyLuaTblParser.KLASS_OTHERS

			# Here we try to validate the PATTERN as a numeric (int or float),
			# if the validation failed, we flag a ValueError to notify the caller. 
			try:
				f = float(t)
			except ValueError:
				print 'Failed to parse item #%s#, table element can not be %s.' % (t, t)
				raise ValueError
			else:
				return t, PyLuaTblParser.KLASS_OTHERS
		else:
			# Here we are certain that we got a dict, but we need to justify the key,
			# as lua tables, the KEY=VALUE can not be like the following examples,
			# BAD AND ILLEGAL KEY=VALUE PATTERN.
			# 	(1) 1=value          --> key can not be int 
			# 	(2) nil=value        --> key can not be KEYWORD nil
			# 	(3) 1.2=value        --> key can not be numeric
			# 	(4) a<op>b=value     --> key can not be the pattern like a.b or a+b, or a&b, or a*b etc.
			#	(5) =value           --> key can not be empty string

			leftPart = t[0:equalIdx].strip()
			rightPart = t[equalIdx+1:len(t)].strip()

			if leftPart == "nil" or len(leftPart) == 0 or len(rightPart) == 0:
				print 'Failed to parse item #%s#, dict key can not be nil.' % t
				raise ValueError

			for i in xrange(len(leftPart)):
				if 97 <= ord(leftPart[i]) <= 122 or 65 <= ord(leftPart[i]) <= 90:
					continue
				else:
					print 'Failed to parse item #%s#, dict key can not be %s.' % (t, leftPart)
					raise ValueError
			
			res = {}
			res[leftPart] = self.__load(rightPart)
		return res, PyLuaTblParser.KLASS_ISDICT 


	def __load(self, s):
		index = 1
		s = s.strip()
		parts = self.__partition(s)
		if not parts:
			return None

		dictTmp = {}
		for item in parts:
			res, status = self.__itemParse(item)
			if status == PyLuaTblParser.KLASS_OTHERS or status == PyLuaTblParser.KLASS_ISLIST:
				dictTmp[index] = res
				index += 1
			elif status == PyLuaTblParser.KLASS_ISDICT:
				key, val = res.keys()[0], res.values()[0]
				if key in dictTmp.keys():
					print "Key #%s# conflicts occured in table %s." % (key, s)
					raise ValueError
				else:
					dictTmp[key] = val

		return dictTmp


	def load(self, s):
		self.luaTblDict = self.__load(s)
		print 'load(self, s) -->', self.luaTblDict


	def __dump(self, data):
		assert type(data) is dict
		keys = data.keys()
		s = ""
		if (len(keys)) > 1:
			s += "{";

		for key in keys:
			value = data[key]
			# According to the type of the key, different methods will be used
			# to processing the output result. 
			try:
				i = int(key)
			except:
				s += str(key) + "=" + self.__dump(value) + ","
			else:
				# Determine the value which can be float, int, string, bool, nil
				try:
					# Is the value a float ?
					i = float(value)
				except:
					# The value is not a float.
					if value == "nil" or value == "false" or value == "true":
						s += "" + str(value) + ","	
					else:
						s += "'" + str(value) + "',"
				else:
					# Yes, the value is of type float
					s += "" + str(value) + ","
		s = s[:-1]

		if len(keys) > 1:
			s += "}"
		return s


	def dump(self):
		dictTmp = self.luaTblDict
		return self.__dump(dictTmp)


	def loadLuaTable(self, f):
		s = ''
		with open(f, "rb") as fp:
			line = fp.readline()
			while line:
				s += line
				line = fp.readline()
		self.load(s)


	def dumpLuaTable(self, f):
		s = self.dump()
		if not s and len(s) > 0:
			with open(f, "wb") as fp:
				fp.write(s)


	def __loadList(self, lst):
		assert type(lst) is list
		res = []
		for i in xrange(len(lst)):
			if type(lst[i]) is dict:
				res.append(self.__loadDict(lst[i]))
			elif type(lst[i]) is list:
				res.append(self.__loadList(lst[i]))
			else:
				if lst[i] == False or lst[i] == True:
					res.append({i+1: str(lst[i]).lower()})
				else:
					res.append({i+1: str(lst[i])})

		return self.__xtransfer(res)


	def __loadDict(self, d):
		assert type(d) is dict
		dictTmp = {}
		keys = d.keys()
		for key in keys:
			if type(d[key]) is list:
				dictTmp[key] = self.__loadList(d[key])
			elif type(d[key]) is dict:
				dictTmp[key] = self.__loadDict(d[key])
			else:
				if d[key] == False:
					dictTmp[key] = "false"
				elif d[key] == True:
					dictTmp[key] = "true"
				else:
					dictTmp[key] = {1: str(d[key])}

		return dictTmp


	def loadDict(self, d):
		self.luaTblDict = self.__loadDict(d)
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


	def __dumpDict(self, d):
		dictTmp = {}
		keys = d.keys()

		for key in keys:
			if type(d[key]) is dict:
				dkeys = d[key].keys()
				if len(dkeys) == 1:
					dictTmp[key] = d[key][dkeys[0]]
					continue

				dictTmp[key] = []
				for k in dkeys:
					item = self.__dumpDict({k:d[key][k]})
					if type(k) is int:
						dictTmp[key].append(item[k])
					else:
						dictTmp[key].append(item)
				dictTmp[key] = self.__xtransfer(dictTmp[key])
			else:
				# Firstly, process the special cases like nil, bool
				if d[key] == "nil":
					if type(key) is int:
						dictTmp[key] = None
					continue
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
					try:
						i = int(d[key])
					except ValueError:
						dictTmp[key] = f
					else:
						dictTmp[key] = i
				
		return dictTmp


	def dumpDict(self):
		return self.__dumpDict(self.luaTblDict)


	def update(self, d):
		self.luaTblDict[key] = self.__loadDict(d)


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
			self.luaTblDict[key] = self.__loadList(value)
		elif type(value) is dict:
			self.luaTblDict[key] = self.__loadDict(value)
		else:
			self.luaTblDict[key] = {1: value}


if __name__ == '__main__':
	s = '{array = {65,23,5,{1, 2, 3},hello="world"},dict = {mixed = {43,54.33,false,9,string = {"value", "hello",{11,22,},}},array = {3,6,4},string = "value"}}'
	parser = PyLuaTblParser()
	parser.load(s)
	t = parser.dump()
	pdict = parser.dumpDict()
	print 'pidct: ', pdict
	parser.loadDict(pdict)

	print 'getter parser["array"][1] =', parser["array"][1]
	parser["well"] = ["jk", "eng"]
	parser["array"] = {"name": "xuxinhui", "age": 25, 2:13}
	print 'setter parser["array"] =', parser["array"]
	print parser.dump()
	print parser.dumpDict()