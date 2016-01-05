#!/usr/bin/python

import socket
import select
import os, sys, pickle, json, signal

import inspect
CUR_PATH = os.path.abspath(inspect.getfile(inspect.currentframe()))
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)

from conf import conf
from model import model

class Client(object):
	def __init__(self, user=None, sock=None, islogin=False):
		self.user = user
		self.sock = sock
		self.islogin = islogin
		if self.sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect(conf.SERVER_ADDR)
		if self.sock is not None:
			self.sock.settimeout(1)


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
		self.islogin = True
		self.register_login_helper(conf.CMD_LOGIN)


	def chatall(self):
		info = '\t    ' + self.user.username + ' says: '
		msg = raw_input(info)
		cmddata = {"msg": msg, "username": self.user.username}
		serailizedStr = json.dumps({"cmdtype": conf.CMD_CHATALL, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)


	def logout(self):
		self.islogin = False
		cmddata = {"username": self.user.username, "password": self.user.password}
		serailizedStr = json.dumps({"cmdtype": conf.CMD_LOGOUT, "cmddata": cmddata})
		self.sock.sendall(serailizedStr)
		while True:
			online_time_msg = ""
			data = self.sock.recv(4096)
			if data:
				try:
					data = json.loads(data)
				except ValueError:
					data = None
				if data and "total_online_time" in data.keys():
					online_time_msg += '\n\t  Your accumulated online time is: ' + str(data["total_online_time"]) + " secs."
				if data and "online_time" in data.keys():
					online_time_msg += "\n\t  This time you spent " + str(data["online_time"]) + " secs online."
				online_time_msg += "\n\t  Bye !!!"
				print online_time_msg
				break

		self.run()


	def exit(self):
		self.islogin = False
		exit(0)


	def help(self):
		print '\t  Usage description'
		print '\t  --Use COMMAND [register] to sign up if you are not ever registered'
		print '\t  --Use COMMAND [login] to sign in with the account you registered'
		print '\t  --Use COMMAND [logout] to leave the system if you had just login'
		print '\t  --Use COMMAND [chat] to send messages to all online users'
		print '\t  --Use COMMAND [chkmsg] to check the incoming message box'
		print '\t  --Use COMMAND [exit] to close the system\n'


	def illegalcmd(self, cmd):
		print '\n\t  [ERROR] command (%s) is illegal !!!\n' % cmd
		self.help()


	def get_response(self):
		data = None
		try:
			data = self.sock.recv(4096)
		except (socket.timeout, socket.error):
			pass

		if data:
			data = json.loads(data)

		return data


	def display_chat_msg(self, segs):
		for msg in segs:
			if len(msg) < 1:
				continue

			msgpiece = None
			try:
				msgpiece = json.loads(msg)
			except ValueError:
				pass

			if msgpiece and "msg" in msgpiece.keys() and "username" in msgpiece.keys():
				info = '\t    ' + msgpiece["username"] + ' said: ' + msgpiece["msg"]
				print info


	def run(self):
		print '\n\n\t\tWelcome to xGameCenter !!!\n'
		print '\t1. Register your account please press $register'
		print '\t2. Login please press $login'
		print '\t3. Chatting to all please press $chat'
		print '\t4. Check incoming messages please press $chkmsg'
		print '\t5. Logout please press $logout'
		print '\t6. Exit please press $exit'
		print '\t7. Print help messages please press $help'
		while True:
			while self.islogin:
				resp = None
				try:
					resp = self.sock.recv(4096)
					if resp:
						# print '\t  resp = ', resp
						segs = resp.split("#")
						# print '\t  segs = ', segs
						self.display_chat_msg(segs)
						# resp = json.loads(resp)
					break
				except (socket.timeout, socket.error):
					break

				# if resp and "msg" in resp.keys() and "username" in resp.keys():
				# 	info = '\t    ' + resp["username"] + ' said: ' + resp["msg"]
				# 	print info

			cmd = raw_input('\t  $').strip()
			if cmd == "help":
				self.help()
			elif cmd == 'register':
				self.register()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Register successed, and you can now login.')
				else:
					print('\t  Register failed, please try again.')
			elif cmd == 'login':
				self.login()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Login successed, and you can now chat/logout/exit.')
				else:
					print('\t  Login failed, please try again.')
			elif cmd == 'chat':
				self.chatall()
			elif cmd == 'chkmsg':
				continue
			elif cmd == 'logout':
				self.logout()
				resp = self.get_response()
				if resp and resp["status"] == 'success':
					print('\t  Logout successed, and you can now login/exit.')
				else:
					print('\t  Logout failed, please try again.')
			elif cmd == 'exit':
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