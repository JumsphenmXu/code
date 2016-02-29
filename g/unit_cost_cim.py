#!/usr/bin/python

__author__ = 'XU Xinhui'

import random
import copy
import time

class XCOLOR(object):
	BLACK = 0
	RED = 1
	GRAY = 2

	def __init__(self):
		pass


class XEdgeStatus(object):
	def __init__(self, to, weight):
		self.to = to
		self.weight = weight

	def get_dest(self):
		return self.to

	def get_weight(self):
		return self.weight

	def set_weight(self, weight):
		self.weight = weight


class XVerticeStatus(object):
	def __init__(self, threshold=0.3, mutation_flag=False, mutation_factor=0.0, current_color=XCOLOR.GRAY):
		self.threshold = threshold
		self.mutation_flag = mutation_flag
		self.mutation_factor = mutation_factor
		self.current_color = current_color
		self.edges = []
		self.red_visit = 0
		self.black_visit = 0

	def add_edge(self, e):
		self.edges.append(e)

	def del_edge(self, e):
		if e in self.edges:
			self.edges.remove(e)

	def red_visit_inc(self):
		self.red_visit += 1

	def red_visit_dec(self):
		self.red_visit -= 1

	def black_visit_inc(self):
		self.black_visit += 1

	def black_visit_dec(self):
		self.black_visit -= 1

	# getters for attributes
	# 
	def get_red_visit(self):
		return self.red_visit

	def get_black_visit(self):
		return self.black_visit

	def get_edges(self):
		return self.edges

	def get_threshold(self):
		return self.threshold

	def get_mutation_flag(self):
		return self.mutation_flag

	def get_mutation_factor(self):
		return self.mutation_factor

	def get_current_color(self):
		return self.current_color

	# setters for attributes
	def set_edges(self, edges):
		self.edges = edges

	def set_threshold(self, threshold):
		self.threshold = threshold

	def set_mutation_flag(self, mutation_flag):
		self.mutation_flag = mutation_flag

	def set_mutation_factor(self, mutation_factor):
		self.mutation_factor = mutation_factor

	def set_current_color(self, current_color):
		self.current_color = current_color


class XGraph(object):
	def __init__(self):
		"""
		@graph is a map which maps vertice id to its status of type XVerticeStatus
		@directed_graph boolean which flags the graph is directed or not
		@edge_num is an int indicates how many edges does the graph has
		@vertice_num is an int which shows the total number of vertices the graph contains
		"""
		self.graph = {}
		self.directed_graph = False
		self.edge_num = 0
		self.vertice_num = 0

	def load_graph_from_file(self, file_name, seperator=" ", directed_graph=False):
		self.directed_graph = directed_graph
		fp = open(file_name, "rb")
		if not fp:
			print 'Failed to open file %s !!!' % file_name
			return False

		line = fp.readline()
		while line:
			units = line.split(seperator)
			if seperator == '\t' or seperator == ' ':
				units = line.split()
			weight = 0.33 * random.random()
			if len(units) < 2:
				line = fp.readline()
				continue

			if len(units) > 2:
				weight = float(units[2])

			sid = int(units[0])
			eid = int(units[1])
			if sid not in self.graph.keys():
				self.graph[sid] = XVerticeStatus()
			if eid not in self.graph.keys():
				self.graph[eid] = XVerticeStatus()

			self.graph[sid].add_edge(XEdgeStatus(eid, weight))
			self.edge_num += 1
			if not self.directed_graph:
				self.graph[eid].add_edge(XEdgeStatus(sid, weight))
				self.edge_num += 1

			line = fp.readline()

		self.vertice_num = len(self.graph.keys())
		fp.close()
		return True

	def threshold_generator(self, alpha=0.8):
		"""
		TODO: place your own threshold generator here
		"""
		vertices = self.graph.keys()
		for vid in vertices:
			threshold = alpha * random.random()
			self.graph[vid].set_threshold(threshold)

	def weight_generator(self, beta=0.25):
		"""
		TODO: place your own weight generator here
		"""
		vertices = self.graph.keys()
		for vid in vertices:
			edges = self.graph[vid].get_edges()
			for i in xrange(len(edges)):
				weight = beta * random.random()
				edges[i].set_weight(weight)

			self.graph[vid].set_edges(edges)

	def mutation_factor_generator(self, theta=0.15):
		"""
		TODO: place your own mutation factor generator here
		"""
		vertices = self.graph.keys()
		for vid in vertices:
			mfactor = theta * random.random()
			self.graph[vid].set_mutation_factor(mfactor)

	def max_degree_neighbor(self, vertice, exclusive_set):
		edges = self.get_edges_by_vertice(vertice)
		nbrs = []
		for e in edges:
			nbrs.append(e.get_dest())
		nbrs.append(vertice)
		maximal, maxnode = -1, -1

		for u in nbrs:
			if u in exclusive_set:
				continue

			deg = len(self.get_edges_by_vertice(u))
			if maximal < deg:
				maximal = deg
				maxnode = u
				
		return maxnode

	def set_vertice_status(self, vertice, status):
		self.graph[vertice] = status

	def get_edge_num(self):
		if self.directed_graph:
			return self.edge_num
		return self.edge_num / 2

	def get_vertice_num(self):
		return self.vertice_num

	def get_all_vertices(self):
		return self.graph.keys()

	def get_edges_by_vertice(self, vertice):
		return self.graph[vertice].get_edges()

	def get_vertice_status(self, vertice):
		return self.graph[vertice]


class XDiffusionModel(object):
	def __init__(self):
		pass

	def calc_influence(self, graph, T, S):
		"""
		@T: seed set for company/product/idea A
		@S: seed set for company/product/idea B
		Computing influence diffusion for selecting T, S respectively
		"""
		resT, resS = [], []
		for t in T:
			# resT.append(t)
			status = graph.get_vertice_status(t)
			status.set_current_color(XCOLOR.RED)
			status.set_mutation_flag(True)
			status.red_visit_inc()

		for s in S:
			# resS.append(s)
			status = graph.get_vertice_status(s)
			status.set_current_color(XCOLOR.BLACK)
			status.set_mutation_flag(True)
			status.black_visit_inc()

		for t in T:
			edges = graph.get_edges_by_vertice(t)
			for e in edges:
				to = e.get_dest()
				status = graph.get_vertice_status(to)
				weight = e.get_weight()
				threshold = status.get_threshold()

				current_color = status.get_current_color()
				if current_color == XCOLOR.BLACK and not status.get_mutation_flag():
					r = random.random()
					if r < status.get_mutation_factor() and threshold < weight:
						resT.append(to)
						status.set_current_color(XCOLOR.RED)
						status.set_mutation_flag(True)
						status.red_visit_inc()
						# graph.set_vertice_status(to, status)
						continue

				if current_color != XCOLOR.GRAY or status.get_red_visit() > 0:
					continue

				if threshold < weight:
					resT.append(to)
					status.set_current_color(XCOLOR.RED)

				status.red_visit_inc()
				# graph.set_vertice_status(to, status)

		for s in S:
			edges = graph.get_edges_by_vertice(s)
			for e in edges:
				to = e.get_dest()
				status = graph.get_vertice_status(to)
				weight = e.get_weight()
				threshold = status.get_threshold()

				current_color = status.get_current_color()
				if current_color == XCOLOR.RED and not status.get_mutation_flag():
					r = random.random()
					if r < status.get_mutation_factor() and threshold < weight:
						resS.append(to)
						status.set_current_color(XCOLOR.BLACK)
						status.set_mutation_flag(True)
						status.black_visit_inc()
						# graph.set_vertice_status(to, status)
						continue

				if current_color != XCOLOR.GRAY or status.get_black_visit() > 0:
					continue

				if threshold < weight:
					resS.append(to)
					status.set_current_color(XCOLOR.BLACK)

				status.black_visit_inc()
				# graph.set_vertice_status(to, status)

		if len(resT) == 0 and len(resS) == 0:
			return len(T), len(S)

		t, s = self.calc_influence(graph, resT, resS)
		return t + len(T), s + len(S)


class XStrategies(object):
	def __init__(self, graph, model):
		self.graph = graph
		self.model = model

	def greedy(self, k):
		ft = time.time()
		S = []
		i = 0

		while i < k:
			vertices = self.graph.get_all_vertices()
			maxinf = -1
			target = -1
			for v in vertices:
				if v in S:
					continue

				Ss = copy.deepcopy(S)
				Ss.append(v)
				g = copy.deepcopy(self.graph)
				curS, _ = self.model.calc_influence(g, Ss, [])
				g = copy.deepcopy(self.graph)
				prevS, _ = self.model.calc_influence(g, S, [])
				if curS - prevS > maxinf:
					maxinf = curS - prevS
					target = v

			if target != -1:
				S.append(target)
				i += 1

		time_elapsed = time.time() - ft
		print '#Greedy Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

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

		time_elapsed = time.time() - ft
		print '#Degree Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

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

		time_elapsed = time.time() - ft
		print '#Comparable Heuristic Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

	def random_max_degree_neighbor(self, T):
		ft = time.time()
		nodes = self.graph.get_all_vertices()
		S = []
		i = 0
		# The get sample method is similar to the method we used in
		# 'A Budgeted Method for Influence Maximization' (XU Xinhui et al SEKE2015)
		while i < k:
			u = random.choice(nodes)
			es = list(set(T) | set(S))
			maxnode = self.graph.max_degree_neighbor(u, es)
			if maxnode == -1:
				continue
			S.append(maxnode)
			i += 1

		time_elapsed = time.time() - ft
		print 'RMDN Time consumed: %.2f secs' % (time_elapsed)
		return S, time_elapsed

	def infmax(self, k, R, result_file):
		ts = []
		res = []
		T, gtimes = self.greedy(k)

		S, dtimes = self.degree_heuristic(T)
		ts.append((T, S))
		res.append(('DegreeHeuristic', 0, 0, dtimes))

		S, ctimes = self.comparable_heuristic(T)
		ts.append((T, S))
		res.append(('ComparableHeuristic', 0, 0, ctimes))

		S, rtimes = self.random_max_degree_neighbor(T)
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
	print 'Creating a graph...'
	graph_file = '../../graphdata/USAir_unweight.txt'
	g = XGraph()
	g.load_graph_from_file(graph_file, '\t')
	print '#edge =', g.get_edge_num()
	print '#vertice =', g.get_vertice_num()
	print 'A graph generated successfully !'

	g.threshold_generator()
	g.weight_generator()
	g.mutation_factor_generator()

	m = XDiffusionModel()
	s = XStrategies(g, m)

	print 'Run the strategies...'
	for k in xrange(5):
		num = (k + 2) * 5
		result_file = "./result/usa" + str(num) + ".txt"
		s.infmax(num, 100, result_file)