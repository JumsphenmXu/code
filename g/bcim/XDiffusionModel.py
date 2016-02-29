#!/usr/bin/python
#

__author__ = 'XU Xinhui'

import random
from XGraph import XCOLOR

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
