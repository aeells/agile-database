import MySQLdb

def prompt_password_if_empty(connectConfig):
    global password
    if connectConfig.getPassword() is None:
        invalid = True
        while (invalid):
            password = raw_input("Please enter password to access database " + connectConfig.getDatabase() + " on " + connectConfig.getHost() + ": ")
            connectConfig.password = password
            invalid = check_invalid_credentials(connectConfig)
    return


def check_invalid_credentials(connectConfig):
    try:
        conn = MySQLdb.connect(connectConfig.getHost(), connectConfig.getUser(), connectConfig.getPassword(), connectConfig.getDatabase())
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return False
    except MySQLdb.OperationalError, e:
        print "Invalid credentials %d: %s" % (e.args[0], e.args[1])
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return True

