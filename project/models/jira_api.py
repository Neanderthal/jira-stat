from jira import JIRA
from config import Config

config = Config()

server = JIRA(server=config.url,
              basic_auth=(config.login, config.password))