#!/usr/bin/python

ROOT_PATH = './../'
DB_PATH = ROOT_PATH + 'db.pkl'

SERVER_NAME = 'localhost'
SERVER_IP = '127.0.0.1'
LISTEN_PORT = 12357
SERVER_ADDR = (SERVER_IP, LISTEN_PORT)

CMD_REGISTER =	0
CMD_LOGIN =	1
CMD_CHAT = 2
CMD_LOGOUT = 3
CMD_EXIT = 4