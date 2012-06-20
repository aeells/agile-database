import MySQLdb, os, sys

from warnings import filterwarnings, resetwarnings
from mysql import security_credentials as security
from bin import standard_dir_structure as dir_struct, connection_config as config, cksum

def update_patch_sequence(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE seq_patch_metadata SET value = value + 1;
            """)
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return


def select_patch_sequence(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value FROM seq_patch_metadata;
            """)
        patch_sequence = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return patch_sequence


def patch(env, scriptsBaseDir):
    filterwarnings('ignore', category=MySQLdb.Warning)

    connectConfig = config.retrieveConnectionConfigurationFor(env, scriptsBaseDir)
    security.prompt_password_if_empty(connectConfig)

    update_patch_sequence(connectConfig)
    release_number = select_patch_sequence(connectConfig)
    print release_number

    resetwarnings()
    return

