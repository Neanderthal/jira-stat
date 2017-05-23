import json
import os
from ConfigParser import ConfigParser

class Config(object):
    class __Config(object):
        def __init__(self, file_names='settings.cfg'):
            fileDir = os.path.dirname(os.path.realpath(__file__))

            self.config = ConfigParser()
            self._readed_config = self.config.read(os.path.join(fileDir, file_names ))

            self._url = self.config.get("server", "url")
            self._login = self.config.get("server", "login")
            self._password = self.config.get("server", "password")
            self._stash = self.config.get("server", "stash")
            self._token = json.loads(self.config.get("server", "token"))

            self._members = json.loads(self.config.get("team", "members"))
            self._admins = json.loads(self.config.get("team", "admins"))


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
        def admins(self):
            return self._admins

        @property
        def members(self):
            return self._members

        @property
        def token(self):
            return self._token

        @property
        def stash(self):
            return self._stash

    instance = None

    def team_members(self):
        self.config.get("team", "members")

    def __init__(self, **arg):
        if not Config.instance:
            Config.instance = Config.__Config(*arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)
