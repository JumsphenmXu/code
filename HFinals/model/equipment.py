#!/usr/bin/python


class EquipmentType(object):
	WEAPON = 0x0001
	SHIELD = 0x0002
	ACCESSORIES = 0x0004


class Equipment(object):
	def __init__(self, name, offense, defense, etype):
		self.name_ = name
		self.offense_ = offense
		self.defense_ = defense
		self.etype_ = etype

	@classmethod
	def clone(cls, equipment):
		if isinstance(equipment, cls):
			return cls(equipment.name_, equipment.offense_, equipment.defense_, equipment.etype_)
		raise ValueError('The object can not be cloned !!!')

	def get_name(self):
		return self.name_

	def set_name(self, name):
		self.name_ = name

	def get_offense(self):
		return self.offense_

	def set_offense(self, offense):
		if offense < 0:
			raise ValueError('The value of offense can not be nagative !!!')
		self.offense_ = offense

	def get_defense(self):
		return self.defense_

	def set_defense(self, defense):
		if defense < 0:
			raise ValueError('The value of defense can not be nagative !!!')
		self.defense_ = defense

	def get_type(self):
		return self.etype_

	def set_type(self, etype):
		if etype != EquipmentType.WEAPON and etype != EquipmentType.SHIELD and etype != EquipmentType.ACCESSORIES:
			raise ValueError('The type of Equipment must be one of [WEAPON, SHIELD, ACCESSORIES] !!!')
		self.etype_ = etype


class Gun(Equipment):
	def __init__(self):
		pass


class Knife(Equipment):
	def __init__(self):
		pass


class Jacket(Equipment):
	def __init__(self):
		pass


class Armour(Equipment):
	def __init__(self):
		pass


class Shoe(Equipment):
	def __init__(self):
		pass


class Jade(Equipment):
	def __init__(self):
		pass