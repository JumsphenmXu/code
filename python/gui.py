#!/usr/bin/env python

import Tkinter


def getItem(self, bracketFlag=False):
	ans = []
	while True:
		self.skip()
		ch = self.next()

		if ch is None:
			if bracketFlag:
				raise ValueError('Illegal expression !!!')
			else:
				break

		if ch == '}':
			if not bracketFlag:
				raise ValueError('Brackets does not match !!!')
			if len(ans) == 1 and ans[0] != {}:
				ans = ans[0]
			self.printLeftToken('SRC RIGHT:')
			return ans

		if ch == '{':
			self.printLeftToken('SRC LEFT:')
			item = self.getItem(True)
			if self.prev() != '}':
				raise ValueError('Brackets does not match !!!')
			self.skip()
			ch = self.next()
			if ch is None and not bracketFlag:
				break
			elif ch != '}':
				PyLuaTblParser.validate(ch)
			else:
				self.putback()
			ans.append(item)
			if self.underDebugMode():
				print '{-->ans =', ans
		elif ch == '"' or ch == '\'':
			s = self.getStr(ch)
			self.skip()
			ch = self.next()
			if ch != '}':
				PyLuaTblParser.validate(ch)
			else:
				self.putback()
			ans.append(s)
			if self.underDebugMode():
				print '"-->ans =', ans
		elif ch == '[':
			self.skip()
			ch = self.next()
			key, val = None, None
			if ch == '"' or ch == '\'':
				key = self.getStr(ch)
			else:
				self.putback()
				key = self.getNumber()

			self.skip()
			if self.next() != ']':
				raise ValueError('Square brackets does not match !!!')
			self.skip()
			if self.next() != '=':
				raise ValueError('Dict should in the pattern KEY=VAL !!!')
			self.skip()
			val = self.getValue(key)
			if self.underDebugMode():
				print '[\'key\'] = %s, val = %s' % (str(key), str(val))
			self.skip()
			ch = self.next()
			if ch != '}':
				PyLuaTblParser.validate(ch)
			else:
				self.putback()
			if key is None or key == '':
				raise ValueError('Key can not be Empty or None !!!')

			if val is not None or type(key) is int:
				ans.append({key: val})
			if self.underDebugMode():
				print '[-->ans =', ans
		elif PyLuaTblParser.isDigit(ch) or ch == '+' or ch == '-':
			if ch == '-' and self.next() == '-':
				ch = self.next()
				while ch is not None and ch != '\n':
					ch = self.next()
				continue
				# self.putback()
			else:
				self.putback()
				num = self.getNumber()
				self.skip()
				ch = self.next()
				if ch != '}':
					PyLuaTblParser.validate(ch)
				else:
					self.putback()
				ans.append(num)
			if self.underDebugMode():
				print 'N-->ans =', ans
		elif PyLuaTblParser.isAlphabet(ch) or ch == '_':
			key = ''
			while PyLuaTblParser.isAlphanum(ch):
				key += ch
				ch = self.next()
			self.putback()
			self.skip()

			key, spFlag = self.checkSpecialStr(key)
			if spFlag:
				self.skip()
				ch = self.next()
				if ch != '}':
					PyLuaTblParser.validate(ch)
				else:
					self.putback()
				continue

			if self.next() != '=':
				raise ValueError('Dict should in the pattern KEY=VAL !!!')
			val = self.getValue(key)
			if self.underDebugMode():
				print 'key = %s, val = %s' % (str(key), str(val))
			self.skip()
			ch = self.next()
			if ch != '}':
				if self.underDebugMode():
					print 'Already parsed $%s$.' % self.luaStr[:self.curPos]
				PyLuaTblParser.validate(ch)
			else:
				self.putback()

			if key is None or key == '':
				raise ValueError('Key can not be Empty or None !!!')
			if val is not None:
				ans.append({key: val})
			if self.underDebugMode():
				print 'K-->ans =', ans
		else:
			msg = 'Invalid lua table string: $%s$, current character is $%s$.' % (self.luaStr[0:self.curPos], ch)
			raise ValueError(msg)
	
	if len(ans) == 1 and ans[0] != {}:
		ans = ans[0]

	if self.underDebugMode():
		print 'Finally ans =', ans
	return ans		





if __name__ == '__main__':
	root = Tkinter.Tk()

	label = Tkinter.Label(root, text="hello world!")
	label.pack()

	btn = Tkinter.Button(root, text="Press me!!!", command=root.quit, bg='red', fg='white')
	btn.pack(fill=Tkinter.X, expand=1)

	Tkinter.mainloop()