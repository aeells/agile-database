import os
from pkg_resources import resource_string

from impl.mysql import security, common_dml, open_db
from impl.common import dir_struct, conn_config

def clean_schema(connectConfig):
    with open_db(connectConfig) as cursor:
        cursor.execute("DROP PROCEDURE IF EXISTS p_clean_tables;")
        cursor.execute(resource_string(__name__, 'scripts/baseline/p_clean_tables.sql'))
        cursor.execute("""
            CALL p_clean_tables(%s);
            """, (connectConfig.getDatabase()))


def create_patch_metadata(connectConfig):
    with open_db(connectConfig) as cursor:
        cursor.execute(resource_string(__name__, 'scripts/baseline/patch_metadata.sql'))


def execute_baseline(baseDir, connectConfig):
    with open(os.path.join(baseDir, 'baseline/install.txt'), 'r') as f:
        for line in f:
            print line,
            # new connection required inside loop, otherwise we can only have a single SQL statement per file, see:
            # http://eric.lubow.org/2009/python/pythons-mysqldb-2014-error-commands-out-of-sync/
            with open_db(connectConfig) as cursor:
                cursor.execute(open(os.path.join(baseDir, 'baseline/', line.rstrip('\n')), 'r').read())


def patch_metadata_assert_patches_applied(baseDir, connectConfig):
    patches = dir_struct.all_patch_scripts(baseDir)
    for patch in patches:
        # new connection required inside loop, otherwise we can only have a single SQL statement per file, see:
        # http://eric.lubow.org/2009/python/pythons-mysqldb-2014-error-commands-out-of-sync/
        with open_db(connectConfig) as cursor:
            cursor.execute("""
                INSERT INTO patch_metadata (release_number, patch_number, script, patch_type, patch_timestamp, script_checksum) VALUES (0, %s, %s, 'BASELINE', NOW(), %s);
                """, (patch.getPatchNumber(), patch.getName(), int(patch.getChecksum())))
            cursor.execute("COMMIT;")


def baseline(env, baseDir, connectConfig=None):
    if connectConfig is None:
        connectConfig = conn_config.retrieveConnectionConfigurationFor(env, baseDir)
        security.prompt_password_if_empty(connectConfig)

    clean_schema(connectConfig)
    create_patch_metadata(connectConfig)
    execute_baseline(baseDir, connectConfig)
    patch_metadata_assert_patches_applied(baseDir, connectConfig)


def check(env, baseDir, connectConfig=None):
    if connectConfig is None:
        connectConfig = conn_config.retrieveConnectionConfigurationFor(env, baseDir)
        security.prompt_password_if_empty(connectConfig)

    return common_dml.determine_if_baseline_exists(connectConfig)
