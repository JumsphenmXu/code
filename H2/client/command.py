#!/usr/bin/python

import socket, sys, os, inspect, pickle
CUR_PATH = inspect.getfile(inspect.currentframe())
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)
from conf import conf


class Command(object):
	"""
	COMMAND LIST
		*Register(R): register an account.
		*LogIn(LI): login game center.
		*LogOut(LO): logout game center.
		*Exit(E): exit the game client.
		*ChatAll(CA): send a message to all clients.
		*ChatGrp gid(CG): send a message to group which identified by group id gid.
		*CreaTeGrp(CTG): create a group
	"""
	cmd_list = ['R', 'LI', 'LO', 'E', 'CA', 'CG', 'CTG']

	def __init__(self, csocket=None, cmd=None):
		self.csocket = socket
		self.cmd = cmd


	def __register(self, username, password):
		serailizedStr = json.dumps({cmdtype: 'R', username: username, password: password})
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(conf.SERVER_ADDR)
		sock.sendall(serailizedStr)


	def __login(self, username, password):
		serailizedStr = json.dumps({cmdtype:'LI', username: username, password: password})
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(conf.SERVER_ADDR)
		sock.sendall(serailizedStr)


	def __logout(self):
		pass


	def __exit(self):
		exit(0)

	def __chatall(self, message):
