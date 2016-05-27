#!/usr/bin/python

from conf import conf
from model import user, equipment
from dbconnection import DBConnection
import pickle, time

class TYPE(object):
	INT = 'INT'
	FLOAT = 'FLOAT'
	STRING = 'STRING'
	BOOLEAN = 'BOOLEAN'


class CMD(object):
	LOGIN = 'LOGIN'
	REGISTER = 'REGISTER'
	REQUIRE_LEVEL_INFO = 'REQUIRE_LEVEL_INFO'
	SPAWN_ENEMY = 'SPAWN_ENEMY'


class Util(object):

	@classmethod
	def __calc_level_exp(cls, level):
		exp = conf.BASE_LEVEL_EXP * conf.LEVEL_INC_FACTOR * level
		return int(exp)

	@classmethod
	def init_game_level(cls, max_level=69):
		dbconn = DBConnection(conf.DB_GAME_INFO)
		cursor = dbconn.get_cursor()

		if not cursor:
			cursor = {}

		if 'level_info' not in cursor.keys():
			cursor['level_info'] = {}

		level_info = cursor['level_info']
		level_info['max_level'] = max_level
		level_info['levels'] = []

		for level in xrange(max_level):
			level_info['levels'].append(Util.__calc_level_exp(level+1))

		dbconn.write_back(cursor)

	@classmethod
	def get_game_level_info(cls):
		dbconn = DBConnection(conf.DB_GAME_INFO)
		cursor = dbconn.get_cursor()

		if not cursor or 'level_info' not in cursor.keys():
			return None

		return cursor['level_info']
