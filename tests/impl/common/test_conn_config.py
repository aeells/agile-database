import unittest
from impl.common.conn_config import retrieveConnectionConfigurationFor

class ConnectionConfigurationTest(unittest.TestCase):
    def test_assert_yaml_contract_unsecured(self):
        connect_config = retrieveConnectionConfigurationFor('unsecured', 'tests/impl')
        self.assertEqual('qmg_admin', connect_config.getUser())
        self.assertEqual('qmg', connect_config.getPassword())
        self.assertEqual('localhost', connect_config.getHost())
        self.assertEqual('qmg', connect_config.getDatabase())

    def test_assert_yaml_contract_secured(self):
        connect_config = retrieveConnectionConfigurationFor('secured', 'tests/impl')
        self.assertIsNone(connect_config.getPassword())


if __name__ == '__main__':
    unittest.main()
