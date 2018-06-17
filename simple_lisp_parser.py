#!/usr/bin/python


class frame(object):

	def __init__(self, prev_frame=None, next_frame=None):
		self._scopes = {}
		self._prev_frame = prev_frame
		self._next_frame = next_frame

	def put_var(self, key, val, force_update=True):
		if force_update:
			self._scopes[key] = val
		else:
			if key not in self._scopes.keys():
				self._scopes[key] = val

	def get_var(self, key, default=None):
		f = self
		while f is not None:
			if key in f._scopes.keys():
				return f._scopes[key]

			f = f.get_prev_frame()

		return default

	def get_prev_frame(self):
		return self._prev_frame

	def set_prev_frame(self, prev_frame):
		self._prev_frame = prev_frame

	def get_next_frame(self):
		return self._next_frame

	def set_next_frame(self, next_frame):
		self._next_frame = next_frame

	def __repr__(self):
		f = self
		res = []
		while f is not None:
			res.append(str(f._scopes))
			f = f.get_prev_frame()

		return 'frame status:' + ' | '.join(res) 

	def __str__(self):
		return self.__repr__()


class stack(object):

	def __init__(self):
		self._stk = []
		self._top = -1

	def top(self):
		if self._top >= 0:
			return self._stk[self._top]

		return None

	def pop(self):
		if self._top == -1:
			raise ValueError('stack underflow')
		self._top -= 1

	def push(self, item):
		self._stk.append(item)
		self._top += 1

	def empty(self):
		return self.top == -1

	def __repr__(self):
		return 'stack:' + str(self._stk)

	def __str__(self):
		return self.__repr__()

class parser(object):

	KEYWORDS = ( 'let', 'add', 'mult', )

	def __init__(self, expr):
		self._expr = expr
		self._cur = 0
		self._end = len(self._expr if self._expr else '')
		self._frame = frame()
		self._operand_stk = stack()

	def peek_next(self):
		if self._cur >= self._end:
			return None

		return self._expr[self._cur]

	def next(self):
		if self._cur < self._end:
			self._cur += 1
			return self._expr[self._cur - 1]

		return None

	def skip(self):
		while True:
			if self._cur >= self._end:
				return

			if self._expr[self._cur] in ' \t\n\r':
				self._cur += 1
			else:
				break

	def putback(self):
		if self._cur > 0:
			self._cur -= 1
			return self._cur

		return None

	def print_unparsed_expr(self):
		if self._cur < self._end:
			print 'unparse expr:', self._expr[self._cur:]

	def isdigit(self, c):
		return '0' <= c <= '9'

	def hex_to_decimal(self, c):
		if '0' <= c <= '9':
			return int(c)

		if c in 'aA':
			return 10
		elif c in 'bB':
			return 11
		elif c in 'cC':
			return 12
		elif c in 'dD':
			return 13
		elif c in 'eE':
			return 14
		elif c in 'fF':
			return 15

		return None

	def value(self):
		cur = self._cur
		end = self._end

		oct_flag = self._expr[cur] == '0' and cur + 1 < end and self.isdigit(self._expr[cur+1])
		hex_flag = self._expr[cur] == '0' and cur + 1 < end and self._expr[cur+1] in 'xX'

		if oct_flag: cur += 1
		if hex_flag: cur += 2

		if cur >= end or not self.isdigit(self._expr[cur]):
			return None

		res = 0
		while cur < end and self.isdigit(self._expr[cur]):
			if oct_flag:
				res *= 8
			elif hex_flag:
				res *= 16
			else:
				res *= 10

			res += self.hex_to_decimal(self._expr[cur])
			cur += 1

		self._cur = cur
		return res

	def isalpha(self, c):
		return 'a' <= c <= 'z' or\
				'A' <= c <= 'Z'

	def token(self):
		c = self.next()
		t = ''
		first = True
		while self.isalpha(c) or c == '_' or (self.isdigit(c) and not first):
			t += c
			first = False
			c = self.next()

		if c is not None:
			self.putback()

		return t

	def peek_token(self):
		# get next token without affecting the parser's index
		cur = self._cur
		t = self.token()
		self._cur = cur

		return t

	def parse_value(self):
		self.skip()
		c = self.peek_next()

		if self.isdigit(c):
			return self.value()
		elif self.isalpha(c) or c == '_':
			t = self.token()
			return self._frame.get_var(t)
		elif c == '(':
			return self.eval()

	def set_new_frame(self):
		f = frame()
		f.set_prev_frame(self._frame)
		self._frame.set_next_frame(f)
		self._frame = f

	def back_frame(self):
		f = self._frame.get_prev_frame()
		if f is not None:
			f.set_next_frame(None)

		self._frame = f

	def let(self):
		while True:
			self.skip()
			c = self.peek_next()
			if self.isdigit(c):
				# has no key
				val = self.value()
				self._operand_stk.push(val)
				break
			else:
				if c == '(':
					val = self.eval()
					self._operand_stk.push(val)
				elif c == ')':
					self.back_frame()
					self.next()
					break
				else:
					t = self.token()
					val = self.parse_value()
					if val is None:
						self._operand_stk.push(self._frame.get_var(t))
					else:
						self._frame.put_var(t, val)

	def add(self):
		return self.cal('add')

	def mult(self):
		return self.cal('mult')

	def cal(self, op):
		lval = self.parse_value()
		rval = self.parse_value()

		res = None
		if op == 'add':
			res = lval + rval
		elif op == 'mult':
			res = lval * rval

		# eat the right-parenthsis
		self.skip()
		if self.peek_next() == ')':
			self.back_frame()
			self.next()

		return res

	def eval(self):
		self.skip()
		c = self.next()
		if c != '(':
			raise ValueError('Expression should be started with (')
		else:
			self.skip()
			self.set_new_frame()
			c = self.peek_next()
			if self.isalpha(c) or c == '_':
				t = self.token()
				if t == 'let':
					self.let()
				elif t == 'mult':
					return self.mult()
				elif t == 'add':
					return self.add()
				else:
					self._operand_stk.push(self._frame.get_var(t))
			elif self.isdigit(c):
				self._operand_stk.push(self.value())
			elif c == ')':
				self.next()
				self.back_frame()

				res = self._operand_stk.top()
				self._operand_stk.pop()
				return res

		return None if self._operand_stk.empty() else self._operand_stk.top()

if __name__ == '__main__':
	# expr = '(mult 2 (let x 2 y 4 (add x y)))'
	# expr = '(let x 3 x 2 (add x 1))'
	# expr = '(let x 2 (mult x 5))'
	# expr = '(let x 2 (mult x (let x 3 y 4 (add x y))))'
	# expr = '(let x 1 y 2 x (add x y) (add x y))'
	# expr = '(let x 2 (add (let x 3 (let x 4 x)) x))'
	expr = '(let a1 3 b2 (add a1 1) b2)'

	print 'test:', expr
	p = parser(expr)
	print p.eval()