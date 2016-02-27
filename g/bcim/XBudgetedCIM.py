#!/usr/bin/python

__author__ = 'XU Xinhui'

from XGraph import XGraph
from XDiffusionModel import XDiffusionModel
from XStrategy import XStrategy
from XGraphPricing import XGraphPricing

class XBudgetedCIM(object):
	def __init__(self, graph_file, model, strategy):
		self.graph_file = graph_file
		self.model = model
		self.strategy = strategy
		self.graph = XGraph()
		self.graph.load_graph_from_file(graph_file)
		self.graph.threshold_generator()
		self.graph.weight_generator()
		self.graph.mutation_factor_generator()

	def pricing_graph(self):
		gp = XGraphPricing()
		return gp.pricing_graph(self.graph_file)

	def greedy(self, graph, T, budget):
		pass

	def degree_heuristic(self, graph, T, budget):
		pass

	def comparable_heuristic(self, graph, T, budget):
		pass