#!/usr/bin/python

import socket, sys, os, inspect, pickle
CUR_PATH = inspect.getfile(inspect.currentframe())
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)
from conf import conf


def justifyInfo(info, alphanum=True):
	if alphanum:
		for i in xrange(len(info)):
			if 'a' <= info[i] <= 'z' or 'A' <= info[i] <= 'Z' or '0' <= info[i] <= '9' or info[i] == '_':
				continue
			else:
				print '\t    Only alphanumeric or underscore is allowed, please try again.'
				return False
	return True

def register():
	while True:
		username = raw_input('\t    Username:')
		password = raw_input('\t    Password:')
		if len(username) < 1:
			print '\t    Username can not be empty, please try again.'
			continue
		if len(username) < 1:
			print '\t    Password can not be empty, please try again.'
			continue

		if not justifyInfo(username):
			continue
		data = {username: username, password: password}
		cmdType = conf.CMD_REGISTER
		cmdData = data
		serailizedStr = json.dumps({cmdType: cmdType, cmdData: cmdData})
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(conf.SERVER_ADDR)
		sock.sendall(serailizedStr)
		break
		

def login():
	while True:
		username = raw_input('\t    Username:')
		password = raw_input('\t    Password:')
		if len(username) < 1:
			print '\t    Username can not be empty, please try again.'
			continue
		if len(username) < 1:
			print '\t    Password can not be empty, please try again.'
			continue
		data = {username: username, password: password}
		cmdType = conf.CMD_LOGIN
		cmdData = data
		serailizedStr = json.dumps({cmdType: cmdType, cmdData: cmdData})
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(conf.SERVER_ADDR)
		sock.sendall(serailizedStr)
		break


def chat():
	pass

def logout():
	pass

def illegalCmd(cmd):
	print 'No command [%s] found, please check the instruction.' % cmd

def facade():
	print '\n\n\t\tWelcome to xGameCenter !!!\n'
	print '\t1. Register your account please press $R'
	print '\t2. Login please press $L'
	print '\t3. Chatting please press $C'
	print '\t4. Logout please press $T'
	print '\t5. Exit please press $E'
	while True:
		cmd = raw_input('\t  $')
		if cmd == 'R':
			register()
		elif cmd == 'L':
			login()
		elif cmd == 'C':
			chat()
		elif cmd == 'T':
			logout()
		elif cmd == 'E':
			exit()
		else:
			illegalCmd(cmd)


if __name__ == '__main__':
	# facade()
	import pickle
	lst = [1, 2, 3]
	dct = {'hello': 'world', 'nice': 'good'}
	fp = open('data.pkl', 'wb')
	pickle.dump(lst, fp, -1)
	pickle.dump(dct, fp)
	fp.close()

	print '#1:', lst
	print '#1:', dct

	fo = open('data.pkl', 'rb')
	dat1 = pickle.load(fo)
	dat2 = pickle.load(fo)
	fo.close()

	print '#2:', dat1
	print '#2:', dat2

	print PROJECT_PATH