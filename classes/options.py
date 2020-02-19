#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import tornado.options
# from tornado.log import define_logging_options

# 3rd-party Packages


# Local Packages


# CONST


# Class & Function Definition
# class OptionParser(tornado.options.OptionParser):
#     def set(self, name, key, value):
#         self._options[name].update(key, value)
# options = OptionParser()
options = tornado.options.options
tornado.options.define(
    "config-file",
    group="",
    default="/usr/local/etc/tornado.conf",
    help=(
        "Path to config file. The options in config file will override options set earlier on the command line, "
        "but can be overridden by later flags."
    ),
    callback=lambda path: options.parse_config_file(path, final=False)
)
tornado.options.define(
    "debug",
    group="",
    default=False,
    help=(
        "Run program in debug mode. If true, the logging level is forced to debug"
    ),
    metavar="True|False"
)

# Logic
print(1)
options.parse_config_file('conf/tornado.conf')
print(2)
options.parse_command_line()

