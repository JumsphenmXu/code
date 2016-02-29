#!/usr/bin/python

__author__ = 'XU Xinhui'

import random, copy, time
from XGraph import XGraph
from XDiffusionModel import XDiffusionModel
from XGraphPricing import XGraphPricing

class XBudgetedCIM(object):
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

	def get_sample(self, k, budget, epsilon):
		bsum = 0
		T = []
		vertices = self.graph.get_all_vertices()
		i = 0

		while i < k:
			v = random.choice(vertices)
			max_v = self.graph.max_degree_neighbor(v, T)

			if max_v not in self.cost.keys() or max_v in T:
				continue

			if bsum + self.cost[max_v] <= budget + epsilon:
				T.append(max_v)
				bsum += self.cost[max_v]

			if bsum >= budget - epsilon:
				break
			i += 1

		return T

	def greedy(self, T, budget, epsilon):
		pass

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

		print '#Degree Heuristic Time consumed: %.2f secs' % (time.time() - ft)
		return S

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

		print '#Comparable Heuristic Time consumed: %.2f secs' % (time.time() - ft)
		return S

	def infmax(self, k, budget, epsilon):
		T = self.get_sample(k, budget, epsilon)

		S = self.degree_heuristic(T, budget, epsilon)
		g = copy.deepcopy(self.graph)
		t, s = self.model.calc_influence(g, T, S)
		print 'DegreeHeuristic k = %d, budget = %d, t = %d, s = %d' % (k, budget, t, s)

		S = self.comparable_heuristic(T, budget, epsilon)
		g = copy.deepcopy(self.graph)
		t, s = self.model.calc_influence(g, T, S)
		print 'ComparableHeuristic k = %d, budget = %d, t = %d, s = %d' % (k, budget, t, s)


if __name__ == '__main__':
	k = 15
	budget = 100
	epsilon = 2
	graph_file = '../../../graphdata/USAir_unweight.txt'
	model = XDiffusionModel()

	bcim = XBudgetedCIM(graph_file, model)
	for i in xrange(3):
		k = (i + 2) * 5
		budget += 50 * i
		bcim.infmax(k, budget, epsilon)
