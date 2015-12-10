from PyLuaTblParser import PyLuaTblParser

test_cases = [
	({'array':[65,23,5],'dict':{'mixed':{1:43,2:54.33,3:False,4:9,'string':"value"},'array':[3,6,4],'string':"value"}},
		'{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'),
	({},'{}'),
	({'u\'root\'':[5,4,6],1:1,2:6,3:7,'string':"value"},'{[\'u\\\'root\\\'\'] = {5,4,6},1,6,7,string = \'value\',}'),
	({1:5,2:6,3:8,4:{},6:[None,None],'root':5},'{5,6,8,{},nil,{nil,nil},[\'root\'] = 5}'),
	({1:{1:'nil',3:{},'io':90}},'{{[1] = "nil", nil, nil, [3] = 34, {},[6] = nil, io = 90}}'),
	({0.66:16}, '{[0.66] = 16}'),
	({},'{nil}'),
	({1:{},2:{}}, '{{},{}}'),
	({'array':321}, '{array = 123, array = 321}'),
	({1:[1.123,-415,-64.13],2:{},"root" : 123}, "{{1.123,-415,-64.13},{},root=123}"),
	({1:[112.3,-415.0,-64.13],2:{},"root":123},"{{11.23e+1,-4.15e2,-6413e-2},{},root=123}"),
	({1:12312,2:51290018,3:12341,4:255},"{ 12312, 51290018, 12341, 0xff}"),
	({1:123, 2: 5413, 3:{'array':[3,2,1], 1:321}},'{123,-- {\"luthor kill 5 superman\" = 123},\n 5413,{array = {3,2,1},321},}'),
	({'array':'abc\"bca!@#$%^&*()+_| ',1:1,2:4,3:'d'},'{array = \'abc\\\"bca!@#$%^&*()+_| \',1,4,\'d\'}'),
	({'array':'abc\'bca!@#$%^&*()+_| ',1:1,2:4,3:'d'},'{array = \"abc\\\'bca!@#$%^&*()+_| \",1,4,\'d\'}'),
	({'seperate name test':123, 'seperate name 2':{'seperate name 3' : 321} }, '{[\'seperate name test\']=123, [\"seperate name 2\"]= {[\'seperate name 3\'] = 321},}'),
	({1:'one',2:'hh',3:'d',4:'c','d': 'two'},"{\"one\",[\'d\']=\"two\",[3]=\"three\",\"hh\",[1]=\"y\",\"d\",\"c\"}"),
	({'a':1, 1:{'object with 1 member':['array with 1 element']}, 2:'test'},'{a = 1,{["object with 1 member"] = {"array with 1 element",},},"test"}'),
	({1:1},'{[--[==[comment]=]==]1]=1}')
	]

def test(i,d,s):
	a1 = PyLuaTblParser()
	a2 = PyLuaTblParser()
	a3 = PyLuaTblParser()

	a1.load(s)
	d1 = a1.dumpDict() 
	a2.loadDict(d1)
	d2 = a2.dumpDict()

	file_path = 'dict'
	a2.dumpLuaTable(file_path)
	a3.loadLuaTable(file_path)

	d3 = a3.dumpDict()
	if((str(d) == str(d1)) and (str(d1) == str(d2)) and (str(d2) == str(d3))):
		print('case ' + str(i) + ':Ok!')
	else:
		print('case ' + str(i) + ':Failed!')
		print('\td :' + str(d))
		print('\td1:' + str(d1))
		print('\td2:' + str(d2))
		print('\td3:' + str(d3))

def main():
	print(str(len(test_cases)) + ' tests in all')
	for i in range(len(test_cases)):
	#i = 4
		t = test_cases[i]
		test(i,t[0],t[1])

main()