#!/usr/bin/python

import socket, sys, os, inspect, pickle, json
CUR_PATH = os.path.abspath(inspect.getfile(inspect.currentframe()))
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)
from conf import conf

class CacheMgr(object):
	def __init__(self, buf={}):
		self.buf = buf


	def append_msg(self, sock, msg):
		fd = sock.fileno()
		if fd in self.buf:
			self.buf[fd].append(msg)
		else:
			self.buf[fd] = [msg]


	def del_msg_by_idx(self, sock, idx):
		fd = sock.fileno()
		if fd not in self.buf.keys() or len(self.buf[fd]) <= idx:
			return

		del self.buf[fd][idx]


	def del_msg(self, sock, msg):
		fd = sock.fileno()
		if fd not in self.buf.keys() or msg not in self.buf[fd]:
			return
		self.buf[fd].remove(msg)


	def get_msg_by_idx(self, sock, idx):
		fd = sock.fileno()
		if fd not in self.buf.keys() or len(self.buf[fd]) <= idx:
			return None

		return self.buf[fd][idx]


	def next_msg(self, sock):
		fd = sock.fileno()
		if fd not in self.buf.keys() or len(self.buf[fd]) < 1:
			return None

		msg = self.buf[fd][0]
		self.del_msg_by_idx(sock, 0)
		return msg