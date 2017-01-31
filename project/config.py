import json
from ConfigParser import ConfigParser

class Config(object):
    class __Config(object):
        def __init__(self, file_names='settings.cfg'):
            self.config = ConfigParser()
            self._readed_config = self.config.read(file_names)

            self._url = self.config.get("server", "url")
            self._login = self.config.get("server", "login")
            self._password = self.config.get("server", "password")
            self._members = json.loads(self.config.get("team", "members"))

        @property
        def login(self):
            return self._login

        @property
        def url(self):
            return self._url

        @property
        def password(self):
            return self._password

        @property
        def members(self):
            return self._members

    instance = None

    def team_members(self):
        self.config.get("team", "members")

    def __init__(self, **arg):
        if not Config.instance:
            Config.instance = Config.__Config(*arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
