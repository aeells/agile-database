import yaml, os

class ConnectConfig:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def getHost(self):
        return self.host

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password

    def getDatabase(self):
        return self.database


def retrieveConnectionConfigurationFor(env, scriptsBaseDir):
    connect_config = yaml.load(open(os.path.join(scriptsBaseDir, 'config/agile-database.yaml'), 'r'))[env]
    return ConnectConfig(connect_config["host"], connect_config["user"], connect_config["password"], connect_config["database"])

