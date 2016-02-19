#!/usr/bin/python


import random


class XEdge(object):
	def __init__(self, start, end, weight=1.0):
		self.start = start
		self.end = end
		self.weight = weight


	def get_start(self):
		return self.start


	def set_start(self, start):
		self.start = start


	def get_end(self):
		return self.end


	def set_end(self, end):
		self.end = end


	def get_weight(self):
		return self.weight


	def set_weight(self, weight):
		self.weight = weight


class XGraph(object):
	def __init__(self, file_name, seperator=" "):
		self.edges = []
		self.edge_num = 0
		self.vertice_num = 0
		self.vertices_threshold = {}
		self.default_weight = True
		ok = self.load_graph_from_file(file_name, seperator)
		if not ok:
			print 'Failed to load the graph from file %s !!!' % file_name
			exit()


	def load_graph_from_file(self, file_name, seperator):
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
				self.default_weight = False
				weight = float(units[2])

			start = int(units[0])
			end = int(units[1])
			edge = XEdge(start, end, weight)
			self.edges.push(edge)
			self.edge_num += 1
			self.vertices_threshold[start] = 0.0
			self.vertices_threshold[end] = 0.0
			self.vertice_num = len(self.vertices_threshold.keys())
			line = fp.readline()

		fp.close()
		self.__threshold_generator()
		if not self.default_weight:
			self.__weight_generator()

		return True


	def __threshold_generator(self):
		vertices = self.vertices_threshold.keys()
		for v in vertices:
			self.vertices_threshold[v] = 0.33 * random.random()


	def __weight_generator(self):
		for i in xrange(self.edge_num):
			self.edge[i].set_weight(0.1 * random.random())


	def get_edge_num(self):
		return self.edge_num


	def get_vertice_num(self):
		return self.vertice_num


if __name__ == '__main__':
	g = XGraph("g.txt")