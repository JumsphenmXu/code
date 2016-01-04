#!/usr/bin/python

import socket
import select
import os, sys, pickle, json

import inspect
CUR_PATH = os.path.abspath(inspect.getfile(inspect.currentframe()))
print 'CUR_PATH =', CUR_PATH
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
print 'PROJECT_PATH =', PROJECT_PATH
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)

from conf import conf
from model import model


class Client(object):
	def __init__(self, user=None, sock=None, ischat=False):
		self.user = user
		self.sock = sock
		self.ischat = ischat
		if self.sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect(conf.SERVER_ADDR)


	def register_login_helper(self, cmdtype):
		self.ischat = False
		username = raw_input('\t    Username:')
		password = raw_input('\t    Password:')
		self.user = model.User(username, password)

		cmddata = {"username": username, "password": password}
		serailizedStr = json.dumps({"cmdtype": cmdtype, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)
		

	def register(self):
		self.register_login_helper(conf.CMD_REGISTER)


	def login(self):
		self.register_login_helper(conf.CMD_LOGIN)


	def chatall(self):
		self.ischat = True
		info = '\t    ' + self.user.username + '$'
		msg = raw_input(info)
		cmddata = {"msg": msg, "username": self.user.username}
		serailizedStr = json.dumps({"cmdtype": conf.CMD_CHATALL, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)


	def logout(self):
		self.ischat = False
		cmddata = {"username": self.user.username, "password": self.user.password}
		serailizedStr = json.dumps({"cmdtype": conf.CMD_LOGOUT, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)
		self.run()


	def exit(self):
		self.ischat = False
		exit(0)


	def illegalcmd(self, cmd):
		self.ischat = False
		print '\n\t  [ERROR] command (%s) is illegal !!!\n' % cmd


	def get_response(self):
		data = None
		try:
			data = self.sock.recv(4096)
		except socket.error:
			pass

		if data:
			data = json.loads(data)

		return data


	def run(self):
		print '\n\n\t\tWelcome to xGameCenter !!!\n'
		print '\t1. Register your account please press $R'
		print '\t2. Login please press $LI'
		print '\t3. Chatting to all please press $CA'
		print '\t4. Logout please press $LO'
		print '\t5. Exit please press $E'
		while True:
			if self.ischat:
				resp = None
				self.sock.settimeout(1)
				try:
					resp = self.sock.recv(4096)
				except socket.timeout:
					pass
				else:
					if resp and "msg" in resp:
						msg = "\t  " + resp["username"] + "$" + resp["msg"]
						print msg

			cmd = raw_input('\t  $')
			if cmd == 'R':
				self.register()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Register successed, and you can now login.')
				else:
					print('\t  Register failed, please try again.')
			elif cmd == 'LI':
				self.login()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Login successed, and you can now chat/logout/exit.')
				else:
					print('\t  Login failed, please try again.')
			elif cmd == 'CA':
				self.chatall()
				# resp = self.get_response()
				# if resp and resp["status"] == 'success':
				# 	print('\t  Chatting successed.')
				# else:
				# 	print('\t  Chatting failed, please try again.')
			elif cmd == 'LO':
				self.logout()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Logout successed, and you can now login/exit.')
				else:
					print('\t  Logout failed, please try again.')
			elif cmd == 'E':
				self.exit()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Exit successed.')
				else:
					print('\t  Exit failed, please try again.')
			else:
				self.illegalcmd(cmd)


if __name__ == '__main__':
	client = Client()
	client.run()