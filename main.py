#! /usr/bin/env python3
# -* coding: utf-8 -*

# Official packages


# 3rd-party Packages
import tornado.options
from tornado.log import *
# from tornado.options import options, define

# Local Packages
import classes.options

# CONST


# Class & Function Definition


# Logic
# define('debug', default=True, help='enable debug mode')
# define('port', default=8888, help='run on this port', type=int)

# 从命令行中解析参数信息， 如 python web.py --port=9002, 这里的port解析

print(tornado.options.options.debug)