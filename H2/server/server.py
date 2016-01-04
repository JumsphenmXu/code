#!/usr/bin/python

from cache import *
import socket, select
import os, sys, pickle, json
from conf import conf
from model import model

class CmdError(Exception):
	def  __init__(self, error_msg):
		self.error_msg = error_msg
		raise NotImplementedError(self.error_msg)


class GameServer(object):
	def __init__(self, server_addr=conf.SERVER_ADDR, backlog=5, cache=CacheMgr()):
		self.cache = cache
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind(server_addr)
		self.server.listen(backlog)
		self.inputs = [self.server]
		self.outputs = []
		self.bufsize = 4096


	def register(self, username, password):
		user = model.User(username, password)
		user.save()


	def login(self, username, password):
		user = model.User(username, password)
		fp = open(conf.USER_INFO_DATA, "rb")
		db_cursor = pickle.load(fp)

		if not db_cursor or "user_info" not in db_cursor:
			print '\n[ERROR] login in failed, can not find user with username = %s !!!\n' % username
			return False

		user_info = db_cursor["user_info"]
		if not user_info or user.uid not in user_info.keys():
			print '\n[ERROR] login in failed, can not find user with username = %s !!!\n' % username
			return False

		return True


	def logout(self, username, password, sock):
		user = model.User(username, password)
		user.save()

		if sock in self.inputs:
			self.inputs.remove(sock)
		if sock in self.outputs:
			self.outputs(sock)


	def chatall(self, msg, sock):
		for s in self.outputs:
			if s == self.server or s == sock:
				continue

			self.cache.append_msg(s, msg)


	def exit(self, username, password, sock):
		user = model.User(username, password)
		user.save()

		if sock == self.server:
			return

		if sock in self.inputs:
			self.inputs.remove(sock)
		if sock in self.outputs:
			self.outputs.remove(sock)


	def error(self, error_msg):
		print error_msg


	def cmd_dispatcher(self, data, sock):
		cmddata = data["cmddata"]
		cmdtype = data["cmdtype"] 
		resp = ""
		if cmdtype == conf.CMD_REGISTER:
			print '\nRegister command is executing...'
			self.register(cmddata["username"], cmddata["password"])
			print 'Register command finished!'
			resp = json.dumps({"status": "success"})
		elif cmdtype == conf.CMD_LOGIN:
			print '\nLogin command is executing...'
			flag = self.login(cmddata["username"], cmddata["password"])
			resp = json.dumps({"status": "success"})
			if flag:
				print 'Login command successed !!!'
			else:
				resp = json.dumps({"status": "failed"})
				print 'User (username = %s) failed to login !!!' % cmddata["username"]
		elif cmdtype == conf.CMD_LOGOUT:
			print '\nLogout command is executing...'
			self.logout(cmddata["username"], cmddata["password"], sock)
			print 'Logout command finished'
			resp = json.dumps({"status": "success"})
		elif cmdtype == conf.CMD_CHATALL:
			print '\nChat all command is executing...'
			self.chatall(json.dumps(cmddata), sock)
			print 'Chat all command finished !!!'
			return
			# resp = json.dumps({"status": "success"})
		elif cmdtype == conf.CMD_EXIT:
			print '\nExit command is executing...'
			self.exit(cmddata["username"], cmddata["password"], sock)
			print 'Exit command finished !!!'
			resp = json.dumps({"status": "success"})
		else:
			error_msg = '\n[ERROR] command error ocurred, cmd data ='
			cmddata = data
			self.error(error_msg)
			self.error(cmddata)
			resp = json.dumps({"status": "failed"})
		sock.sendall(resp)



	def run(self):
		print 'server starting.....'
		# For unix we can put sys.stdin in select.select function, while can not on windows.
		# self.inputs.append(sys.stdin)

		while True:
			try:
				read_fds, write_fds, _ = select.select(self.inputs, self.outputs, [])
			except select.error:
				print '\n[ERROR] Failed to execute I/O multiplex by select.select() !!!\n'
				exit(1)

			for sock in read_fds:
				if sock == self.server:
					print '\nAccepting connection.....'
					client, addr = self.server.accept()
					if client not in self.inputs:
						self.inputs.append(client)
					if client not in self.outputs:
						self.outputs.append(client)
				else:
					# read_fds contains the sockets which have incoming data
					data = sock.recv(self.bufsize)
					if data:
						data = json.loads(data)
						self.cmd_dispatcher(data, sock)

					if sock not in self.outputs:
						self.outputs.append(sock)

			for sock in write_fds:
				msg = self.cache.next_msg(sock)
				if msg:
					sock.sendall(msg)
				else:
					self.outputs.remove(sock)


if __name__ == '__main__':
	gs = GameServer()
	gs.run()