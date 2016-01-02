#!/usr/bin/python

from dbmgr import *
import socket
import select
import os, sys, pickle
from conf import conf


class CmdError(Exception):
	def  __init__(self, error_msg):
		self.error_msg = error_msg
		raise NotImplementedError(self.error_msg)


class GameServer(object):
	def __init__(self, server_addr=conf.SERVER_ADDR, backlog=5, dbmgr=DbMgr()):
		self.dbmgr = dbmgr
		self.dbmgr.load_data()
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind(server_addr)
		self.server.listen(backlog)

	def run(self):
		print 'server starting.....'
		self.dbmgr.all_members.append(self.server)
		# For unix we can put sys.stdin in select.select function, while can not on windows.
		# self.dbmgr.all_members.append(sys.stdin)

		while True:
			try:
				inputs, outputs, _ = select.select(self.dbmgr.all_members, self.dbmgr.all_members, [])
			except select.error:
				print '\n[ERROR] Failed to execute I/O multiplex by select.select() !!!\n'
				exit(1)

			for sock in inputs:
				if sock == self.server:
					client, addr = self.server.accept()
				




# def do(cmd, client_addr):
# 	if cmd == conf.CMD_REGISTER:
# 		do_register(client_addr)
# 	elif cmd == conf.CMD_LOGIN:
# 		do_login(client_addr)
# 	elif cmd == conf.CMD_CHAT:
# 		do_chat(client_addr)
# 	elif cmd == conf.CMD_LOGOUT:
# 		do_logout(client_addr)
# 	elif cmd == conf.CMD_EXIT:
# 		do_exit(client_addr)
# 	else:
# 		error_msg = 'Command [%s] not implemented !!!' % cmd
# 		raise CmdError(error_msg) 


# def run():
# 	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	sock.bind(conf.SERVER_ADDR)
# 	sock.listen(5)
# 	while True:
# 		conn, client_addr = sock.accept()
# 		while True:
# 			data = conn.recv(8096)
# 			if data:
# 				data = json.loads(data)
# 				print 'data =', data


if __name__ == '__main__':
	# run()
	gs = GameServer()
	gs.run()