#!/usr/bin/python

from conf import conf
import time, pickle

class User(object):
	def __init__(self, username, password, total_online_time=0.0, last_login_time=time.time()):
		self.username = username
		self.password = password
		self.total_online_time = total_online_time
		self.last_login_time = last_login_time
		self.uid = self.generate_uid(username, password)


	def str_hash(self, s):
		if not s or len(s) == 0:
			return 0

		res = 1
		for i in xrange(len(s)):
			res = (res << i) * ord(s[i])
		return res


	def generate_uid(self, username, password):
		return self.str_hash(username) ^ self.str_hash(password)


	def get_total_online_time(self):
		db_cursor = self.get_user_info_history()
		user_info = db_cursor["user_info"]
		res = 0.0
		if user_info and "total_online_time" in user_info[self.uid].keys():
			res += user_info[self.uid]["total_online_time"]

		res += time.time() - self.last_login_time
		return res


	def calc_online_time(self):
		return time.time() - self.last_login_time


	def get_user_info_history(self):
		db_cursor = None
		fp = open(conf.USER_INFO_DATA, "rb")
		try:
			db_cursor = pickle.load(fp)
		except:
			pass
		fp.close()

		user_info = None
		if db_cursor and "user_info" in db_cursor.keys():
			user_info = db_cursor["user_info"]
		elif not db_cursor:
			db_cursor = {}
			db_cursor["user_info"] = {}
		elif "user_info" not in db_cursor.keys():
			db_cursor["user_info"] = {}

		return db_cursor


	def save(self):
		self.total_online_time += time.time() - self.last_login_time
		
		db_cursor = self.get_user_info_history()
		user_info = db_cursor["user_info"]
		if self.uid not in user_info.keys():
			user_info[self.uid] = {}
			user_info[self.uid]["total_online_time"] = 0.0

		user_info[self.uid]["username"] = self.username
		user_info[self.uid]["password"] = self.password
		user_info[self.uid]["total_online_time"] += self.total_online_time
		user_info[self.uid]["last_login_time"] = self.last_login_time

		db_cursor["user_info"] = user_info
		fp = open(conf.USER_INFO_DATA, "wb")
		pickle.dump(db_cursor, fp)


class Group(object):
	def __init__(self, creator):
		self.gid = creator.uid
		self.creator = creator
		self.members = [creator]


	def add_user(self, user):
		if user not in self.members:
			self.members.append(user)


	def del_user(self, user):
		if user in self.members:
			self.members.remove(user)


	def save(self):
		db_cursor = None
		fp = open(conf.USER_INFO_DATA, "rb")
		try:
			db_cursor = pickle.load(fp)
		except:
			pass
		fp.close()

		group_info = None
		if db_cursor and "group_info" in db_cursor.keys():
			group_info = db_cursor["group_info"]
		elif not db_cursor:
			db_cursor = {}
			db_cursor["group_info"] = {}
		else:
			db_cursor["group_info"] = {}

		group_info = db_cursor["group_info"]
		if self.gid not in group_info.keys():
			group_info[self.gid]["creator"] = self.creator
		group_info[self.gid]["members"] = self.members

		db_cursor["group_info"] = group_info
		fp = open(conf.USER_INFO_DATA, "wb")
		pickle.dump(db_cursor, fp)
		fp.close()