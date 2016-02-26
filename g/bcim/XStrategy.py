#!/usr/bin/python
#

__author__ = 'XU Xinhui'

class XStrategy(object):
	def __init__(self, graph, model):
		self.graph = graph
		self.model = model

	def greedy(self, T):
		ft = time.time()
		S = []
		i, k = 0, len(T)
		while i < k:
			vertices = self.graph.get_all_vertices()
			maxinf = -1
			target = -1
			for v in vertices:
				if v in T or v in S:
					continue

				Tt, Ss = copy.deepcopy(T), copy.deepcopy(S)
				Ss.append(v)
				g = copy.deepcopy(self.graph)
				_, scntx = self.model.calc_influence(g, Tt, Ss)
				g = copy.deepcopy(self.graph)
				_, scnt = self.model.calc_influence(g, T, S)
				if scntx - scnt > maxinf:
					maxinf = scntx - scnt
					target = v

			if target != -1:
				S.append(target)
				i += 1
			else:
				break

		print '#Greedy Time consumed: %.2f secs' % (time.time() - ft)
		return S

	def degree_heuristic(self, T):
		ft = time.time()
		k = len(T)
		out_degree = []
		vertices = self.graph.get_all_vertices()
		for vid in vertices:
			out_degree.append((vid, len(self.graph.get_edges_by_vertice(vid))))

		out_degree_sorted = sorted(out_degree, key=lambda x: x[1], reverse=True)

		S = []
		limit, i = k, 0
		if len(out_degree_sorted) < 2 * k:
			limit = len(out_degree_sorted) - k

		while len(S) < limit:
			vid = out_degree_sorted[i][0]
			if vid not in T and vid not in S:
				S.append(vid)
			i += 1

		print '#Degree Heuristic Time consumed: %.2f secs' % (time.time() - ft)
		return S

	def comparable_heuristic(self, T):
		"""
		Given the set T, we should return a set S which under the specified diffusion
		model can have comparable influece spread as T by using this strategy.
		"""
		ft = time.time()
		S = []
		for v in T:
			edges = self.graph.get_edges_by_vertice(v)
			maxinf = -1
			target = -1
			for e in edges:
				to = e.get_dest()
				if to in T or to in S:
					continue

				if target == -1:
					target = to
					g = copy.deepcopy(self.graph)
					maxinf, _ = self.model.calc_influence(g, [target], T)
					continue

				g = copy.deepcopy(self.graph)
				Ss = copy.deepcopy(S)
				prevS, _ = self.model.calc_influence(g, S, T)
				Ss.append(to)
				g = copy.deepcopy(self.graph)
				curS, _ = self.model.calc_influence(g, Ss, T)
				if maxinf < curS - prevS:
					maxinf = curS - prevS
					target = to

			if target != -1:
				S.append(target)
		print '#Comparable Heuristic Time consumed: %.2f secs' % (time.time() - ft)
		return S

	def get_sample(self, k):
		nodes = self.graph.get_all_vertices()
		T = []
		i = 0
		# The get sample method is similar to the method we used in
		# 'A Budgeted Method for Influence Maximization' (XU Xinhui et al SEKE2015)
		while i < k:
			u = random.choice(nodes)
			maxnode = self.graph.max_degree_neighbor(u, T)
			T.append(maxnode)
			i += 1

		return T

	def infmax(self, k):
		T = self.get_sample(k)
		S = self.greedy(T)
		g = copy.deepcopy(self.graph)
		t, s = self.model.calc_influence(g, T, S)
		# s, t = self.model.calc_influence(g, S, T)
		print 'greedy: t = %d, s = %d' % (t, s)
		print 'len(T) =', len(T)
		print 'T =', T
		print 'len(S) =', len(S)
		print 'S =', S

		S = self.degree_heuristic(T)
		g = copy.deepcopy(self.graph)
		t, s = self.model.calc_influence(g, T, S)
		# s, t = self.model.calc_influence(g, S, T)
		print 'degree_heuristic: t = %d, s = %d' % (t, s)
		print 'len(T) =', len(T)
		print 'T =', T
		print 'len(S) =', len(S)
		print 'S =', S

		g = copy.deepcopy(self.graph)
		S = self.comparable_heuristic(T)
		g = copy.deepcopy(self.graph)
		s, t = self.model.calc_influence(g, S, T)
		print 'comparable_heuristic: t = %d, s = %d' % (t, s)
		print 'len(T) =', len(T)
		print 'T =', T
		print 'len(S) =', len(S)
		print 'S =', S

	def infmax_ext(self, k, R, result_file):
		ts = []
		res = []
		T = self.get_sample(k)
		S = self.greedy(T)
		ts.append((T, S))
		res.append(('Greedy', 0, 0))

		S = self.degree_heuristic(T)
		ts.append((T, S))
		res.append(('DegreeHeuristic', 0, 0))

		S = self.comparable_heuristic(T)
		ts.append((T, S))
		res.append(('ComparableHeuristic', 0, 0))

		for i in xrange(R):
			print 'Round %d starts...' % (i + 1)
			for j in xrange(len(ts)):
				g = copy.deepcopy(self.graph)
				t, s = self.model.calc_influence(g, ts[j][0], ts[j][1])
				print 'Round %d: %s-> #t = %d, #s = %d' % (i+1, res[j][0], t, s)
				lres = list(res[j])
				lres[1] += t
				lres[2] += s
				res[j] = tuple(lres)

		fp = open(result_file, 'wb')
		if not fp:
			print 'Failed to open file %s !' % result_file
			return

		for i in xrange(len(res)):
			rt = float(res[i][1]) / R
			rs = float(res[i][2]) / R
			line = res[i][0] + '\t' + str(rt) + '\t' + str(rs) + '\t'
			line += str(100*abs(rt-rs)/max(rt, rs)) + '%\n'
			fp.write(line)

		fp.close()