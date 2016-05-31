#!/usr/bin/python

from conf import conf
import time, pickle


class DBConnection(object):
	def __init__(self, dbname):
		self.dbname = dbname

	def get_cursor(self):
		fp = open(self.dbname, 'rb')
		if not fp:
			print 'Failed to acquire DBConnection !!!'
			raise ValueError('Invalid dbname<%s> !!!' % self.dbname)

		db_cursor = None
		try:
			db_cursor = pickle.load(fp)
		except:
			pass

		fp.close()

		return db_cursor

	def write_back(self, data):
		fp = open(self.dbname, 'wb')
		if not fp:
			print 'Failed to acquire DBConnection !!!'
			raise ValueError('Invalid dbname<%s> !!!' % self.dbname)

		if not data:
			data = {}

		pickle.dump(data, fp)
		fp.close()

	def clear(self):
		self.write_back(None)

	@classmethod
	def is_user_existed(cls, cursor, user):
		if cursor is None or not isinstance(cursor, dict):
			return False

		uid = user.get_uid()
		if uid in cursor.keys():
			user_info = cursor[uid]
			a = user_info['username'] == user.get_username()
			b = user_info['password'] == user.get_password()
			return a and b
		return False

	def disconnect(self):
		pass


if __name__ == '__main__':
	dbconn = DBConnection(conf.DB_USER)
	cursor = dbconn.get_cursor()