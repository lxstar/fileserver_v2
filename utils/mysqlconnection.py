#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb
import logging
logger = logging.getLogger('Sqlconnect.log')


class MySQLConnect():

    def __init__(self, host, port, user, passwd, dbname, charset="utf8", connect_timeout=10):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.charset = charset
        self.connect_timeout = connect_timeout
        self.connection()

    def connection(self):
        '''
        connect sql db
        '''
        self.conn = MySQLdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            port=self.port,
            charset=self.charset,
            connect_timeout=self.connect_timeout
        )
        self.cur = self.conn.cursor()
        self.conn.select_db(self.dbname)

    def execute(self, command, para=None):
        '''
        execute the sql command
        ps: para without ""
        '''
        try:
            self.cur.execute(command, para)
            result = self.cur.fetchall()
            self.conn.commit()
            return result
        except MySQLdb.Error as ex:
            logger.error('execute error:%s,retry!' % str(ex))
            self.connection()
            self.cur.execute(command, para)
            result = self.cur.fetchall()
            self.conn.commit()
            return result

    def close(self):
        '''
        close client
        '''
        self.cur.close()
        self.conn.close()

    def __del__(self):
        try:
            self.close()
        except Exception as ex:
            logger.error('MySQLConnect close error %s' % str(ex))
