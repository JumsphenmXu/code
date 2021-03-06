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
	def __init__(self, src, dest, weight):
		self.src = src
		self.dest = dest
		self.weight = weight

	def get_dest(self):
		return self.dest

	def get_src(self):
		return self.src

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

			self.graph[sid].add_edge(XEdgeStatus(sid, eid, weight))
			self.edge_num += 1
			if not self.directed_graph:
				self.graph[eid].add_edge(XEdgeStatus(eid, sid, weight))
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
