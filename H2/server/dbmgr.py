#!/usr/bin/python

import socket, sys, os, inspect, pickle, json
CUR_PATH = os.path.abspath(inspect.getfile(inspect.currentframe()))
PROJECT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
if PROJECT_PATH not in sys.path:
	sys.path.insert(0, PROJECT_PATH)
from conf import conf


class DbMgr(object):
	def __init__(self, grps={}, all_members=[], all_fileno=[]):
		# grps: mapping gid to group socket list
		# eg. grps[gid] = [sock_1, sock_2, sock_3,...,sock_n]
		self.grps = grps

		# all_members: a list of socket that existed in the very moment
		# eg. all_members = [sock_1, sock_2, sock_3,...,sock_n]
		self.all_members = all_members

		# user_info: a list of tuple of (username, password)
		# eg. user_info = [(username_1, password_1), (username_2, password_2),...(username_n, password_n)]
		self.user_info = []


	def load_data(self):
		fp = open(conf.USER_INFO_DATA)
		try:
			self.user_info = pickle.load(fp)
		except:
			self.user_info = []
		fp.close()


	def dump_data(self):
		fp = open(conf.USER_INFO_DATA)
		pickle.dump(fp, -1)
		fp.close()
		

	def add_member_to_grp(self, gid, member):
		if gid not in self.grps.keys():
			self.grps[gid] = [member]
		
		if member in self.grps[gid]:
			print '\n[WARN] add_member_to_grp failed !!!'
			print '[INFO] member (fileno = %d) already in the group !!!\n' % member.fileno()
			return

		self.grps[gid].append(member)


	def del_member_from_grp(self, gid, member):
		if gid not in self.grps.keys():
			print '\n[WARN] del_member_from_grp failed !!!'
			print '[INFO] can not find the group id (gid = %d) !!!\n' % gid
			return

		if member in self.grps[gid]:
			self.grps[gid].remove(member)
			return

		print '\n[WARN] del_member_from_grp failed !!!'
		print '[INFO] member (fileno = %d) is not in the group !!!\n' % member.fileno()


	def add_member(self, member):
		if member in self.all_members:
			print '\n[WARN] add_member failed !!!'
			print '[INFO] member (fileno = %d) already in the group !!!\n' % member.fileno()
			return

		self.all_members.append(member)


	def del_member(self, member):
		if member in self.all_members:
			self.all_members.remove(member)

		print '\n[WARN] del_member failed !!!'
		print '[INFO] member (fileno = %d) does not existed in the member list !!!\n' % member.fileno()


	def add_user(self, username, password):
		for i in xrange(len(self.user_info)):
			if username == self.user_info[i][0]:
				print '\n[WARN] add_user failed !!!'
				print '[INFO] user (username = %s) already existed !!!\n' % username
				return

		self.user_info.append((username, password))


	def del_user(self, username):
		for i in xrange(len(self.user_info)):
			if username == self.user_info[i][0]:
				self.user_info.remove(self.user_info[i])
				return
		print '\n[WARN] del_user failed !!!'
		print '[INFO] No such user (username = %s) to remove !!!\n' % username