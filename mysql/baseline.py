# baseline.py -

import MySQLdb, os, sys

from warnings import filterwarnings, resetwarnings
from mysql import security_credentials as security
from bin import standard_dir_structure as dir_struct, connection_config as config, cksum

def clean_schema(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS p_clean_tables;")
        cursor.execute(open("./mysql/scripts/baseline/p_clean_tables.sql").read())
        cursor.execute("""
            CALL p_clean_tables(%s);
            """, (connectConfig.getDatabase()))
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return


def create_patch_metadata(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute(open("./mysql/scripts/baseline/patch_metadata.sql").read())
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return


def execute_baseline(scriptsBaseDir, connectConfig):
    with open(os.path.join(scriptsBaseDir, 'baseline/install.sql'), 'r') as f:
        for line in f:
            print line,
            try:
                # new connection required inside loop, otherwise we can only have a single SQL statement per file, see:
                # http://eric.lubow.org/2009/python/pythons-mysqldb-2014-error-commands-out-of-sync/
                conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
                cursor = conn.cursor()
                cursor.execute(open(os.path.join(scriptsBaseDir, 'baseline/', line.rstrip('\n')), 'r').read())
                cursor.close()
                conn.close()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
        f.close()
    return


def patch_metadata_assert_patches_applied(scriptsBaseDir, connectConfig):
    patches = dir_struct.find_all_patch_scripts(scriptsBaseDir)
    for patch in patches:
        if not os.path.isdir(patch):
            patch_number = dir_struct.extract_patch_number(patch)
            checksum = cksum.memcrc(open(patch, 'rb').read())
            try:
                # new connection required inside loop, otherwise we can only have a single SQL statement per file, see:
                # http://eric.lubow.org/2009/python/pythons-mysqldb-2014-error-commands-out-of-sync/
                conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO patch_metadata (release_number, patch_number, script, patch_type, patch_timestamp, script_checksum) VALUES (0, %s, %s, 'BASELINE', NOW(), %s);
                    """, (patch_number, patch, int(checksum)))
                cursor.execute("COMMIT;")
                cursor.close()
                conn.close()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
    return


def baseline(env, scriptsBaseDir):
    filterwarnings('ignore', category=MySQLdb.Warning)

    connectConfig = config.retrieveConnectionConfigurationFor(env, scriptsBaseDir)
    security.prompt_password_if_empty(connectConfig)
    clean_schema(connectConfig)
    create_patch_metadata(connectConfig)
    execute_baseline(scriptsBaseDir, connectConfig)
    patch_metadata_assert_patches_applied(scriptsBaseDir, connectConfig)

    resetwarnings()
    return
