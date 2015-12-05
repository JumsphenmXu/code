#!/usr/bin/python


def __partition(self, s):
		# s = self.__eliminate_whitespace(s)
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
				if i+1 < slen and (s[i+1] == ',' or s[i+1] == '}'):
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


# from PyLuaTblParser import PyLuaTblParser

# def testPyLuaTblParser(luaTblStr):
# 	parser = PyLuaTblParser()
# 	parser.load(luaTblStr)

# 	luaTblDumpedStr = parser.dump()
# 	print 'luaTblDumpedStr =', luaTblDumpedStr

# 	luaTblDumpedDict = parser.dumpDict()
# 	print 'luaTblDumpedDict =', luaTblDumpedDict

# 	parser.loadDict(luaTblDumpedDict)
# 	print 'parser dump after loadDict:', parser.dump()

# 	# set newAttributeList to a list
# 	parser['newAttributeList'] = [10, "I am XU", {"newKey": "newValue"}]

# 	# set newAttributeDict to a dict
# 	parser['newAttributeDict'] = {"DKey1": [{"Dkey2": "DVal2"}, [100, 1000, {"NICE": "GOOD"}], "I am Xin"], "LastName": "HUI"}

# 	print 'luaTblDumpedDict after setting some new features:', parser.dumpDict()
# 	print 'luaTblStr after setting some new features:', parser.dump()

# 	print 'get array attribute in PyLuaTblParser:', parser["array"]


# if __name__ == '__main__':
# 	luaTblStr = '{array = {65,23,5,{1, 2, 3},hello="world"},dict = {mixed = {43,54.33,false,9,string = {"value", "hello",{11,22,},}},array = {3,6,4},string = "value"}}'
# 	testPyLuaTblParser(luaTblStr)
