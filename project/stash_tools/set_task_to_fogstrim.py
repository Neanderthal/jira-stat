# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys

from jira import JIRA

from config import Config

cfg = Config()
server = JIRA(server=cfg.url,
              basic_auth=(cfg.login, cfg.password))


if __name__ == '__main__':
    try:
        issue, time = (sys.argv[1], sys.argv[2])
    except IndexError:
        print "Usage: set_task_to_fogstrim.py <issue_key> <time>"
        sys.exit(1)

    jira_issue = server.issue(issue)

    fixVersions = []
    for version in jira_issue.fields.fixVersions:
        #if version.name != 'version_to_remove':
        fixVersions.append({'name': version.name})
    fixVersions.append({'name': 'Фогстрим'})
    jira_issue.update(fields={'fixVersions': fixVersions})


    parsed_time = re.search("(\d)h", time).groups()
    original_estimate = (int(parsed_time[0])) * 60
    jira_issue.update(
        fields={"timetracking": {"remainingEstimate": original_estimate,
                                 "originalEstimate": original_estimate}})

    jira_issue.fields.labels.append('Фогстрим')
    jira_issue.update(fields={"labels": jira_issue.fields.labels})

    transitions = server.transitions(jira_issue)
    transition_id = [trans for trans in transitions if 'К разработке' in trans['name'] ][0]['id']
    server.transition_issue(issue, transition_id)


