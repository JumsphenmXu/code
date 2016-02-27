#!/usr/bin/python

__author__ = 'XU Xinhui'

import networkx as nx

class XGraphPricing(object):
	"""
	Pricing the given graph, namely giving every vertice a price tag according the 
	pricing strategy provided in 'A Balanced Method for Budgeted Influence Maximization'
	(XU Xinhui et al. SEKE2015)
	"""
	def __init__(self):
		pass

	def __load_graph(self, graph_file):
		graph = nx.Graph()

		with open(graph_file, "rb") as fp:
			for line in fp:
				nodes = line.split()
				u, v = long(nodes[0]), long(nodes[1])

				try:
					graph[u][v]['weight'] = 1
				except KeyError:
					graph.add_edge(u, v, weight=1)

		return graph

	def __get_pagerank_value(self, graph):
		return nx.pagerank(graph)

	def __max_degree_neighbor(self, graph, node, exclusive_set):
		nbrs = graph.neighbors(node)
		nbrs.append(node)
		maximal = -1
		max_node = -1

		for u in nbrs:
			if u in exclusive_set:
				continue

			deg = len(graph.neighbors(u))
			if maximal < deg:
				maximal = deg
				max_node = u

		return maximal, max_node

	def __cost_mapping(self, graph, rank_value):
		def cost_eval(item):
			maximal, max_node = self.__max_degree_neighbor(graph, item[0], [])
			return item[0], int((100*item[1]+50) * len(graph.neighbors(item[0])) / maximal)

		return map(cost_eval, rank_value)

	def pricing_graph(self, graph_file):
		graph = self.__load_graph(graph_file)
		rank_value = self.__get_pagerank_value(graph)
		rv = []
		for key, val in rank_value.items():
			rv.append((key, val))

		cost_list = self.__cost_mapping(graph, rv)
		graph_price = {}
		for e in cost_list:
			graph_price[e[0]] = e[1]

		return graph_price


if __name__ == '__main__':
	graph_file = '../../../graphdata/USAir_unweight.txt'
	pg = XGraphPricing()
	print pg.pricing_graph(graph_file)