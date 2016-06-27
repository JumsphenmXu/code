#!/usr/bin/python

SERVER_IP='127.0.0.1'
SERVER_PORT=23233
SERVER_ADDR=(SERVER_IP, SERVER_PORT)


DB_USER='./../data/dbuser.pkl'
DB_WEAPON='./../data/dbweapon.pkl'
DB_GAME_INFO='./../data/dbgameinfo.pkl'


BASE_LEVEL_EXP = 1000
LEVEL_INC_FACTOR = 1.4
INFINITY_EXP = (1 << 30)
