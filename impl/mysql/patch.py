import os, sys
from pymysql.err import MySQLError

from impl.mysql import security, common_dml, get_connection
from impl.common import dir_struct, conn_config

def apply_patch(connectConfig, script):
    try:
        conn = get_connection(connectConfig)
        cursor = conn.cursor()
        cursor.execute(open(os.path.join(script.getPath(), script.getName()), 'r').read())
        cursor.close()
        conn.close()
    except MySQLError as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)


def patch(env, baseDir):
    connectConfig = conn_config.retrieveConnectionConfigurationFor(env, baseDir)
    security.prompt_password_if_empty(connectConfig)

    release_number = common_dml.update_release_number(connectConfig)

    scripts = dir_struct.all_patch_scripts_sorted_asc(baseDir)
    for script in scripts:
        patch_type = common_dml.determine_patch_type_if_already_applied(connectConfig, script)
        if patch_type in ('PATCH', 'BASELINE'):
            # do nothing
            continue
        elif patch_type == 'ROLLBACK':
            print "Applying patch: " + script.getName()
            apply_patch(connectConfig, script)
            common_dml.update_patch_metadata_entry(connectConfig, script, release_number, 'PATCH')
        else:
            print "Applying patch: " + script.getName()
            apply_patch(connectConfig, script)
            common_dml.insert_patch_metadata_entry(connectConfig, script, release_number)

