#!/usr/bin/python

__author__ = 'XU Xinhui'

import random, copy, time
from XGraph import XGraph
from XDiffusionModel import XDiffusionModel
from XGraphPricing import XGraphPricing


class XBudgetedCIMext(object):
	def __init__(self, graph_file, model):
		self.graph_file = graph_file
		self.model = model
		self.graph = XGraph()
		self.graph.load_graph_from_file(graph_file)
		self.graph.threshold_generator()
		self.graph.weight_generator()
		self.graph.mutation_factor_generator()
		self.cost = self.pricing_graph()

	def pricing_graph(self):
		gp = XGraphPricing()
		return gp.pricing_graph(self.graph_file)

	def random_max_degree_neighbor(self, S, budget, epsilon):
		bsum = 0
		T = []
		vertices = self.graph.get_all_vertices()
		i = 0

		ft = time.time()
		while i < k:
			v = random.choice(vertices)
			es = list(set(T) | set(S))
			max_v = self.graph.max_degree_neighbor(v, es)

			if max_v not in self.cost.keys():
				continue

			if bsum + self.cost[max_v] <= budget + epsilon:
				T.append(max_v)
				bsum += self.cost[max_v]
				i += 1
				if bsum >= budget - epsilon:
					break

		time_elapsed = time.time() - ft
		print '#RMDN Time consumed: %.2f secs' % (time_elapsed)
		return T, time_elapsed

	def greedy(self, k, budget, epsilon):
		S = []
		i = 0
		bsum = 0
		vertices = self.graph.get_all_vertices()

		ft = time.time()
		while i < k:
			target, maxinf = -1, -1
			for v in vertices:
				if v in S:
					continue

				Ss = copy.deepcopy(S)
				Ss.append(v)
				g = copy.deepcopy(self.graph)
				curS, _ = self.model.calc_influence(g, Ss, [])

				g = copy.deepcopy(self.graph)
				prevS, _ = self.model.calc_influence(g, S, [])

				if curS - prevS > maxinf and bsum + self.cost[v] <= budget + epsilon:
					maxinf = curS - prevS
					target = v

			if target != -1:
				S.append(target)
				bsum += self.cost[target]
				i += 1
				if bsum >= budget - epsilon:
					break

		time_elapsed = time.time() - ft
		print '#Greedy Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

	def degree_heuristic(self, S, budget, epsilon):
		ft = time.time()
		out_degree = []
		vertices = self.graph.get_all_vertices()
		for vid in vertices:
			out_degree.append((vid, len(self.graph.get_edges_by_vertice(vid))))

		out_degree_sorted = sorted(out_degree, key=lambda x: x[1], reverse=True)
		T = []
		bsum = 0
		i = 0
		while True:
			vid = out_degree_sorted[i][0]
			i += 1
			if vid in T or vid in S:
				continue

			if bsum + self.cost[vid] <= budget + epsilon:
				bsum += self.cost[vid]
				T.append(vid)

			if bsum >= budget - epsilon or len(T) >= len(S):
				break

		time_elapsed = time.time() - ft
		print '#Degree Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return T, time_elapsed

	def comparable_heuristic(self, S, budget, epsilon):
		ft = time.time()
		T = []
		bsum = 0
		for v in S:
			edges = self.graph.get_edges_by_vertice(v)
			maxinf = -1
			target = -1
			for e in edges:
				to = e.get_dest()
				# if to in T or to in S or self.cost[to] <= 0:
				if to in T or to in S:
					continue

				if target == -1:
					target = to
					g = copy.deepcopy(self.graph)
					maxinf, _ = self.model.calc_influence(g, [target], S)
					continue

				g = copy.deepcopy(self.graph)
				prevT, _ = self.model.calc_influence(g, T, S)
				Ts = copy.deepcopy(T)
				Ts.append(to)
				g = copy.deepcopy(self.graph)
				curT, _ = self.model.calc_influence(g, Ts, S)
				# fc = float(curT - prevT)/self.cost[to]
				fc = curT - prevT
				if maxinf < fc and bsum + self.cost[to] <= budget + epsilon:
					maxinf = fc
					target = to

			if target != -1:
				T.append(target)
				bsum += self.cost[target]

			if bsum >= budget - epsilon or len(T) >= len(S):
				break

		time_elapsed = time.time() - ft
		print '#Comparable Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return T, time_elapsed

	def local_degree_heuristic(self, S, budget, epsilon):
		ft = time.time()
		vertices = self.graph.get_all_vertices()
		T = []
		bsum = 0
		for v in S:
			r = random.choice(vertices)
			target = r
			x = self.graph.max_degree_neighbor(r, list(set(T) | set(S)))
			if x != -1:
				target = x

			maxd = len(self.graph.get_edges_by_vertice(target))
			edges = self.graph.get_edges_by_vertice(v)
			for e in edges:
				to = e.get_dest()
				d = len(self.graph.get_edges_by_vertice(to))
				if maxd < d and bsum + self.cost[to] <= budget + epsilon:
					maxd = d
					target = to
				
			if target != -1 and bsum + self.cost[target] <= budget + epsilon:
				T.append(target)
				bsum += self.cost[target]

			if bsum >= budget - epsilon or len(T) >= len(S):
				break

		time_elapsed = time.time() - ft
		print '#Local Degree Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return T, time_elapsed

	def local_greedy_heuristic(self, S, budget, epsilon):
		ft = time.time()
		vertices = self.graph.get_all_vertices()
		T = []
		bsum = 0
		for v in S:
			r = random.choice(vertices)
			target = r
			r = self.graph.max_degree_neighbor(r, list(set(T) | set(S)))
			if r != -1:
				target = r

			maxinf = -(1 << 20)

			# if self.cost[target] <= 0 or bsum + self.cost[target] > budget + epsilon:
			if bsum + self.cost[target] > budget + epsilon:
				target = -1
			else:
				Ttmp = copy.deepcopy(T)
				Ttmp.append(target)
				g = copy.deepcopy(self.graph)
				prevT, _ = self.model.calc_influence(g, T, S)
				g = copy.deepcopy(self.graph)
				curT, _ = self.model.calc_influence(g, Ttmp, S)
				# maxinf = float(curS - prevS)/self.cost[target]
				maxinf = curT - prevT

			edges = self.graph.get_edges_by_vertice(v)
			for e in edges:
				to = e.get_dest()
				# if to in T or to in S or self.cost[to] <= 0:
				if to in T or to in S:
					continue

				if target == -1:
					target = to
					g = copy.deepcopy(self.graph)
					maxinf, _ = self.model.calc_influence(g, [target], S)
					continue

				g = copy.deepcopy(self.graph)
				prevT, _ = self.model.calc_influence(g, T, S)
				Ts = copy.deepcopy(T)
				Ts.append(to)
				g = copy.deepcopy(self.graph)
				curT, _ = self.model.calc_influence(g, Ts, S)
				# fc = float(curS - prevS)/self.cost[to]
				fc = curT - prevT
				if maxinf < fc and bsum + self.cost[to] <= budget + epsilon:
					maxinf = fc
					target = to

			if target != -1:
				T.append(target)
				bsum += self.cost[target]

			if bsum >= budget - epsilon or len(T) >= len(S):
				break

		time_elapsed = time.time() - ft
		print '#Local Greedy Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return T, time_elapsed

	def infmax(self, k, R, budget, epsilon, result_file):
		ts = []
		res = []
		S, gtimes = self.greedy(k, budget, epsilon)

		T, dtimes = self.degree_heuristic(S, budget, epsilon)
		ts.append(T)
		res.append(('DHeu', 0, 0, dtimes))

		T, ctimes = self.comparable_heuristic(S, budget, epsilon)
		ts.append(T)
		res.append(('CHeu', 0, 0, ctimes))
		
		T, rtimes = self.random_max_degree_neighbor(S, budget, epsilon)
		ts.append(T)
		res.append(('RMDN', 0, 0, rtimes))

		T, ldtimes = self.local_degree_heuristic(S, budget, epsilon)
		ts.append(T)
		res.append(('LDeg', 0, 0, ldtimes))

		T, lgtimes = self.local_greedy_heuristic(S, budget, epsilon)
		ts.append(T)
		res.append(('LGdy', 0, 0, lgtimes))

		for i in xrange(R):
			print 'Round %d starts...' % (i + 1)
			for j in xrange(len(ts)):
				g = copy.deepcopy(self.graph)
				s, t = self.model.calc_influence(g, S, ts[j])
				print 'Round %d: %s-> #s = %d, #t = %d' % (i+1, res[j][0], s, t)
				print 'len(S) = %d, len(T) = %d' % (len(S), len(T))
				lres = list(res[j])
				lres[1] += s
				lres[2] += t
				res[j] = tuple(lres)

		fp = open(result_file, 'wb')
		if not fp:
			print 'Failed to open file %s !' % result_file
			return

		line = 'Greedy time consumed: ' + str(gtimes) + '\n'
		line += 'Budget: ' + str(budget) + '\n'
		fp.write(line)
		line = 'ALGORITHM\tLEN(S)\tLEN(T)\tINFLUENCE(S)\tINFLUENCE(T)\tTIME\n'
		fp.write(line)
		for i in xrange(len(res)):
			rs = float(res[i][1]) / R
			rs = round(rs, 2)
			rt = float(res[i][2]) / R
			rt = round(rt, 2)
			line = '{0: >9}'.format(res[i][0]) + '\t' + '{0: >6}'.format(str(len(S))) + '\t'
			line += '{0: >6}'.format(str(len(ts[i]))) + '\t' + '{0: >12}'.format(str(rs)) + '\t'
			line += '{0: >12}'.format(str(rt)) + '\t' + '{0: >4}'.format(str(res[i][3])) + '\n'
			fp.write(line)

		fp.close()


if __name__ == '__main__':
	k = 15
	budget_base = 200
	rounds = 30
	epsilon = 2
	base_dir = '../../../graphdata/'
	graph_files = ['USAir_unweight', 'BA_weight', 'blogs', 'facebook']
	graph_files = ['blogs']
	suffix = '.txt'
	model = XDiffusionModel()

	for f in graph_files:
		graph_file = base_dir + f + suffix
		bcim = XBudgetedCIMext(graph_file, model)
		for bstep in xrange(4):
			budget = budget_base + 100 * (bstep + 1)
			for i in xrange(6):
				k = 5 * (i + 1)
				result_file = '../result/final/' + f
				result_file += '-B' + str(budget) + '-K' + str(k) + suffix
				bcim.infmax(k, rounds, budget, epsilon, result_file)
