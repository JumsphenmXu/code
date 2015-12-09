#!/usr/bin/python

import sys, socket

if __name__ == '__main__':
	import socket, sys
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv_addr = ('166.111.134.46', 9111)
	sock.connect(serv_addr)
	sock.sendall('say hi to xinhui')