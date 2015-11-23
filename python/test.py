#!/usr/bin/python

from PyLuaTblParser import PyLuaTblParser

def testPyLuaTblParser(luaTblStr):
	parser = PyLuaTblParser()
	parser.load(luaTblStr)

	luaTblDumpedStr = parser.dump()
	print 'luaTblDumpedStr =', luaTblDumpedStr

	luaTblDumpedDict = parser.dumpDict()
	print 'luaTblDumpedDict =', luaTblDumpedDict

	parser.loadDict(luaTblDumpedDict)
	print 'parser dump after loadDict:', parser.dump()

	# set newAttributeList to a list
	parser['newAttributeList'] = [10, "I am XU", {"newKey": "newValue"}]

	# set newAttributeDict to a dict
	parser['newAttributeDict'] = {"DKey1": [{"Dkey2": "DVal2"}, [100, 1000, {"NICE": "GOOD"}], "I am Xin"], "LastName": "HUI"}

	print 'luaTblDumpedDict after setting some new features:', parser.dumpDict()
	print 'luaTblStr after setting some new features:', parser.dump()

	print 'get array attribute in PyLuaTblParser:', parser["array"]


if __name__ == '__main__':
	luaTblStr = '{array = {65,23,5,{1, 2, 3},hello="world"},dict = {mixed = {43,54.33,false,9,string = {"value", "hello",{11,22,},}},array = {3,6,4},string = "value"}}'
	testPyLuaTblParser(luaTblStr)
