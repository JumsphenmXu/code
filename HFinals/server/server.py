#!/usr/bin/python
#
import inspect, sys, os, json
CUR_PATH = os.path.abspath(inspect.getfile((inspect.currentframe())))
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)

from conf import conf
from model.user import User
from util.dbconnection import DBConnection
from util.util import TYPE, CMD
import SocketServer


class GameServerHandler(SocketServer.BaseRequestHandler):
	# escape message if necessary
	def __escape_msg(self, s, ch):
		if not s or not isinstance(s, str) or len(s) == 0:
			return s

		t = ''
		for c in s:
			if c == ch:
				t += '\\'
			t += c

		return t

	# reply_info must be a list whose element is a 3-tuple of (key, value, type)
	# where type can be BOOLEAN, STRING, INT, FLOAT
	def pack_message(self, reply_info):
		msg = ''
		for ele in reply_info:
			s = ele[0] + '#' + str(ele[1]) + '#' + ele[2]
			if len(msg) > 0:
				msg += '$'
			msg += s

		return msg

	# login handler
	def login(self, cmd_params):
		username = cmd_params['username']
		password = cmd_params['password']
		user = User(username, password)

		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		return DBConnection.is_user_existed(cursor, user.get_uid(), username, password)

	# register handler
	def register(self, cmd_params):
		username = cmd_params['username']
		password = cmd_params['password']
		user = User(username, password)
		uid = user.get_uid()

		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		if DBConnection.is_user_existed(cursor, uid, username, password):
			print 'User %s has already been register, you can login directly.' % (username)
			return True

		if not cursor:
			cursor = {}

		data = {}
		data['username'] = username
		data['password'] = password
		cursor[uid] = data
		dbconn.write_back(cursor)
		print 'User %s registers successfully.'
		return True

	def require_level_info(self):
		pass

	def spawn_enemy(self):
		pass

	# command dispatcher
	def cmd_dispatch(self, cmd):
		cmd_type = cmd['type']
		cmd_params = cmd['params']
		msg = None

		if cmd_type == CMD.LOGIN:
			msg = self.login(cmd_params)
		elif cmd_type == CMD.REGISTER:
			msg = self.register(cmd_params)
		elif cmd_type = CMD.REQUIRE_LEVEL_INFO:
			msg = self.require_level_info()
		elif cmd_type = CMD.SPAWN_ENEMY:
			self.spawn_enemy()

		return msg

	def handle(self):
		print 'handle......'
		data = self.request.recv(4096)
		print 'DATA RECIVED:', data
		cmd = json.loads(data)
		print 'CMD RECIVED:', cmd
		error = not self.cmd_dispatch(cmd)
		reply_info = [('error', error, TYPE.BOOLEAN)]
		msg = self.pack_message(reply_info)
		print 'REPLY MESSAGE:', msg
		self.request.sendall(msg)


class GameServer():
	def __init__(self, host, port):
		self.server = SocketServer.TCPServer((host, port), GameServerHandler)

	def run(self):
		self.server.serve_forever()


if __name__ == '__main__':
	server = GameServer(conf.SERVER_IP, conf.SERVER_PORT)
	server.run()