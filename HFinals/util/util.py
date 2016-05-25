#!/usr/bin/python

from conf import conf
from model import user, equipment
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
