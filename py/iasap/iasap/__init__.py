# Copyright 2011-2014 梅濁酒(umedoblock)

__all__ = ['IasapCurses', 'IasapTkinter']

import sqlite3, os, sys, datetime, argparse
import configparser

from iasap.iasap_tkinter import IasapTkinter
from iasap.iasap_curses import IasapCurses
from iasap.sql import GeneralSQLConnection
from iasap.lib import logger, start_logger

def main(cls, table_name):
    start_logger(__file__, os.path.curdir, logger.DEBUG)

    kv_merged, kv_defaults, kv_argment = \
        merge_kv_by_defaults_and_argument(cls.DEFAULTS)

    kv = set_kv_for_regular(kv_defaults, kv_argment, kv_merged["conf"], table_name)

    if not os.path.isfile(kv["dbpath"]):
        raise OSError("cannot access \"{}\": No such file.".format(kv["dbpath"]))

    iasap_obj = cls(kv["dbpath"], table_name, kv["mode"], kv["limit"])
    logger.debug("iasap_obj = {}".format(iasap_obj))
    iasap_obj.start()

def _merge_kv(first, second, third={}):
    kv = {}
    for k, v in first.items():
        kv[k] = v
    for k, v in second.items():
        kv[k] = v
    for k, v in third.items():
        kv[k] = v
    logger.debug("kv in _merge_kv() =")
    logger.debug(kv)
    logger.debug("\n")
    return kv

def _get_kv_by_conf(path, section):
    logger.debug("path =")
    logger.debug(path)
    with open(path) as f:
        config = configparser.ConfigParser()
        config.read_file(f, section)
    kv = {}
    for key, value in config[section].items():
        if value:
            kv[key] = value
    if kv["limit"]:
        kv["limit"] = int(kv["limit"])
    logger.debug("kv in _get_kv_by_conf() =")
    logger.debug(kv)
    logger.debug("\n")
    return kv

if os.path.islink(__file__):
    __file__ = os.path.realpath(__file__)
__file__ = os.path.abspath(__file__)
dirname = os.path.dirname(__file__)

DEFAULTS = {
    "conf": os.path.join(dirname, "..", "iasap.conf"),
    "dbpath": os.path.join(dirname, "..", 'iasap.sqlite3'),
    "mode": "tkinter",
    "limit": 30,
    "debug": False,
}

def _set_kv_by_defaults(defaults=None):
    logger.debug("kv in _set_kv_by_defaults() =")
    logger.debug(defaults)
    logger.debug("\n")
    return defaults

def merge_kv_by_defaults_and_argument(defaults=None):
    kv_defaults = _set_kv_by_defaults(defaults)
    kv_argment = _get_kv_by_argument(defaults)
    kv_tmp = _merge_kv(kv_defaults, kv_argment)
    return kv_tmp, kv_defaults, kv_argment

def set_kv_for_regular(kv_defaults, kv_argment, conf_path, section):
    kv_conf = _get_kv_by_conf(conf_path, section)
    kv = _merge_kv(kv_defaults, kv_conf, kv_argment)
    return kv

def _get_kv_by_argument(defaults=None):
    parser = argparse.ArgumentParser(description='argment.')

    parser.add_argument('--conf', metavar='f', dest='conf',
                       default=defaults["conf"],
                       help='conf path default is {}.'.format(defaults["conf"]))
    parser.add_argument('--dbpath', metavar='f', dest='dbpath',
                       default=defaults["dbpath"],
                       help='sqlite dbpath default is {}'.format(defaults["dbpath"]))
    parser.add_argument('--mode', metavar='s', dest='mode',
                       default=defaults["mode"],
                       help='iasap default mode is tkinter, mode is tkinter, curses or one-shot.')
    parser.add_argument("--limit", metavar="N", dest="limit",
                         type=int, default=defaults["limit"],
                         help="max number of rows as select result, default is {}".format(defaults["limit"]))
    parser.add_argument("--debug", help="debug mode switch, default is False.", action="store_true")

    args = parser.parse_args()
    kv = {}
    logger.debug("sys.argv =")
    logger.debug(sys.argv)
    logger.debug("args =")
    logger.debug(args)
    logger.debug("vars(args) =")
    logger.debug(vars(args))
#   logger.debug("args.items() =")
#   logger.debug(args.items())
    shell_command = "`".join(sys.argv)
    for k, v in vars(args).items():
        logger.debug("k={}, v={}".format(k, v))
        if "--{}".format(k) in shell_command:
            # user $B;XDj(B
            kv[k] = v
    logger.debug("kv in _get_kv_by_argument() =")
    logger.debug(kv)
    logger.debug("\n")
    return kv

class Iasap(object):
    def __init__(self, dbpath, table_name, mode, height):
        limit = height
        self._limit = height

        try:
            # dbpath = ':memory:'
            conn = sqlite3.connect(dbpath)
        except sqlite3.OperationalError as raiz:
            if raiz.args[0] == 'unable to open database file':
                s = traceback.format_exc()
                logger.error(s)
                logger.error('dbpath is {}'.format(dbpath), file=sys.stderr)
            raise sqlite3.OperationalError(*raiz.args)

        conn = GeneralSQLConnection(conn)
      # print('conn =', conn)
        self.conn = conn

        self._make_sql_template(table_name, limit)

        logger.debug("mode is {} in Iasap.__init__()".format(mode))
        if mode == 'curses':
            _iasap = IasapCurses()
        elif mode == 'tkinter':
            _iasap = IasapTkinter()
        elif mode == 'one-shot':
            _iasap = self
        else:
            logger.debug("mode = \"{}\"".format(mode))
            raise ValueError('mode="{}" must be "curses" or "tkinter".'.format(mode))
        self.get_body = _iasap.get_body
        self.start = _iasap.start

    def get_body(self, search):
        sql = self._make_sql(search)
        rows = self._do_select(sql)
        logger.debug('search = "{}"'.format(search))
        if not search:
            return ''
        body = '\n'.join([text for text in self])
        return body

    def start(self, search):
        print("search: {}".format(search))
        body = get_body(search)
        for line in body:
            print(line)

    def _do_select(self, sql):
        logger.debug('sql = "{}"'.format(sql))
        s = datetime.datetime.now()
        self.named_rows = self.conn.select(sql)
        e = datetime.datetime.now()
        d = (e - s).total_seconds()
        logger.debug('select start at {}'.format(s))
        logger.debug('select   end at {}'.format(e))
        logger.debug('passed  time is {}'.format(d))

    def _make_sql(self, search):
        if not self._isascii(search):
            _sql = '''
                    tail collate nocase like "%{}%"
                  '''.format(search)
        elif ' ' in search:
            _sql = '''
                    head collate nocase like "{}%"
                    or
                    tail collate nocase like "{} "
                    or
                    tail collate nocase like " {}"
                  '''.format(search, search, search)
        else:
            _sql = '''
                    head collate nocase like "{}%"
                    and
                    head collate nocase not like "% %"
                  '''.format(search)
        sql = self._sql_template.format(_sql)

        return sql

    def _make_sql_template(self, table_name, limit):
        _from_where = "* from {} where".format(table_name)
        _limit = "limit {}".format(limit)

        self._sql_template = " ".join((_from_where, "{}", _limit))

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        self._i += 1
        if self._i > self._limit:
            self.named_rows.cur.close()
            raise StopIteration
        nx = self.named_rows.__next__()
        return '|'.join((nx.head, nx.tail))

    def _isascii(self, s):
        try:
            s.encode('ascii')
        except UnicodeEncodeError as raiz:
            if raiz.args[0] == 'ascii' and \
               raiz.args[4] == 'ordinal not in range(128)':
                return False
            else:
                raise UnicodeEncodeError(*raiz.args)
        return True
