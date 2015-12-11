#!/usr/bin/python

import os, sys, inspect

projectDIR = os.path.realpath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
if projectDIR not in sys.path:
	sys.path.insert(0, projectDIR)