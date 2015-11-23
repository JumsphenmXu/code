Author: XU Xinhui
Email: xuxh13@163.com

PyLuaTblParser Documentation
1. You can create a parser by
	parser = PyLuaTblParser()
2. Given a lua table in the form of string, like
	luaTblStr = '{array = {65,23,5,hello="world"},dict = {mixed = {43,54.33,false,9,string = {"value", "hello",}},array = {3,6,4},string = "value"}}' 
3. Load the string-formatted lua table into the parser by
	parser.load(luaTblStr)
4. Dump the inner data of the parser as a string by
	parser.dump()
5. Also you can dump the inner data as a python dict
	parser.dumpDict()
6. You can get/set the inner data structure by using the index operator []
	SETTER:
		parser['newAttributeList'] = [10, "I am XU", {"newKey": "newValue"}]
		parser['newAttributeDict'] = {"DKey1": [{"Dkey2": "DVal2"}, [100, 1000, {"NICE": "GOOD"}], "I am Xin"], "LastName": "HUI"}
	GETTER:
		parser["array"], parser["newAttributeList"]
7. PyLuaTblParser also support load from file
	parser.loadLuaTable(f)
8.	Dump the string-formatted lua table to file
	parser.dumpLuaTable(f)


How to run the test file
	Put PyLuaTblParser.py and test.py in the same directory in your workspace, then for windows
		python test.py
	and for linux, you have two ways to execute this script
		1. python test.py
		2. chmod +x test.py && ./test.py


PS:
	As far by now, the lua table key can only be string, like a=VALUE, abc=VALUE, etc.
	and to my best of knowledge, lua doesn't accept key-value pattern like following format:
		1=VALUE, 
		1.1=VALUE, 
		nil=VALUE, 
		=VALUE
		a<op>b=VALUE, where op in {'*', '.', '#', '*', '/', '%', '+', '-', '?', any other non-alphabetic characters}
	Bugs left for further improving, the string VALUE attributes have some restricts, 
	like the following formats are illegal for the uptodate version of PyLuaTblParser:
		KEY="ajb,ce", where in string value contains comma
		KEY="abj\"dc", KEY='ab\'', where in string value contains quotation mark