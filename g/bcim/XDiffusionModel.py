#!/usr/bin/python
#

__author__ = 'XU Xinhui'

import random
from XGraph import XCOLOR

class XDiffusionModel(object):
	def __init__(self):
		pass

	def calc_influence(self, graph, S, T, mutable=False):
		"""
		@graph: network graph
		@S: seed set for company/product/idea A
		@T: seed set for company/product/idea B
		@mutable: indicate whether the node in S and T can be mutated during the process
		Computing influence diffusion for selecting T, S respectively
		"""
		resS, resT = [], []
		for s in S:
			status = graph.get_vertice_status(s)
			status.set_current_color(XCOLOR.RED)
			if not mutable:
				status.set_mutation_flag(True)
			status.red_visit_inc()

		for t in T:
			status = graph.get_vertice_status(t)
			status.set_current_color(XCOLOR.BLACK)
			if not mutable:
				status.set_mutation_flag(True)
			status.black_visit_inc()

		for s in S:
			edges = graph.get_edges_by_vertice(s)
			for e in edges:
				dest = e.get_dest()
				status = graph.get_vertice_status(dest)
				color = status.get_current_color()

				if color == XCOLOR.RED or status.get_red_visit() > 0:
					continue

				if color == XCOLOR.BLACK and not status.get_mutation_flag():
					r = random.random()
					if r < status.get_mutation_factor():
						resS.append(dest)
						if dest in resT:
							resT.remove(dest)
						if dest in T:
							T.remove(dest)

						status.set_current_color(XCOLOR.RED)
						status.set_mutation_flag(True)
						status.red_visit_inc()
						continue

				weight = 0.0
				threshold = status.get_threshold()
				tedges = graph.get_edges_by_vertice(dest)
				for te in tedges:
					v = te.get_dest()
					c = graph.get_vertice_status(v).get_current_color()
					if c == XCOLOR.RED:
						weight += te.get_weight()

				if threshold < weight:
					resS.append(dest)
					status.set_current_color(XCOLOR.RED)

				status.red_visit_inc()

		for t in T:
			edges = graph.get_edges_by_vertice(t)
			for e in edges:
				dest = e.get_dest()
				status = graph.get_vertice_status(dest)
				color = status.get_current_color()

				if color == XCOLOR.BLACK or status.get_black_visit() > 0:
					continue

				if color == XCOLOR.RED and not status.get_mutation_flag():
					r = random.random()
					if r < status.get_mutation_factor():
						resT.append(dest)
						if dest in resS:
							resS.remove(dest)
						if dest in S:
							S.remove(dest)

						status.set_current_color(XCOLOR.BLACK)
						status.set_mutation_flag(True)
						status.black_visit_inc()
						continue

				weight = 0.0
				threshold = status.get_threshold()
				tedges = graph.get_edges_by_vertice(dest)
				for te in tedges:
					v = te.get_dest()
					c = graph.get_vertice_status(v).get_current_color()
					if c == XCOLOR.BLACK:
						weight += te.get_weight()

				if threshold < weight:
					resT.append(dest)
					status.set_current_color(XCOLOR.BLACK)

				status.black_visit_inc()

		if len(resS) == 0 and len(resT) == 0:
			return len(S), len(T)

		s, t = self.calc_influence(graph, resS, resT, True)
		return s + len(S), t + len(T)
