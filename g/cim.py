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

	def add_edge(self, e):
		self.edges.push(e)

	def del_edge(self, e):
		if e in self.edges:
			self.edges.remove(e)

	# getters for attributes
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

	def load_graph_from_file(self, file_name, seperator=" "):
		fp = open(file_name, "rb")
		if not fp:
			print 'Failed to open file %s !!!' % file_name
			return False

		line = fp.readline()
		while line:
			units = line.split(seperator)
			weight = 1.0
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

	def __threshold_generator(self):
		"""
		TODO: place your own threshold generator here
		"""
		pass

	def __weight_generator(self):
		"""
		TODO: place your own weight generator here
		"""
		pass

	def __mutation_factor_generator(self):
		"""
		TODO: place your own mutation factor generator here
		"""
		pass

	def get_edge_num(self):
		if self.directed_graph:
			return self.edge_num
		return self.edge_num / 2

	def get_vertice_num(self):
		return self.vertice_num


class XStrategies(object):
	def __init__(self, graph):
		self.graph = graph


	def greedy(self):
		pass

	def heuristic(self):
		pass
		

if __name__ == '__main__':
	g = XGraph("g.txt")