#!/home/umedoblock/local/bin/py3.3

# Copyright 2011-2014 梅濁酒(umedoblock)

import os

from iasap import Iasap
from iasap.iasap_tkinter import IasapTkinter
from iasap.iasap_curses import IasapCurses
from iasap import logger, start_logger
from iasap import set_kv_for_conf, set_kv_for_regular

class Iasap(object):
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
        self._py_ol.start()

def main():
    start_logger(__file__, os.path.curdir, logger.DEBUG)

    kv_tmp, kv_defaults, kv_argment = set_kv_for_conf()

    kv = set_kv_for_regular(kv_defaults, kv_argment, kv_tmp["conf"])

    if not os.path.isfile(kv["dbpath"]):
        raise OSError("cannot access \"{}\": No such file.".format(kv["dbpath"]))

    iasap = Iasap(kv["dbpath"], kv["limit"], kv["mode"])
    iasap.start()

if __name__ == '__main__':
    main()
