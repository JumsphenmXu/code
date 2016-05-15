#!/usr/bin/python

from util import dbconnection
from conf import conf
import time

class User(object):
	def __init__(self, username, password):
		self.username_ = username
		self.password_ = password
		self.equipments_ = None
		self.total_online_time_ = 0
		self.last_online_time_ = 0
		self.login_time_ = time.time()
		self.health_ = 1000
		self.level_ = 1
		self.wealth_ = 0
		self.uid_ = self.__uid()

	def __str_hash(self, s):
		if not s or len(str(s)) == 0:
			return 0

		s = str(s)
		hvalue = 0
		for c in s:
			hvalue += ord(c) ^ (hvalue << 1)

		return hvalue

	def __uid(self):
		return self.__str_hash(self.username_) ^ self.__str_hash(self.password_)

	def __pack_user_info(self):
		user_info = {}
		user_info['username'] = self.username_
		user_info['password'] = self.password_
		user_info['equipments'] = self.equipments_
		user_info['total_online_time'] = self.total_online_time_
		user_info['last_online_time'] = self.last_online_time_
		user_info['login_time'] = self.login_time_
		user_info['health'] = self.health_
		user_info['wealth'] = self.wealth_
		user_info['level'] = self.level_
		return user_info

	def get_uid(self):
		return self.uid_

	def get_username(self):
		return self.username_

	def set_username(self, username):
		self.username_ = username
		self.uid_ = self.__uid()

	def get_equipments(self):
		return self.equipments_

	def set_equipments(self, equipments):
		self.equipments_ = equipments

	def get_total_online_time(self):
		return self.total_online_time_

	def set_total_online_time(self, total_online_time):
		self.total_online_time_ = total_online_time

	def get_last_online_time(self):
		return self.last_online_time_

	def set_last_online_time(self, last_online_time):
		self.last_online_time_ = last_online_time

	def get_login_time(self):
		return self.login_time_

	def set_login_time(self, login_time):
		self.login_time_ = login_time

	def get_health(self):
		return self.health_

	def set_health(self, health):
		self.health_ = health

	def get_wealth(self):
		return self.wealth_

	def set_wealth(self, wealth):
		self.wealth_ = wealth

	def get_level(self):
		return self.level_

	def set_level(self, level):
		self.level_ = level

	def increment_level(self):
		self.level_ += 1

	def is_dead(self):
		return self.health_ < 0

	def calc_odffense(self):
		offense = 0
		defense = 0
		for e in equipments:
			offense += e.get_offense() + 10 * self.level_
			defense += e.get_defense() + 10 * self.level_

		if offense == 0 or defense == 0:
			offense += 20 * self.level_
			defense += 18 * self.level_

		return offense, defense

	def save(self):
		dbconn = dbconnection.DBConnection(conf.DB_USER)
		cursor = dbconn.get_cursor()

		if not cursor:
			cursor = {}

		if self.uid_ not in cursor:
			cursor[self.uid_] = {}

		self.total_online_time_ += time.time() - self.login_time_
		self.last_online_time_ = time.time()
		user_info = self.__pack_user_info()
		cursor[self.uid_] = user_info

		dbconn.write_back(cursor)
		dbconn.disconnect()