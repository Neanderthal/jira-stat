# -*- coding: utf-8 -*-
import time
import telebot
from jira import JIRA

config = Config()

#mychat_id = 113200632
mychat_id = -214342832
number_of_issues = 0

config = Config()
bot = telebot.TeleBot(config.token)
ls = bot.get_updates(allowed_updates=["channel_post"])

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.send_message(mychat_id, '/getreviewers@JiraMessagesBot')
    while True:
        server = JIRA(server=config.url,
                      basic_auth=(config.login, config.password))
        count = len(server.search_issues('filter=22538'))
        if count != number_of_issues and count < 3:
            bot.send_message(mychat_id, u'У фогстрима осталось {} задач'.format(count))
            number_of_issues = count
        time.sleep(3600)
