from unittest import TestCase
import os

from project.config import Config

member_2 = 'a.prokoptsev@xxx.ru'
member_1 = 'a.afonin@xxx.ru'
password = "888888"
login = "s.istomin"
url = "https://xxxxxx.xxx"
config_filename = 'test.cfg'


class TestConfig(TestCase):
    def setUp(self):
        with open(config_filename, 'w') as file:
            strings = (
                "[server]\n",
                ("url = %s\n" % url),
                ("login = %s\n" % login),
                ("password = %s\n" % password),
                "\n",
                "[team]\n",
                ('members = ["%s", "%s"]' % (member_1, member_2))
            )

            file.writelines(strings)

    def test_config_creation(self):
        try:
            config = Config(config_filename)
        except Exception as ex:
            self.fail("test failed exception {} raised".format(type(ex)))

        self.assertEqual(config.url, url)
        self.assertEqual(config.login, login)
        self.assertEqual(config.password, password)
        self.assertEqual(config.members[0], member_1)
        self.assertEqual(config.members[1], member_2)
    pass

    def tearDown(self):
        os.remove(config_filename)
