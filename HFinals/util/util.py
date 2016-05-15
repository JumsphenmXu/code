#!/usr/bin/python

from conf import conf
from model import user, equipment
import pickle, time


def init_equipments():
	fp = open(conf.WEAPON, 'wb')
	if not fp:
		print 'Failed to initiate equipments !!!'
		raise ValueError('Wrong file name <%s> !!!' % conf.WEAPON)

	