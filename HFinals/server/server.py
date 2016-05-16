#!/usr/bin/python
#
import inspect, sys, os, json
CUR_PATH = os.path.abspath(inspect.getfile((inspect.currentframe())))
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)

from conf import conf
from model import user
from util import dbconnection
import SocketServer


class GameServerHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		print 'handle......'
		res = self.request.recv(1024)
		print res
		return res


class GameServer():
	def __init__(self, host, port):
		self.server = SocketServer.TCPServer((host, port), GameServerHandler)

	def run(self):
		self.server.serve_forever()


if __name__ == '__main__':
	server = GameServer(conf.SERVER_IP, conf.SERVER_PORT)
	server.run()