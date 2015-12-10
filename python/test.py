from PyLuaTblParser import PyLuaTblParser

# if __name__ == '__main__':
	# s = '{"hello",key="value", {"in\a\b", 3, 4, [1.23]=56, nil, --yye    \n{mixed="inin", nice={0,9,\a\b8}}}, 1, 2} --hello'
	# s = '{array = {65,23,5,{1, 2, 3},["a"]=nil, nil, {{}}, [1]=678, ["yada,had"]="nice", hello="worl,[]\\\"ddefj"},dict = {mixed = {43,54.33,false,9,string = {"value]", "hello",{11,22,}}},array = {3,6,4},string = "value"}}'
	# s = '{{{}},{1, 2, 3,}, hello="world"}, "hh"'
	# s = '"hello"'
	# s = "{['array']={65,23,5,{1,2,3},{{11,22,33}},{{}},[1]=78,['yada,had']='nice',['hello']='worl,[]\"ddefj'},['dict']={['mixed']={43,54.33,9,['string']={'value]','hello',{11,22}}},['array']={3,6,4},['string']='value'}}"
	# s = '{{1, 2}, {{{{}}}}}'
	# s = '{hello="world"; {hhh=2, [4]=1},{{}}, hel=1,nil, false, true,s 2, .123, "#, 0xea, \t\r\n\\\\,k"}'
	# s = '{1, 2, array={2, 3, 4, "hi"}}'
	# s = '{{{{1, 2, 3}, 4}}}'
	# s = '{["hel\\\'\\\'\\\'\\\'\\\'l"]=1}'
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
	# s = '{{[1] = "nil", nil, nil, [3] = 34, {},--[[yy]]--[===[kk]===][6] --[=[tt--[[ddd]]]=]= --[[dd]]nil, io --[[oo]]= 90,--[[name]]-.23}}'
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
	# s = '{[\'u\\\'root\\\'\'] = {5,4,6},1,6,7,string = \'value\',}'
	# s = '{array = \'abc\\\"bca!@#$%^&*()+_| \',1,4,\'d\'}'
	# s = '{var={"val", {["key"]="val"},}, {}, [11]=-1, var, arb, }'
	# s = '{{[1] = "nil", nil, nil, [3] = 34, {},[6] = nil, io = 90}}'
	# s = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
	# s = '{5,6,8,{},nil,{nil,nil},[\'root\'] = 5}'
	# s = '{{{}}}'
	# s = '{{[1] = "nil", nil, nil, [3] = 34, {},[6] = nil, io = 90}}'
	# s = '{var={var="\\a"}}'
	# s = '{var={"\\a\\vb ", --hafd [1]=3, jkd="worl\\\\d", \a\b\t\r, \nvar="\\a\\d\\f\\flag"}, "jakfajfdka", 1.234, -.34, -2e2\n\\\n}'
	# s = "{{['\\\\'] = {1,2,3,\"\\\'\'\", \n\r\t\b\a\fstring = '\\\'value'},},}"
	# s = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
	# parser = PyLuaTblParser()

	# print 'SOURCE s =', s
	# parser.load(s)
	# print '#1 luaLst:', parser.luaLst

	# s = parser.dump()
	# print '#2 luaStr:', parser.luaStr

	# d = parser.dumpDict()
	# print '#3 luaDct:', d

	# parser.loadDict(d)
	# print '#4 loadDict luaLst:', parser.luaLst

	# s = parser.dump()
	# print '#5 luaStr:', s

	# parser.load(s)
	# print '#6 luaLst', parser.luaLst
	# d = parser.dumpDict()
	# print '#7 luaDct', d

	# s = parser.dump()
	# print '#8 luaStr', s
	# parser.load(s)


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
	({1:1},'{[--[==[comment]=]==]1]=1}'),
	({1:{'\\':{1:1,2:2,3:3,4:"\''", 'string':'\'value'}}}, "{{['\\\\'] = {1,2,3,\"\\\'\'\", \n\r\t\b\a\fstring = '\\\'value'},},}")
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
		t = test_cases[i]
		test(i,t[0],t[1])


if __name__ == '__main__':
	main()