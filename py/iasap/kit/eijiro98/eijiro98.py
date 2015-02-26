#!/home/umedoblock/local/bin/py3.3

# Copyright 2011-2014 梅濁酒(umedoblock)

import os, sys

def append_parent_dir(n_up):
    here = os.path.abspath(__file__)
    ups = ""
    if n_up:
        ups = os.path.join(*([".."] * n_up))
    _parent_dir = os.path.join(os.path.dirname(here), ups)
    sys.path.append(_parent_dir)

append_parent_dir(2)

__file__ = os.path.abspath(__file__)
dirname = os.path.dirname(__file__)

from iasap import Iasap
from iasap.iasap_tkinter import IasapTkinter
from iasap.iasap_curses import IasapCurses
from iasap import logger, start_logger
from iasap import merge_kv_by_defaults_and_argument, set_kv_for_regular

class Eijiro98(object):
    DEFAULTS = {
        "conf": os.path.join(dirname, "..", "eijiro98.conf"),
        "dbpath": os.path.join(dirname, "..", 'eijiro98.sqlite3'),
        "mode": "tkinter",
        "limit": 30,
        "debug": False,
    }

    def __init__(self, dbpath, limit, mode):
        iasap = Iasap(dbpath, limit)
        if mode == 'curses':
            _iasap = IasapCurses()
        elif mode == 'tkinter':
            _iasap = IasapTkinter()
        else:
            logger.debug("mode = \"{}\"".format(mode))
            raise ValueError('mode="{}" must be "curses" or "tkinter".'.format(mode))
        _iasap.get_body = iasap.get_body
        self._iasap = _iasap

    def start(self):
        self._iasap.start()

def main():
    start_logger(__file__, os.path.curdir, logger.DEBUG)

    kv_merged, kv_defaults, kv_argment = \
        merge_kv_by_defaults_and_argument(Eijiro98.DEFAULTS)

    kv = set_kv_for_regular(kv_defaults, kv_argment, kv_merged["conf"])

    if not os.path.isfile(kv["dbpath"]):
        raise OSError("cannot access \"{}\": No such file.".format(kv["dbpath"]))

    eijiro98 = Eijiro98(kv["dbpath"], kv["limit"], kv["mode"])
    eijiro98.start()

if __name__ == '__main__':
    main()
