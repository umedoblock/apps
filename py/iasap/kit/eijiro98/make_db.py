# Copyright 2011-2014 梅濁酒(umedoblock)

import sqlite3
import argparse
import configparser
import re
import os

import lib
lib.sys_path_append_parent_dir(2)
from iasap.sql import GeneralSQLConnection
from iasap.lib import start_logger, logger

from eijiro98 import Eijiro98

start_logger(os.path.basename(__file__), os.path.curdir, logger.DEBUG)

parser = argparse.ArgumentParser(description='make eijiro98 database.')

parser.add_argument('--txtpath', metavar='f', dest='txtpath',
                    required=True,
                    help='eijiro98.txt path')
parser.add_argument('--dbpath', metavar='f', dest='dbpath',
                    nargs='?',
                    default=Eijiro98.DEFAULTS["dbpath"],
                    help='default: eijiro98.sqlite')
parser.add_argument('--table-name', metavar='t', dest='table_name',
                    default='eijiro98',
                    help='default table name is eijiro98.')
parser.add_argument('--conf', metavar='f', dest='conf',
                    nargs=1,
                    default=Eijiro98.DEFAULTS["conf"],
                    help='eijiro98.conf default is {}'.format( \
                          Eijiro98.DEFAULTS["conf"]))
parser.add_argument('--debug', dest='debug',
                   action='store_true', default=False,
                   help='use debug ? (default: False)')

args = parser.parse_args()
txtpath = args.txtpath
print('args.txtpath =', txtpath)
if not txtpath:
    raise ValueError('txtpath muse be available txtpath')
dbpath = args.dbpath
print('args.dbpath =', dbpath)
if not dbpath:
    raise ValueError('dbpath muse be available path')
conf = args.conf
print('args.conf =', conf)
if not conf:
    raise ValueError('conf muse be available path')

txtpath = os.path.expanduser(txtpath)
dbpath = os.path.expanduser(dbpath)
confpath = os.path.expanduser(conf)

if os.path.isfile(dbpath):
    print("dbpath として指定した path には既に、file が存在します。")
    print(dbpath)
    s = input("を削除しますか？ 削除するなら、yes を入力してください。->: ")

    if s.lower() == "yes":
        os.remove(dbpath)
    else:
        raise ValueError("dbpath に適切な値を入力して下さい。")

config = configparser.ConfigParser()
config.read(confpath)
conn_sqlite3 = sqlite3.connect(dbpath)
conn = GeneralSQLConnection(conn_sqlite3)
try:
    conn.create_table(config['schema'])
except sqlite3.OperationalError as raiz:
    if raiz.args[0] != 'table {} already exists'.format(args.table_name):
        raise sqlite3.OperationalError(*raiz.args)

with open(txtpath, encoding='utf8') as f:
    for l in f:
        l = l.strip()
      # print(l)
        head, tail = re.findall('(.*) /// (.*)', l)[0]
      # prefix, v0 = parse_head(head)
      # v1, suffix = parse_tail(tail)
      # print(prefix, v0, v1, suffix, sep='|')
      # print(head, tail, sep='|')
        column = \
            {'id': None, 'head': head, 'tail': tail}
        conn.insert(args.table_name, column)
conn.close()
