"""
This module holds all of the sql and wrapper scripts for MySQL.
"""
import pymysql

def get_connection(config):
    return pymysql.connect(host=config.getHost(), user=config.getUser(), db=config.getDatabase(), passwd=config.getPassword())