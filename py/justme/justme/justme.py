import sqlite3
import os
import time
import datetime
import tempfile

class CannotRun(Exception):
    pass

class JustMe(object):
    """Prohibit to run two process/instance at same time.
    To use a transaction behavior via sqlite3.
    """

    TABLE_NAME = 'just_me'
    CREATE_TABLE = '''
        CREATE TABLE {}(
            id integer primary key autoincrement unique not null
            ,
            moment text not null -- when do you call lock() or unlock() ?
            ,
            type text not null -- "lock" or "unlock"
            ,
            pid integer not null -- process id
        );
    '''.format(TABLE_NAME)
    LOCK_FILE_PATH = os.path.join(tempfile.gettempdir(), 'just_me.lock')

    def __init__(self,
                 script_name='"JustMe"',
                 db_path=LOCK_FILE_PATH,
                 ):
        """initilize attributes and create database to lock database."""

        self.script_name = script_name
        self._db_path = db_path
        self._pid = os.getpid()

        # for transaction
        self._conn = sqlite3.connect(self._db_path,
                                     timeout=0,
                                     isolation_level='IMMEDIATE')
        self._cur = self._conn.cursor()
        self._create_db()

    def lock(self):
        """see method name"""
        self._lock()

    def unlock(self):
        """see method name"""
        self._unlock()

    def clean(self):
        """delete lock file"""
        os.remove(self._db_path)

    def dump_db(self, limit=0):
        """dump db order by id desc.
        And set limit records of number."""
        sql = 'select * from {} order by id desc'.format(JustMe.TABLE_NAME)
        if limit:
            sql += ' limit {}'.format(limit)

      # print('sql =')
      # print(sql)
        rows = self._cur.execute(sql)
        column_names = tuple(map(lambda x: x[0], self._cur.description))
        print(column_names)
        for row in rows.fetchall():
            print(row)

    def _create_db(self):
        """see method name"""
        try:
            self._cur.execute(JustMe.CREATE_TABLE)
        except sqlite3.OperationalError as raiz:
            message = 'table {} already exists'.format(JustMe.TABLE_NAME)
            if raiz.args[0] != message:
                raise raiz

    def _lock(self):
        """acquire lock instance.
           if you cannot lock, raise CannotRun()
        """

        self._insert_to_lock('prelock')
        self._insert_to_lock('lock')

    def _insert_to_lock(self, type_):
        if type_ == 'lock':
            self._conn.isolation_level = 'IMMEDIATE'
        elif type_ == 'prelock':
            self._conn.isolation_level = None
        else:
            ValueError('unkown type_ "{}"'.format(type_))

        error_message = ''
        sql = self._make_sql(type_)
        try:
            self._cur.execute(sql)
            # NEVER self._conn.commit() in _lock()
        except sqlite3.OperationalError as raiz:
            if raiz.args[0] == 'database is locked':
                error_message = \
                    ('Another process/instance of '
                     '{0} is already running.'.format(self.script_name))
            else:
                raise raiz

        if error_message:
            last_record = self.get_last_record()
            column_names = tuple(map(lambda x: x[0], self._cur.description))
            print('last record is')
            print(column_names)
            print(last_record)
            raise CannotRun(error_message)

    def get_last_record(self):
        """get last record"""
        fmt = 'select * from {0} where id = (select max(id) from {0})'
        sql = fmt.format(JustMe.TABLE_NAME)
        last_record = self._cur.execute(sql).fetchone()
        return last_record

    def _unlock(self):
        """release lock instance"""
        self._conn.isolation_level = 'IMMEDIATE'
        sql = self._make_sql('unlock')
        self._cur.execute(sql)
        self._conn.commit()

    def _make_sql(self, type_):
        """make sql sentence for lock/unlock"""
        now = datetime.datetime.now().isoformat()
        d = {
            'id': 'NULL',
            'moment': now,
            'type': type_,
            'pid': self._pid,
        }

        fmt = ("insert into {0}(id, moment, type, pid) "
               "values({id}, '{moment}', '{type}', {pid})")
        sql = fmt.format(JustMe.TABLE_NAME, **d)
      # print('sql =')
      # print(sql)

        return sql

    def __enter__(self):
        """automatic lock()"""
        self.lock()

    def __exit__(self, *args):
        """automatic unlock()"""
        self.unlock()

if __name__ == '__main__':

    class MyJustMe(JustMe):
        """how to inherit the JustMe class"""

        def lock(self):
            """you should change this method in inherited class.
            """
            now = datetime.datetime.now().isoformat()
            print('{0} pid={1} trying lock().'.format(now, self._pid))

            super().lock()

            now = datetime.datetime.now().isoformat()
            print('{0} pid={1} locked.'.format(now, self._pid))

        def unlock(self):
            """you should change this method in inherited class.
            """
            now = datetime.datetime.now().isoformat()
            print('{0} pid={1} trying unlock().'.format(now, self._pid))

            super().unlock()

            now = datetime.datetime.now().isoformat()
            print('{0} pid={1} unlocked.'.format(now, self._pid))

    my_just_me = MyJustMe(script_name='MyJustMe')

    with my_just_me:
        time.sleep(5)

  # my_just_me.lock()   # equal to above with sentence.
  # time.sleep(5)       #
  # my_just_me.unlock() #

    my_just_me.dump_db(limit=10)

  # my_just_me.clean() # if need.
