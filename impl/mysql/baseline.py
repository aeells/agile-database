import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb, os, sys
from pkg_resources import resource_string

from warnings import filterwarnings, resetwarnings
from impl.mysql import security, common_dml
from impl.common import dir_struct, conn_config


def clean_schema(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("DROP PROCEDURE IF EXISTS p_clean_tables;")
        cursor.execute(resource_string(__name__, 'scripts/baseline/p_clean_tables.sql'))
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
        cursor.execute(resource_string(__name__, 'scripts/baseline/patch_metadata.sql'))
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return


def execute_baseline(baseDir, connectConfig):
    with open(os.path.join(baseDir, 'baseline/install.txt'), 'r') as f:
        for line in f:
            print line,
            try:
                # new connection required inside loop, otherwise we can only have a single SQL statement per file, see:
                # http://eric.lubow.org/2009/python/pythons-mysqldb-2014-error-commands-out-of-sync/
                conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
                cursor = conn.cursor()
                cursor.execute(open(os.path.join(baseDir, 'baseline/', line.rstrip('\n')), 'r').read())
                cursor.close()
                conn.close()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
        f.close()
    return


def patch_metadata_assert_patches_applied(baseDir, connectConfig):
    patches = dir_struct.all_patch_scripts(baseDir)
    for patch in patches:
            try:
                # new connection required inside loop, otherwise we can only have a single SQL statement per file, see:
                # http://eric.lubow.org/2009/python/pythons-mysqldb-2014-error-commands-out-of-sync/
                conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO patch_metadata (release_number, patch_number, script, patch_type, patch_timestamp, script_checksum) VALUES (0, %s, %s, 'BASELINE', NOW(), %s);
                    """, (patch.getPatchNumber(), patch.getName(), int(patch.getChecksum())))
                cursor.execute("COMMIT;")
                cursor.close()
                conn.close()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)
    return


def baseline(env, baseDir, connectConfig = None):
    filterwarnings('ignore', category=MySQLdb.Warning)

    if connectConfig is None:
        connectConfig = conn_config.retrieveConnectionConfigurationFor(env, baseDir)
        security.prompt_password_if_empty(connectConfig)

    clean_schema(connectConfig)
    create_patch_metadata(connectConfig)
    execute_baseline(baseDir, connectConfig)
    patch_metadata_assert_patches_applied(baseDir, connectConfig)

    resetwarnings()
    return

def check(env, baseDir, connectConfig = None):
    if connectConfig is None:
        connectConfig = conn_config.retrieveConnectionConfigurationFor(env, baseDir)
        security.prompt_password_if_empty(connectConfig)

    return common_dml.determine_if_baseline_exists(connectConfig)
