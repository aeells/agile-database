import os

from impl.mysql import security, common_dml, open_db
from impl.common import dir_struct, conn_config

def apply_rollback(connectConfig, script):
    with open_db(connectConfig) as cursor:
        cursor.execute(open(os.path.join(script.getPath(), script.getName()), 'r').read())


def rollback(env, baseDir, connectConfig = None):
    if connectConfig is None:
        connectConfig = conn_config.retrieveConnectionConfigurationFor(env, baseDir)
        security.prompt_password_if_empty(connectConfig)

    current_release_number = common_dml.select_release_number(connectConfig)

    scripts = dir_struct.all_rollback_scripts_sorted_desc(baseDir)
    for script in scripts:
        patch_release_number = common_dml.determine_patch_applied_recently(connectConfig, script, current_release_number)
        if patch_release_number == current_release_number:
            patch_type = common_dml.determine_patch_type_if_already_applied(connectConfig, script)
            if patch_type in ('PATCH', 'BASELINE'):
                print "Applying rollback: " + script.getName()
                apply_rollback(connectConfig, script)
                common_dml.update_patch_metadata_entry(connectConfig, script, current_release_number, 'ROLLBACK')
                continue
            elif patch_type == 'ROLLBACK':
                # do nothing
                continue
            else:
                # do nothing
                continue


