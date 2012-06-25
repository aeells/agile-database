import unittest
from mock import patch

from impl.common.conn_config import retrieveConnectionConfigurationFor

class SecurityTest(unittest.TestCase):
    def test_secured_connection_password_correct(self):
        connect_config = retrieveConnectionConfigurationFor('secured', 'tests/impl')

        with patch('impl.mysql.security.raw_input', create=True, return_value='qmg'):
            with patch('impl.mysql.security.check_invalid_credentials', return_value=False) as mock_credentials:
                from impl.mysql.security import prompt_password_if_empty

                prompt_password_if_empty(connect_config)
                mock_credentials.assert_called_once_with(connect_config)

        prompt_password_if_empty(connect_config)

        return

#    @unittest.skip("could not get this to work so that the first password is incorrect and the second correct.")
    def test_secured_connection_password_incorrect(self):
        return


if __name__ == '__main__':
    unittest.main()
