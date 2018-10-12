#!/usr/bin/python3

# Copyright 2011-2015 梅濁酒(umedoblock)

import os

import lib

lib.sys_path_append_parent_dir(__file__, 2)

__file__ = os.path.abspath(__file__)
dirname = os.path.dirname(__file__)

import iasap

class Eijiro98(iasap.Iasap):
    DEFAULTS = {
        "conf": os.path.join(dirname, "eijiro98.conf"),
        "dbpath": os.path.join(dirname, 'eijiro98.sqlite3'),
        "mode": "tkinter",
        "limit": 30,
        "debug": False,
    }

if __name__ == '__main__':
    iasap.main(Eijiro98, os.path.basename(__file__), "eijiro98")
