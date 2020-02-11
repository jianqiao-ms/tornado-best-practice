#! /usr/bin/env python
# -* coding: utf-8 -*


# Official packages
from tornado.options import define, options
# 3rd-party Packages


# Local Packages


# CONST


# Class & Function Definition

define(
    "config-file",
    group="",
    default="/usr/local/etc/tornado.conf",
    help=(
        "Path to config file. The options in config file will override options set earlier on the command line, "
        "but can be overridden by later flags."
    ),
    callback=lambda path: options.parse_config_file(path, final=False)
)
define(
    "debug",
    group="",
    default=False,
    help=(
        "Run program in debug mode. If true, the logging level is forced to debug"
    ),
    metavar="True|False"
)

# Logic
options.parse_config_file('conf/tornado.conf')
options.parse_command_line()

