#!/usr/bin/python

import socket, sys, os, inspect, pickle, json
CUR_PATH = inspect.getfile(inspect.currentframe())
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)
from conf import conf

class CmdError(Exception):
	def  __init__(self, error_msg):
		self.error_msg = error_msg
		raise NotImplementedError(self.error_msg)

def do(cmd, client_addr):
	if cmd == conf.CMD_REGISTER:
		do_register(client_addr)
	elif cmd == conf.CMD_LOGIN:
		do_login(client_addr)
	elif cmd == conf.CMD_CHAT:
		do_chat(client_addr)
	elif cmd == conf.CMD_LOGOUT:
		do_logout(client_addr)
	elif cmd == conf.CMD_EXIT:
		do_exit(client_addr)
	else:
		error_msg = 'Command [%s] not implemented !!!' % cmd
		raise CmdError(error_msg) 


def run():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(conf.SERVER_ADDR)
	sock.listen(5)
	while True:
		conn, client_addr = sock.accept()
		while True:
			data = conn.recv(8096)
			if data:
				data = json.loads(data)
				print 'data =', data

if __name__ == '__main__':
	run()