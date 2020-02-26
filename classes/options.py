#! /usr/bin/env python3
# -* coding: utf-8 -*

"""
Overwrite  tornado.options.OptionParser.
  * make define() failed without specific group -- thus print_help() looks better
  * create ALL_GROUPS arguments. Prevent define a mistake group.
  * make parse_config_file() able to parse a .ini like file. With group name supported TODO
Create new type OptionParserWithDefaultGroup
  * make it possible to update all logging options in tornado.log have a same group named "logging". Yes, this is a 
    important move for a better looks of print_help()
"""


# Official packages
import re
import os, sys, logging
from typing import Any, Iterator, Iterable, Tuple, Set, Dict, Callable, List, TextIO
from tornado.options import OptionParser as OfficialOptionParser
from tornado.options import _Option
from tornado.options import exec_in
from tornado.escape import _unicode, native_str
from tornado.log import define_logging_options
# from tornado.log import define_logging_options

# 3rd-party Packages


# Local Packages


# CONST
COMMENT_CHAR = "#"
ALL_GROUPS = [
    "global",
    "logging",
    "database"
]

# Class & Function Definition
class OptionParser(OfficialOptionParser): 
    """Overwrite tornado.options.OptionParser

    Updated:
        Method define -> Disabled without group name
    """
    def define(
        self,
        name: str,
        default: Any = None,
        type: type = None,
        help: str = None,
        metavar: str = None,
        multiple: bool = False,
        group: str = None,
        callback: Callable[[Any], None] = None,
    ) -> None:
        normalized = self._normalize_name(name)
        if normalized in self._options:
            raise Exception(
                "Option %r already defined in %s"
                % (normalized, self._options[normalized].file_name)
            )
        frame = sys._getframe(0)
        options_file = frame.f_code.co_filename

        # Can be called directly, or through top level define() fn, in which
        # case, step up above that frame to look for real caller.
        if (
            frame.f_back.f_code.co_filename == options_file
            and frame.f_back.f_code.co_name == "define"
        ):
            frame = frame.f_back

        file_name = frame.f_back.f_code.co_filename
        if file_name == options_file:
            file_name = ""
        if type is None:
            if not multiple and default is not None:
                type = default.__class__
            else:
                type = str
        if not group in ALL_GROUPS and not normalized == "help":
            raise Exception(
                "Group %r of %r defined in %s invalid"
                % (group, normalized, file_name)
        )
        if group:
            group_name = group  # type: Optional[str]
            option = _Option(
                name,
                file_name=file_name,
                default=default,
                type=type,
                help=help,
                metavar=metavar,
                multiple=multiple,
                group_name=group_name,
                callback=callback,
            )
            self._options[normalized] = option
        else:
            if not normalized == 'help':
                raise Exception(
                    "Option %r defined in %s did not have a group name"
                    % (normalized, file_name)
                )

    def parse_config_file(self, path: str, final: bool = True) -> None:
        """
        Make it possible write a config file with a group define.
        Group is defined like [GROUP].
        The first valid option line(not start with a COMMENT_CACR) of a file must be a [GROUP], or this method will 
            raise an Exception.

        The config dict is diffrent with the official one. In the official config dict, config keys are group name with 
            a value of option evaluation string(or bytes), keys are option names defined in define(). I am not talking 
            the key "__file__".
        """
        config = {"__file__": os.path.abspath(path)}
        with open(path, "rb") as f:
            """
            Put all option evaluation in groups
            """
            CURRENT_GROUP = None
            for cnt, line in enumerate(f):
                if line.decode().startswith(COMMENT_CHAR):
                    continue
                matchObj = re.match(r'^\[([a-zA-Z]+)\]$', line.decode())
                """
                Using module re to check if this line representate a GROUP
                """
                if matchObj:
                    CURRENT_GROUP = matchObj.group(1).lower()
                    config[CURRENT_GROUP] = {}
                else:
                    if not CURRENT_GROUP:
                        """
                        Define options before any group is decleared is not permmited
                        """
                        raise Exception(
                            "Invalid configuration in file %r, line %r\n \
                            \rNo group assigned"
                            % (config["__file__"], cnt)
                        )
                    exec_in(native_str(line), config[CURRENT_GROUP], config[CURRENT_GROUP])
            logging.info('Config in parse_config_file:{}'.format(config))
        for gname in config:
            """
            gname: group name
            Of course variable gname may be '__file__' or other values, the it works as group name, and it's useful only
                when it is a group name in this for statement.
            """
            normalized = self._normalize_name(gname)
            if normalized.startswith("-"):
                continue
            if not gname in ALL_GROUPS:
                """
                Prevent mistake group-name being parsed
                """
                raise Exception(
                    "Invalid group name [%r] in config file %r" 
                    %(gname, config["__file__"])
                )
            for name in config[gname]:
                """
                Here I start the official option evaluation process, but still difference exsits. There is an 
                addtion step to verifiy the group, check if the option is configed in proper group.
                """
                normalized = self._normalize_name(name)
                if normalized in self._options:
                    option = self._options[normalized]
                    if option.multiple:
                        if not isinstance(config[name], (list, str)):
                            raise Exception(
                                "Option %r is required to be a list of %s "
                                "or a comma-separated string"
                                % (option.name, option.type.__name__)
                            )
                    if not option.group_name == gname:
                        raise Exception(
                            "Option %r is in a wrong group [%r]\n\r \
                            It's belone to group [%r]"
                            %(name, gname, option.group_name)
                        )
                    if type(config[gname][name]) == str and option.type != str:
                        option.parse(config[gname][name])
                    else:
                        option.set(config[gname][name])
            

        if final:
            self.run_parse_callbacks()



class OptionParserWithDefaultGroup(OptionParser): 
    """
    OptionParser with a default group
    Init create just for tornado.log.define_logging_options
    """
    def __init__(self, group: str) -> None:
        self.__dict__['default_group_name'] = {'str': group}
        super(OptionParserWithDefaultGroup, self).__init__()

    def define(self, *args, **kwargs):
        super(OptionParserWithDefaultGroup, self).define(*args, **kwargs, group=self.__dict__['default_group_name']["str"])


options = OptionParser()
options_logging = OptionParserWithDefaultGroup("logging")

# Change --logging* options group to "logging"
define_logging_options(options_logging)
options._options.update(options_logging._options)

options.parse_command_line()
options.parse_config_file('/home/jianqiao.ms/workspace/tornado-best-practice/conf/tornado.conf')


if __name__ == "__main__":
    print(options.log_file_max_size)
    print(options.group_dict('logging'))
