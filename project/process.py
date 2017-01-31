# -*- coding: utf-8 -*-

import json
from ConfigParser import ConfigParser
from collections import OrderedDict

import texttable as tt
from enum import Enum
from jira import JIRA
from numpy import mean, std

from project.config import Config
from issue_repository import IssueRepository, Statuses


def open_jira():

    config = Config('settings.cfg')
    server = JIRA(server=config.url, basic_auth=(config.login, config.password))

    return server


def time_spent(issue, user):
    user_log = [worklog.timeSpentSeconds for
                worklog in issue.fields.worklog.worklogs
                if worklog.updateAuthor.key == user.key]
    spent = reduce(lambda a, b: a+b, user_log)
    return spent


def get_ratio(issues):
    values = [int(b.raw['fields']['workratio']) for b in issues if (
            b.raw['fields']['workratio'] < 3e+17)]
    return values

def get_avg_ratio(issues):
    values = (float(sum([int(b.fields.timespent if b.fields.timespent else 0) for b in issues]))
              /sum([int(b.fields.timeoriginalestimate) for b in issues]))
    return values

def get_full_stat(server, user, during=30, since_days_back = 0):
    issue = IssueRepository(server)
    total_in_dev = issue.get_stat_for_user_inchange(user, Statuses.in_dev, during=during, since_days_back=since_days_back)
    total_finished = issue.get_stat_for_user_inchange(user, Statuses.review, during=during, since_days_back=since_days_back)
    total_approved = issue.get_stat_for_user_fixed(user, Statuses.closed, during=during, since_days_back=since_days_back)
    now_indev = issue.get_stat_for_user_fixed(user, Statuses.in_dev, during=during, since_days_back=since_days_back)
    now_indev_str = ", ".join([issue.key for issue in now_indev])

    if total_approved:
        values = get_ratio(total_approved)
        avg_workratio = get_avg_ratio(total_approved)*100
        sko = int(std(values))
    else:
        avg_workratio = 0
        sko = 0

    result = OrderedDict()
    result["name"] = user.name
    result["total_in_dev"] = len(total_in_dev)
    result["planned_time"] = sum([int(b.fields.timeoriginalestimate) for b in total_in_dev])/3600
    result["total_finished"] = len(total_finished)
    result["total_approved"] = len(total_approved)
    result["avg_workratio"] = int(avg_workratio)
    result["sko"] = int((float(sko)/avg_workratio)*100) if sko else 0
    result["today"] = now_indev_str
    result["ratio"] = int(mean(get_ratio(now_indev))) if now_indev else 0

    return result


def get_projects_list(server):
    return [project.key for project in server.projects()]


def get_project_by_key(server, key):
    try:
        return [project for project in server.projects() if (
            project.key == key)][0]
    except:
        return None


def get_users_by_project(server, project=''):
    return [user.key for user in server.search_assignable_users_for_projects(
        '', project, maxResults=False) if user.active]


def process():
    server = open_jira()
    config = ConfigParser()
    config.read("settings.cfg")
    tab = tt.Texttable()
    tab.header(['name','devd','time','fin','closed','ratio','sko','',''])
    members = json.loads(config.get("team", "members"))
    for member in members:
        user = server.search_users(member)[0]
        user_stat = get_full_stat(server, user)
        tab.add_row(user_stat.values())
    print(tab.draw())

def process_for_user(name='g.frolov'):
    server = open_jira()
    config = ConfigParser()
    config.read("settings.cfg")
    tab = tt.Texttable()
    tab.header(
        ['name', 'devd', 'time', 'fin', 'closed', 'ratio', 'sko', '', ''])

    member = name
    user = server.search_users(member)[0]

    periods = 8
    period_len_days = 30

    for period in xrange(periods):

        user_stat = get_full_stat(server, user, during=period_len_days, since_days_back = period * period_len_days)
        tab.add_row(user_stat.values())




    print(tab.draw())



