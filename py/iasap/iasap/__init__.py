# Copyright 2011-2014 梅濁酒(umedoblock)

import sqlite3, os, sys, datetime

from iasap.iasap_tkinter import IasapTkinter
from iasap.iasap_curses import IasapCurses
from iasap.sql import GeneralSQLConnection
from iasap.lib import logger, start_logger
from iasap.lib import merge_kv_by_defaults_and_argument, set_kv_for_regular

if os.path.islink(__file__):
    __file__ = os.path.realpath(__file__)
__file__ = os.path.abspath(__file__)
dirname = os.path.dirname(__file__)

class Iasap(object):
    DEFAULTS = {
        "conf": os.path.join(dirname, "..", "iasap.conf"),
        "dbpath": os.path.join(dirname, "..", 'iasap.sqlite3'),
        "mode": "tkinter",
        "limit": 30,
        "debug": False,
    }

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
        _iasap.get_body = self.get_body
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
        logger.debug("search: {}".format(search))
        body = self.get_body(search)
        for line in body.split("\n"):
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

def main(cls, script_name, table_name):
    start_logger(script_name, os.path.curdir, logger.DEBUG)

    kv_merged, kv_defaults, kv_argment = \
        merge_kv_by_defaults_and_argument(cls.DEFAULTS)

    kv = set_kv_for_regular(kv_defaults, kv_argment, kv_merged["conf"], table_name)

    if not os.path.isfile(kv["dbpath"]):
        raise OSError("cannot access \"{}\": No such file.".format(kv["dbpath"]))

    logger.debug("cls={}(dbpath={}, table_name={}, mode={}, limit={})".format(cls, kv["dbpath"], table_name, kv["mode"], kv["limit"]))
    iasap_obj = cls(kv["dbpath"], table_name, kv["mode"], kv["limit"])
    logger.debug("iasap_obj = {}".format(iasap_obj))
    if kv["mode"] == "one-shot":
        if not len(kv["args"]):
            msg = ("mode として one-shot を指定した場合は、"
                   "one-shot の後に空白を一つ入れ、空白の後に検索語を一つ"
                   "指定しなければなりません。")
            raise ValueError(msg)
        iasap_obj.start(kv["args"][0])
    else:
        iasap_obj.start()
