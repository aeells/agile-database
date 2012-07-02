"""
This module holds all of the sql and wrapper scripts for MySQL.
"""
import pymysql, sys
from contextlib import contextmanager
from pymysql.err import MySQLError

def _get_connection(config):
    return pymysql.connect(host=config.getHost(), user=config.getUser(), db=config.getDatabase(), passwd=config.getPassword())

@contextmanager
def open_db(connection_config):
    connection = _get_connection(connection_config)
    cursor = connection.cursor()
    try:
        yield cursor
    except MySQLError as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        cursor.close()
        connection.close()
