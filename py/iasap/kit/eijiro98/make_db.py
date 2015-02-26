# Copyright 2011-2014 梅濁酒(umedoblock)

import sqlite3
import argparse
import configparser
import re
import os

from iasap.sql import GeneralSQLConnection

parser = argparse.ArgumentParser(description='python dictionary')

parser.add_argument('--dicpath', metavar='f', dest='dicpath',
                    nargs=1,
                    default='./iasap/eijiro98.txt',
                    help='eijiro dicpath')
parser.add_argument('--dbpath', metavar='f', dest='dbpath',
                    nargs='?',
                    default='./iasap.sqlite3',
                    help='sqlite dbpath')
parser.add_argument('--table-name', metavar='t', dest='table_name',
                    required=True,
                    default='eijiro98',
                    help='table name')
parser.add_argument('--schema', metavar='f', dest='schema',
                    nargs=1,
                    default='./iasap/eijiro98.schema',
                    help='database schema')
parser.add_argument('--debug', dest='debug',
                   action='store_true', default=False,
                   help='use debug ? (default: False)')

args = parser.parse_args()
dicpath = args.dicpath
print('args.dicpath =', dicpath)
if not dicpath:
    raise ValueError('dicpath muse be available dicpath')
dbpath = args.dbpath
print('args.dbpath =', dbpath)
if not dbpath:
    raise ValueError('dbpath muse be available path')
schema = args.schema
print('args.schema =', schema)
if not schema:
    raise ValueError('schema muse be available path')

dicpath = os.path.expanduser(dicpath)
dbpath = os.path.expanduser(dbpath)
schema = os.path.expanduser(schema)

config = configparser.ConfigParser()
config.read(schema)
conn = sqlite3.connect(dbpath)
conn = GeneralSQLConnection(conn)
try:
    conn.create_table(config['eijiro98'])
except sqlite3.OperationalError as raiz:
    if raiz.args[0] != 'table eijiro98 already exists':
        raise sqlite3.OperationalError(*raiz.args)

with open(dicpath, encoding='utf8') as f:
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
        conn.insert('eijiro98', column)
conn.close()
