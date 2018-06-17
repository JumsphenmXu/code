

class parser(object):

	def __init__(self, formula):
		self._formula = formula
		self._cur = 0
		self._end = len(formula) if formula else 0

	def peek(self):
		if self._cur < self._end:
			return self._formula[self._cur]

		return None

	def next(self):
		c = self.peek()
		if c is not None:
			self._cur += 1

		return c

	def putback(self):
		self._cur -= 1

	def skip(self):
		c = self.next()
		while c is not None and c in ' \t\r\n':
			c = self.next()

		if c is not None:
			self.putback()

	def isupper(self, c):
		return 'A' <= c <= 'Z'

	def islower(self, c):
		return 'a' <= c <= 'z'

	def isdigit(self, c):
		return '0' <= c <= '9'

	def value(self):
		res = 0
		c = self.next()
		while self.isdigit(c):
			res *= 10
			res += int(c)
			c = self.next()

		if c is not None:
			self.putback()

		return res

	def parse(self):
		self.skip()
		result = {}

		while True:
			c = self.next()
			if c == '(':
				xs = self.parse()
				for key, val in xs.items():
					result[key] = result.get(key, 0) + val
			elif c == ')':
				factor = self.value()
				for key, val in result.items():
					result[key] = val * factor
				return result
			elif self.isupper(c):
				key = c
				c = self.next()
				while self.islower(c):
					key += c
					c = self.next()

				if c is not None:
					self.putback()

				val = self.value()
				print key, val
				if val == 0:
					val = 1

				result[key] = result.get(key, 0) + val
			elif c is None:
				break
			else:
				raise ValueError('The chemistry formula %s is ill-formed !!!' % self._formula)

		return result

if __name__ == '__main__':
	formula = 'KMGHYT((H2O2)4Mg5)10H8O9'
	p = parser(formula)
	print p.parse()