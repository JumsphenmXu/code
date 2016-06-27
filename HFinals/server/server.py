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
from util.util import TYPE, CMD, Util
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
		username = cmd_params['username']['value']
		password = cmd_params['password']['value']
		print 'username:', username
		print 'password:', password
		user = User(username, password)

		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		print 'login cursor:', cursor
		error = not DBConnection.is_user_existed(cursor, user)

		return [('error', error, TYPE.BOOLEAN)]

	# register handler
	def register(self, cmd_params):
		username = cmd_params['username']['value']
		password = cmd_params['password']['value']
		user = User(username, password)
		uid = user.get_uid()

		error = False
		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		if DBConnection.is_user_existed(cursor, user):
			print 'User %s has already been register, you can login directly.' % (username)

		user.save()
		print 'User %s registers successfully.'
		return [('error', error, TYPE.BOOLEAN)]

	def require_level_info(self, cmd_params):
		level = int(cmd_params['level']['value'])
		level_info = Util.get_game_level_info()
		keys = level_info.keys()

		exp = conf.INFINITY_EXP
		error = False
		if 'max_level' in keys and level > level_info['max_level']:
			error = True

		if 'levels' in keys:
			experience = level_info['levels'][level-1]

		reply_info = [('error', error, TYPE.BOOLEAN), ('experience', experience, TYPE.INT)]
		return reply_info

	def require_user_info(self, cmd_params):
		username = cmd_params['username']['value']
		password = cmd_params['password']['value']
		user_info = Util.get_game_user_info(username, password)

		error = False
		if user_info is None:
			error = True

		print 'require_user_info:', user_info
		level = 1 if error else user_info['level']
		health = 0 if error else user_info['health']
		experience = 0 if error else user_info['experience']

		reply_info = [('error', error, TYPE.BOOLEAN)]
		reply_info.append(('level', level, TYPE.INT))
		reply_info.append(('health', health, TYPE.INT))
		reply_info.append(('experience', experience, TYPE.INT))

		return reply_info

	def save_user_info(self, cmd_params):
		username = cmd_params['username']['value']
		password = cmd_params['password']['value']
		experience = cmd_params['experience']['value']
		level = cmd_params['level']['value']

		user = User(username, password)
		dbconn = DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()
		uid = user.get_uid()

		user_info = None
		if uid in cursor.keys():
			user_info = cursor[uid]

		if not user_info:
			user_info = user.pack_user_info()
		
		user_info['experience'] = experience
		user_info['level'] = level
		cursor[uid] = user_info
		dbconn.write_back(cursor)

		reply_info = [('error', False, TYPE.BOOLEAN)]
		return reply_info

	def spawn_enemy(self, cmd_params):
		return [('error', False, TYPE.BOOLEAN)]

	# command dispatcher
	def cmd_dispatch(self, cmd):
		cmd_type = cmd['type']
		cmd_params = cmd['params']
		msg = None

		if cmd_type == CMD.LOGIN:
			msg = self.login(cmd_params)
		elif cmd_type == CMD.REGISTER:
			msg = self.register(cmd_params)
		elif cmd_type == CMD.REQUIRE_LEVEL_INFO:
			msg = self.require_level_info(cmd_params)
		elif cmd_type == CMD.REQUIRE_USER_INFO:
			msg = self.require_user_info(cmd_params)
		elif cmd_type == CMD.SAVE_USER_INFO:
			msg = self.save_user_info(cmd_params)
		elif cmd_type == CMD.SPAWN_ENEMY:
			msg = self.spawn_enemy(cmd_params)

		return msg

	def handle(self):
		print 'handle......'
		data = self.request.recv(4096)
		print 'DATA RECIVED:', data
		cmd = json.loads(data)
		print 'CMD RECIVED:', cmd
		reply_info = self.cmd_dispatch(cmd)

		msg = self.pack_message(reply_info)
		print 'REPLY MESSAGE:', msg
		self.request.sendall(msg)


class GameServer():
	def __init__(self, host, port):
		self.server = SocketServer.TCPServer((host, port), GameServerHandler)

	def run(self):
		self.server.serve_forever()


if __name__ == '__main__':
	# dbconn = DBConnection(conf.DB_USER)
	# dbconn.clear()
	Util.init_game_level()
	server = GameServer(conf.SERVER_IP, conf.SERVER_PORT)
	server.run()