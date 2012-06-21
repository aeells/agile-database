import MySQLdb, os, sys

def update_release_number(connectConfig):
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
    return select_release_number(connectConfig)


def select_release_number(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value FROM seq_patch_metadata;
            """)
        release_number = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return release_number


def insert_patch_metadata_entry(connectConfig, script, release_number):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("""
                    INSERT INTO patch_metadata (release_number, patch_number, script, patch_type, patch_timestamp, script_checksum) VALUES (%s, %s, %s, 'PATCH', NOW(), %s);
                    """, (release_number, script.getPatchNumber(), script.getName(), int(script.getChecksum())))
        cursor.execute("COMMIT;")
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)


def update_patch_metadata_entry(connectConfig, script, release_number, patch_type):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("""
                    UPDATE patch_metadata SET release_number = %s, patch_type = %s, patch_timestamp = NOW(), script_checksum = %s
                        WHERE patch_number = %s
                        AND script = %s;
                    """, (release_number, patch_type, int(script.getChecksum()), script.getPatchNumber(), script.getName()))
        cursor.execute("COMMIT;")
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)


def determine_patch_type_if_already_applied(connectConfig, script):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patch_type FROM patch_metadata
                WHERE patch_number = %s
                AND script = %s;
            """, (script.getPatchNumber(), script.getName()))
        row = cursor.fetchone()
        if row is not None:
            patch_type = row[0]
        else:
            patch_type = None
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return patch_type


def determine_patch_applied_recently(connectConfig, script, releaseNumber):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
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
        else:
            release_number = None
        cursor.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return release_number

