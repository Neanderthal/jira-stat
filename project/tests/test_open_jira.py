from unittest import TestCase

from project.process import open_jira


class TestOpen_jira(TestCase):
    def test_open_jira(self):
        server = None
        try:
            server = open_jira()
        except Exception as ex:
            self.fail("test failed exception {} raised".format(type(ex)))

        self.assertIsNotNone(server)
