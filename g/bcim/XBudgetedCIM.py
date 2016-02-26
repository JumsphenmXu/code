#!/usr/bin/python

__author__ = 'XU Xinhui'

from XGraph import XGraph
from XDiffusionModel import XDiffusionModel
from XStrategy import XStrategy
from XGraphPricing import XGraphPricing

class XBudgetedCIM(object):
	def __init__(self):
		pass

	def pricing_graph(self, graph_file):
		gp = XGraphPricing()

	def greedy(self, graph, T, budget):
		pass

	def degree_heuristic(self, graph, T, budget):
		pass

	def comparable_heuristic(self, graph, T, budget):
		pass