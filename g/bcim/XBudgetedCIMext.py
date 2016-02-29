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

	def random_max_degree_neighbor(self, T, budget, epsilon):
		bsum = 0
		S = []
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
				S.append(max_v)
				bsum += self.cost[max_v]
				i += 1
				if bsum >= budget - epsilon:
					break

		time_elapsed = time.time() - ft
		print '#RMDN Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

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

	def degree_heuristic(self, T, budget, epsilon):
		ft = time.time()
		out_degree = []
		vertices = self.graph.get_all_vertices()
		for vid in vertices:
			out_degree.append((vid, len(self.graph.get_edges_by_vertice(vid))))

		out_degree_sorted = sorted(out_degree, key=lambda x: x[1], reverse=True)
		S = []
		bsum = 0
		i = 0
		while True:
			vid = out_degree_sorted[i][0]
			i += 1
			if vid in T or vid in S:
				continue

			if bsum + self.cost[vid] <= budget + epsilon:
				bsum += self.cost[vid]
				S.append(vid)

			if bsum >= budget - epsilon:
				break

		time_elapsed = time.time() - ft
		print '#Degree Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

	def comparable_heuristic(self, T, budget, epsilon):
		ft = time.time()
		S = []
		bsum = 0
		for v in T:
			edges = self.graph.get_edges_by_vertice(v)
			maxinf = -1
			target = -1
			for e in edges:
				to = e.get_dest()
				if to in T or to in S or self.cost[to] == 0:
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
				fc = float(curS - prevS)/self.cost[to]
				if maxinf < fc and bsum + self.cost[to] <= budget + epsilon:
					maxinf = fc
					target = to

			if target != -1:
				S.append(target)
				bsum += self.cost[to]

			if bsum >= budget - epsilon:
				break

		time_elapsed = time.time() - ft
		print '#Comparable Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

	def infmax(self, k, R, budget, epsilon, result_file):
		ts = []
		res = []
		T, gtimes = self.greedy(k, budget, epsilon)

		S, dtimes = self.degree_heuristic(T, budget, epsilon)
		ts.append((T, S))
		res.append(('DegreeHeuristic', 0, 0, dtimes))

		S, ctimes = self.comparable_heuristic(T, budget, epsilon)
		ts.append((T, S))
		res.append(('ComparableHeuristic', 0, 0, ctimes))
		
		S, rtimes = self.random_max_degree_neighbor(T, budget, epsilon)
		ts.append((T, S))
		res.append(('RMDN', 0, 0, rtimes))

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

		line = 'greedy time consumed: ' + str(gtimes) + ' secs.\n'
		fp.write(line)
		for i in xrange(len(res)):
			rt = float(res[i][1]) / R
			rs = float(res[i][2]) / R
			line = res[i][0] + '\t' + str(rt) + '\t'
			line += str(rs) + '\t' + str(100*abs(rt-rs)/max(rt, rs))
			line += '%\tT' + str(res[i][3]) + '\n'
			fp.write(line)

		fp.close()


if __name__ == '__main__':
	k = 15
	budget = 100
	epsilon = 2
	graph_file = '../../../graphdata/USAir_unweight.txt'
	model = XDiffusionModel()

	bcim = XBudgetedCIMext(graph_file, model)
	for i in xrange(3):
		k = (i + 2) * 5
		budget += 50 * i
		result_file = '../result/d2usa' + str(k) + '.txt'
		bcim.infmax(k, 100, budget, epsilon, result_file)