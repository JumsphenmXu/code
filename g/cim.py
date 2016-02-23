#!/usr/bin/python

import random

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
		self.edges.push(e)

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
			weight = beta * random.random()
			self.graph[vid].set_weight(weight)

	def mutation_factor_generator(self, theta=0.15):
		"""
		TODO: place your own mutation factor generator here
		"""
		vertices = self.graph.keys()
		for vid in vertices:
			mfactor = theta * random.random()
			self.graph[vid].set_mutation_factor(mfactor)

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


class XDiffuseModel(object):
	def __init__(self):
		pass

	def calc_influence(self, graph, T, S):
		"""
		@T: seed set for company/product/idea A
		@S: seed set for company/product/idea B
		Computing influence diffusion for selecting T, S respectively
		"""
		resT, resS, = [], []
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
					if r < status.get_mutation_factor() and threshold < r * weight:
						resT.push(to)
						status.set_current_color(XCOLOR.RED)
						status.set_mutation_flag(True)
						status.red_visit_inc()
						graph.set_vertice_status(status)
						continue

				if current_color != XCOLOR.GRAY or status.get_red_visit() > 0:
					continue

				
				if threshold < weight * random.random():
					resT.push(to)
					status.set_current_color(XCOLOR.RED)

				status.red_visit_inc()
				graph.set_vertice_status(vertice, status)

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
					if r < status.get_mutation_factor() and threshold < r * weight:
						resS.push(to)
						status.set_current_color(XCOLOR.BLACK)
						status.set_mutation_flag(True)
						status.black_visit_inc()
						graph.set_vertice_status(status)
						continue

				if current_color != XCOLOR.GRAY or status.get_black_visit() > 0:
					continue

				if threshold > weight * random.random():
					resS.push(to)
					status.set_current_color(XCOLOR.BLACK)

				status.black_visit_inc()
				graph.set_vertice_status(vertice, status)

		if len(T) == len(resT) and len(S) == len(resS):
			return len(T), len(S)

		return self.calc_influence(graph, resT, resS)


class XStrategies(object):
	def __init__(self, graph, model):
		self.graph = graph
		self.model = model

	def greedy(self, k):
		T, S = [], []
		i = 0
		while i < 2 * k:
			TS = list(set(T) | set(S))
			vertices = self.graph.get_all_vertices()
			maxinf = -1
			target = -1
			for v in vertices:
				if v in TS:
					continue
				Tt, Ss = T, S
				if i % 2 == 0:
					Tt.push(v)
				else:
					Ss.push(v)

				g = self.graph
				tcntx, scntx = self.model.calc_influence(g, Tt, Ss)
				g = self.graph
				tcnt, scnt = self.model.calc_influence(g, T, S)
				if i % 2 == 0:
					if tcntx - tcnt > maxinf:
						maxinf = tcntx - tcnt
						target = v
				else:
					if scntx - scnt > maxinf:
						maxinf = scntx - scnt
						target = v
			if target != -1:
				if i % 2 == 0:
					T.push(target)
				else:
					S.push(target)
			i += 1

		return T, S



	def degree_heuristic(self, k):
		out_degree = []
		vertices = self.graph.get_all_vertices()
		for vid in vertices:
			out_degree.push((vid, len(self.graph[vid].get_edges())))

		out_degree_sorted = sorted(out_degree, key=lambda x: x[1], reversed=True)

		T, S = [], []
		limit, i = 2 * k, 0
		if limit > len(out_degree_sorted):
			limit = len(out_degree_sorted) / 2
			limit *= 2

		while i < limit:
			T.push(out_degree_sorted[i][0])
			S.push(out_degree_sorted[i+1][0])
			i += 2

		return T, S

if __name__ == '__main__':
	print 'Creating a graph...'
	g = XGraph()
	print 'A graph generated successfully !'