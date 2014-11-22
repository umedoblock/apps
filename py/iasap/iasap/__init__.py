# Copyright 2011-2014 梅濁酒(umedoblock)

__all__ = ['IasapCurses', 'IasapTkinter']

import sqlite3, os, sys, datetime
import logging as _logger

global logger
logger = _logger

from iasap.sql import GeneralSQLConnection

CHARACTORS_PRINTED_PER_LINE = 79
CPPL = CHARACTORS_PRINTED_PER_LINE

def start_logger(script_name, log_dir=os.path.curdir, log_level=logger.INFO):
    # 通常使用時は、log_dir=os.path.curdir を想定している。
    # log_dir が空文字であれば、log の出力先を sys.stderr に変更する。

    basename = os.path.basename(script_name)
    if log_dir:
        log_base = ".".join((basename, "log"))
        log_path = os.path.join(log_dir, log_base)

        # http://docs.python.jp/3.4/library/logging.html#logging.basicConfig
        # stream: 指定されたストリームを StreamHandler の初期化に使います。
        # この引数は 'filename' と同時には使えないことに注意してください。
        # 両方が指定されたときには ValueError が送出されます。
        # logger.basicConfig(filename='/dev/null', level=logger.INFO)
        # logger.basicConfig(stream=sys.stderr, level=logger.DEBUG)
        logger.basicConfig(filename=log_path, level=log_level)
    else:
        logger.basicConfig(stream=sys.stderr, level=log_level)

    log_prefix = "INFO:root:"
    horizontal = "=" * (CPPL - len(log_prefix))
    _now = datetime.datetime.now()
    body = "{} start! at {} ".format(basename, _now)
    tail = "=" * (CPPL - (len(log_prefix) + len(body)))

    logger.info(horizontal)
    logger.info(body + tail)
    logger.info(horizontal)

class Iasap(object):
    def __init__(self, dbpath, height):
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

        _table = "eijiro"
        self._make_sql_template(_table, limit)

    def get_body(self, search):
        sql = self._make_sql(search)
        rows = self._do_select(sql)
        logger.debug('search = "{}"'.format(search))
        if not search:
            return ''
        body = '\n'.join([text for text in self])
        return body

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

    def _make_sql_template(self, table, limit):
        _from_where = "* from {} where".format(table)
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
