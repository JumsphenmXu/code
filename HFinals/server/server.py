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
import SocketServer


class GameServerHandler(SocketServer.BaseRequestHandler):

	def login(self, cmd_params):
		username = cmd_params['username']
		password = cmd_params['password']
		user = User(username, password)

		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		return DBConnection.is_user_existed(cursor, user.get_uid(), username, password)

	def register(self, cmd_params):
		username = cmd_params['username']
		password = cmd_params['password']
		user = User(username, password)

		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		if DBConnection.is_user_existed(cursor, user.get_uid(), username, password):
			print 'User %s has already been register, you can login directly.' % (username)
			return True

		data = {}
		data['username'] = username
		data['password'] = password
		cursor[uid] = data
		dbconn.write_back(cursor)
		print 'User %s registers successfully.'
		return True

	def cmd_dispatch(self, cmd):
		cmd_type = cmd['type']
		cmd_params = cmd['params']
		msg = None
		if cmd_type == 'LOGIN':
			msg = self.login(cmd_params)
		elif cmd_type == 'REGISTER':
			msg = self.register(cmd_params)

		return msg

	def handle(self):
		print 'handle......'
		data = self.request.recv(1024)
		print 'DATA recived:', data
		cmd = json.loads(data)
		print 'CMD recived:', cmd
		error = not self.cmd_dispatch(cmd)
		self.request.sendall(json.dumps({'error': error}))


class GameServer():
	def __init__(self, host, port):
		self.server = SocketServer.TCPServer((host, port), GameServerHandler)

	def run(self):
		self.server.serve_forever()


if __name__ == '__main__':
	server = GameServer(conf.SERVER_IP, conf.SERVER_PORT)
	server.run()