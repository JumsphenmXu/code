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
	def __init__(self, user=None, sock=None):
		self.user = user
		self.sock = sock
		if self.sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect(conf.SERVER_ADDR)


	def register_login_helper(self, cmdtype):
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
		info = '\t    ' + self.user.username + '$'
		msg = raw_input(info)
		cmddata = {"msg": msg}
		serailizedStr = json.dumps({"cmdtype": conf.CMD_CHATALL, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)


	def logout(self):
		cmddata = {"username": self.user.username, "password": self.user.password}
		serailizedStr = json.dumps({"cmdtype": conf.CMD_LOGOUT, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)
		self.run()


	def exit(self):
		exit(0)


	def illegalcmd(self, cmd):
		print '\n[ERROR] command (%s) is illegal !!!\n' % cmd


	def run(self):
		print '\n\n\t\tWelcome to xGameCenter !!!\n'
		print '\t1. Register your account please press $R'
		print '\t2. Login please press $LI'
		print '\t3. Chatting to all please press $CA'
		print '\t4. Logout please press $LO'
		print '\t5. Exit please press $E'
		while True:
			cmd = raw_input('\t  $')
			if cmd == 'R':
				self.register()
			elif cmd == 'LI':
				self.login()
			elif cmd == 'CA':
				self.chatall()
			elif cmd == 'LO':
				self.logout()
			elif cmd == 'E':
				self.exit()
			else:
				self.illegalcmd(cmd)


if __name__ == '__main__':
	client = Client()
	client.run()