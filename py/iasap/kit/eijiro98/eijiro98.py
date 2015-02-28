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
