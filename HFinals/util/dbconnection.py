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

	def disconnect(self):
		pass


if __name__ == '__main__':
	dbconn = DBConnection(conf.DB_USER)
	cursor = dbconn.get_cursor()