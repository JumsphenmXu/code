#!/usr/bin/python


import random


class XCOLOR(object):
	BLACK = 0
	RED = 1
	GRAY = 2

	def __init__(self):
		pass


class XVertice(object):
	def __init__(self, vertice_id, threshold=0.0, mutation_flag=False, mutation_factor=0.0, current_color=XCOLOR.GRAY):
		self.vertice_id = vertice_id
		self.threshold = threshold
		self.mutation_flag = mutation_flag
		self.mutation_factor = mutation_factor
		self.current_color = current_color

	# getters for attributes
	def get_vertice_id(self):
		return self.vertice_id

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
	def __init__(self, file_name, seperator=" ", directed=False):
		self.edges = {}
		self.edge_num = 0
		self.vertice_num = 0
		self.default_weight = False
		self.directed = directed
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
				self.default_weight = True
				weight = float(units[2])

			sid = int(units[0])
			eid = int(units[1])
			
			if sid not in self.edges.keys():
				self.edges[sid] = []
			
			if eid not in self.edges.keys():
				self.edges[eid] = []

			self.edges[sid].push(XEdge(XVertice(sid), XVertice(eid), weight))
			self.edge_num += 1
			if not self.directed:	
				self.edges[eid].push(XEdge(XVertice(eid), XVertice(sid), weight))
				self.edge_num += 1

			line = fp.readline()

		self.vertice_num = len(self.edges.keys())
		fp.close()
		return True

	def __threshold_generator(self):
		pass

	def __weight_generator(self):
		pass

	def __mutation_factor_generator(self):
		pass

	def get_edge_num(self):
		if self.directed:
			return self.edge_num
		return self.edge_num / 2

	def get_vertice_num(self):
		return self.vertice_num


if __name__ == '__main__':
	g = XGraph("g.txt")