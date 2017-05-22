# -*- coding: utf-8 -*-

import shlex
import subprocess

import re
from jira import JIRA
from config import Config

config = Config()
remotes = shlex.split("git branch --all --merged default")
process = subprocess.Popen(remotes, cwd="/home/sergey/PycharmProjects/web_bb", stdout=subprocess.PIPE, stderr = subprocess.PIPE)

output, error = process.communicate()

stripped = [item.strip(' ,')for item in output.split('\n') if 'remotes' in item and 'BOBUH' in item]

tasks = {re.search(r'BOBUH-\d{4}', item).group(0):item for item in stripped}
tasks_string = ", ".join(tasks.keys())

server = JIRA(server=config.url, basic_auth=(config.login, config.password))
issues = server.search_issues("issue in ({})".format(tasks_string), maxResults=len(tasks))

closed_issues = [issue for issue in issues if issue.fields.status.name == u'Закрыт']

branches_from_closed_issues = [tasks[issue.key] for issue in closed_issues]

for branch in branches_from_closed_issues:
    delete_string = shlex.split("git push origin --delete {}".format(branch.replace('remotes/origin/','')))
    process = subprocess.Popen(delete_string, cwd="/home/sergey/PycharmProjects/web_bb", stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    output, error = process.communicate()

    print output
    print error




