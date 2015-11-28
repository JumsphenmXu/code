#!/usr/bin/python

s = "['bacd[gf][ef][cd][ad]]efg']" # =\"ehahjksad,\"edfagag\"dafd\""
s = "\"dea\"fe\"efada\"dafadadad\"sfasdf\"fdf\""

def delimiter_matcher(s, index, curDeli, flag):
	i, slen = index + 1, len(s)
	res = -1
	while i < slen:
		while i < slen and s[i] == curDeli:
			res = i
			if not flag:
				flag = True
			i = delimiter_matcher(s, i, curDeli, flag)
		if res != -1:
			i = res
			break
		else:
			i += 1

	if i == slen and not flag:
		print 'Square bracket expression ###%s### represents a error.' % s[index: i-1]
		raise ValueError

	return i


def split_lua_table(s):
	s = s.strip()
	start, lbc, rbc, i, slen = 0, 0, 0, 0, len(s)
	if slen > 0 and s[0] == '{' and s[slen-1] == '}':
		i = 1
		if slen > 1 and s[slen-2] == ',':
			slen -= 2
		else:
			slen -= 1

	s = s[i: slen]
	slen = len(s)
	parts = []
	i = 0
	while i < slen:
		if s[i] == '{':
			lbc += 1
		elif s[i] == '}':
			rbc += 1
			if i == slen - 1 and lbc == rbc:
				parts.append(s[start: i].strip())
				return parts
		elif s[i] == '[':
			f = ''
			i += 1
			if i < slen:
				f = '"' if s[i] == '"' else ('\'' if s[i] == '\'' else '')
			if f != '':
				while i < slen:
					i += 1
					j = i
					while i < slen and s[i] == ' ':
						i += 1
					end = s[i] == f if i < slen else False

					i += 1
					while i < slen and s[i] == ' ':
						i += 1
					end = end and (s[i] == ']' if i < slen else False)

					i += 1
					while i < slen and s[i] == ' ':
						i += 1
					end = end and (s[i] == '=' if i < slen else False)

					if not end:
						i = j + 1
					else:
						break
			else:
				j = i
				while i < slen and s[i] != ']':
					i += 1			
		elif s[i] == '"' or s[i] == '\'':
			f = s[i]
			i += 1
			while i < slen:
				if s[i] != f:
					i += 1
				else:
					break
		elif i == slen - 1 or s[i] == ',':
			if lbc != rbc:
				if i == slen - 1:
					print 'Failed to partition %s, the brackets do not match!' % t
					raise ValueError
				else:
					i += 1
					continue
			else:
				# add to the parts
				if i == slen - 1:
					i = i + 1
				parts.append(s[start: i].strip())
				start = i + 1
				lbc, rbc = 0, 0
		i += 1
	# end main while loop
	return parts


if __name__ == '__main__':
	test = "\"dea\"fe\"efada\"dafadadad\"sfasdf\"fdf"
	s = '{65,23,5, {1, 2, 3},["yada{,[had"]="nice", hello="world,"def,j"}'
	i = delimiter_matcher(test, 0, "\"", False)
	if i < len(test):
		print "i = ", i
		print test[0: i]

	print split_lua_table(s) 
