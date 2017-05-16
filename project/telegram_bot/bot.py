# -*- coding: utf-8 -*-
import time
import telebot
from jira import JIRA
from project.config  import Config

mychat_id = 113200632
number_of_issues = 0

config = Config()
bot = telebot.TeleBot(config.token)

if __name__ == '__main__':
    bot.send_message(mychat_id, u'Начали')
    while True:
        server = JIRA(server=config.url,
                      basic_auth=(config.login, config.password))
        count = len(server.search_issues('filter=22538'))
        if count != number_of_issues and count < 3:
            bot.send_message(mychat_id, u'У фогстрима осталось {} задач'.format(count))
            number_of_issues = count
        time.sleep(3600)
