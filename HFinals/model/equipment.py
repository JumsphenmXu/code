#!/usr/bin/python

class EquipmentType(object):
	WEAPON = 0x0001
	SHIELD = 0x0002
	ACCESSORIES = 0x0004


class Equipment(object):
	def __init__(self, name, offense, defense, etype, level=1):
		self.name_ = name
		self.offense_ = offense
		self.defense_ = defense
		self.level_ = level
		self.etype_ = etype
		self.uid_ = self.__uid()

	def __uid(self):
		if not self.name_ or len(str(self.name_)) == 0:
			raise ValueError('Equipment has no name !!!')

		name = str(self.name_)
		hvalue = 0
		for c in name:
			hvalue += ord(c) ^ (hvalue << self.etype_)

		return hvalue

	@classmethod
	def clone(cls, equipment):
		if isinstance(equipment, cls):
			return cls(equipment.name_, equipment.offense_, equipment.defense_, equipment.etype_)
		raise ValueError('The object can not be cloned !!!')

	def get_uid(self):
		return self.uid_

	def get_name(self):
		return self.name_

	def set_name(self, name):
		self.name_ = name
		self.uid_ = self.__uid()

	def get_offense(self):
		return int((1 + self.level_ / 30.0) * self.offense_)

	def set_offense(self, offense):
		if offense < 0:
			raise ValueError('The value of offense can not be nagative !!!')
		self.offense_ = offense

	def get_defense(self):
		return int((1 + self.level_ / 30.0) * self.defense_)

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
		self.uid_ = self.__uid()

	def get_level(self):
		return self.level_

	def set_level(self, level):
		self.level_ = level


class Gun(Equipment):
	def __init__(self, name, offense, defense, etype, level=1):
		super(Gun, self).__init__(name, offense, defense, etype, level)


class Knife(Equipment):
	def __init__(self, name, offense, defense, etype, level=1):
		super(Knife, self).__init__(name, offense, defense, etype, level)


class Jacket(Equipment):
	def __init__(self, name, offense, defense, etype, level=1):
		super(Jacket, self).__init__(name, offense, defense, etype, level)


class Armour(Equipment):
	def __init__(self, name, offense, defense, etype, level=1):
		super(Armour, self).__init__(name, offense, defense, etype, level)


class Shoe(Equipment):
	def __init__(self, name, offense, defense, etype, level=1):
		super(Shoe, self).__init__(name, offense, defense, etype, level)


class Jade(Equipment):
	def __init__(self, name, offense, defense, etype, level=1):
		super(Jade, self).__init__(name, offense, defense, etype, level)