from impl.mysql import open_db

def update_release_number(connectConfig):
    with open_db(connectConfig) as cursor:
        cursor.execute("""UPDATE seq_patch_metadata SET value = value + 1;""")
    return select_release_number(connectConfig)


def select_release_number(connectConfig):
    with open_db(connectConfig) as cursor:
        cursor.execute("""SELECT value FROM seq_patch_metadata;""")
        return cursor.fetchone()[0]


def insert_patch_metadata_entry(connectConfig, script, release_number):
    with open_db(connectConfig) as cursor:
        cursor.execute("""
            INSERT INTO patch_metadata (release_number, patch_number, script, patch_type, patch_timestamp, script_checksum) VALUES (%s, %s, %s, 'PATCH', NOW(), %s);
            """, (release_number, script.getPatchNumber(), script.getName(), int(script.getChecksum())))
        cursor.execute("COMMIT;")


def update_patch_metadata_entry(connectConfig, script, release_number, patch_type):
    with open_db(connectConfig) as cursor:
        cursor.execute("""
            UPDATE patch_metadata SET release_number = %s, patch_type = %s, patch_timestamp = NOW(), script_checksum = %s
            WHERE patch_number = %s
            AND script = %s;
            """, (release_number, patch_type, int(script.getChecksum()), script.getPatchNumber(), script.getName()))
        cursor.execute("COMMIT;")


def determine_patch_type_if_already_applied(connectConfig, script):
    patch_type = None
    with open_db(connectConfig) as cursor:
        cursor.execute("""
        SELECT patch_type FROM patch_metadata
            WHERE patch_number = %s
            AND script = %s;
        """, (script.getPatchNumber(), script.getName()))
        row = cursor.fetchone()
        if row is not None:
            patch_type = row[0]

    return patch_type


def determine_patch_applied_recently(connectConfig, script, releaseNumber):
    release_number = None
    with open_db(connectConfig) as cursor:
        cursor.execute("""
        SELECT release_number FROM patch_metadata
            WHERE patch_number = %s
            AND script = %s
            AND release_number = %s
            AND patch_type = 'PATCH';
        """, (script.getPatchNumber(), script.getName(), releaseNumber))
        row = cursor.fetchone()
        if row is not None:
            release_number = row[0]

    return release_number


def determine_if_baseline_exists(connectConfig):
    baseline_exists = False
    with open_db(connectConfig) as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = 'patch_metadata'
            """, (connectConfig.getDatabase()))
        row = cursor.fetchone()
        if row is not None:
            if row[0] > 0:
                baseline_exists = True

    return baseline_exists

