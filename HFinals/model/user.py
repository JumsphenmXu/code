#!/usr/bin/python


class User(object):
	def __init__(self, username, password, equipments, level=1):
		self.username_ = username
		self.password_ = password
		self.equipments_ = equipments
		self.total_online_time_ = 0
		self.last_online_time_ = 0
		self.health_ = 0
		self.level_ = level

	def save(self):
		pass

	def calc_odffense(self):
		offense = 0
		defense = 0
		for e in equipments:
			offense += e.get_offense()
			defense += e.get_defense()

		return offense, defense