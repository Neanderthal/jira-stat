# -*- coding: utf-8 -*-
import time
import telebot

from datetime import datetime
from jira import JIRA
from project.config import Config
from project.models.issue import IssueLists, ISSUE_TYPE

FOGSTREAM_FILTER = 'filter=22538'

config = Config()
mychat_id = 113200632
#mychat_id = -214342832


bot = telebot.TeleBot(config.token)
#ls = bot.get_updates(allowed_updates=["channel_post"])


if __name__ == '__main__':
    while True:
        server = JIRA(server=config.url,
                      basic_auth=(config.login, config.password))
        fogstream_issues = server.search_issues(FOGSTREAM_FILTER)

        issue_string = u', '.join([issue.key for issue in fogstream_issues])

        issues_list = IssueLists(list_type = ISSUE_TYPE.fogstream.value, time = datetime.now(), issues = issue_string)
        if(issues_list.is_new()):
            issues_list.save()
            count = len(fogstream_issues)
            if count < 5:
                bot.send_message(mychat_id, u'У фогстрима осталось {} задач'.format(count))
        time.sleep(600)
