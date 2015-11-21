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
					parts.append(t[start:i+1])
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
				parts.append(t[start: i])
				start = i + 1
				leftBracketsCnt = 0
				rightBracketsCnt = 0
		# end of for loop
		return parts

	# STAGE 2: after the STAGE 1, we get items to do further determination,
	# 	namely, we validate the item type (numeric, bool, nil, array, dict, string etc.),
	#	and pick out the invalid items and raise ValueError to notify the caller.
	def __itemParse(self, s):
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
		t = t.strip()
		if len(t) == 0:
			return None, PyLuaTblParser.KLASS_OTHERS

		res = None

		# if we have PATTERN like {member1, member2, member3, ..., membern},
		# we parse it as a list.
		if len(t) != len(s):
			res = []
			resTmp = self.__partition(t)
			for item in resTmp:
				res.append(self.__itemParse(item))
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
			if t == "false" or t == "nil":
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

			if leftPart == "nil" or len(leftPart) == 0:
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
		print self.luaTblDict

	def dump(self):
		pass

	def loadLuaTable(self, f):
		pass

	def dumpLuaTable(self, f):
		pass

	def loadDict(self, d):
		pass

	def dumpDict(self):
		pass


if __name__ == '__main__':
	# s = '{nil, array = {65,23,5},dict = {mixed = {43,54.33,false,9,string = "value"},array = {3,6,4},string = "value"}}'
	s = "{a=1, e = {1, 2, 3, 4, a = {1, 2, 3, c='====', nil, false}}}"
	parser = PyLuaTblParser()
	parser.load(s)
	# print parser._PyLuaTblParser__partition(t)