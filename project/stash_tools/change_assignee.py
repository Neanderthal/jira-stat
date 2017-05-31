# -*- coding: utf-8 -*-
import stashy
from jira import JIRA

from project.config import Config
from jira_issue import get_jira_issues_for_pulreq

config = Config()
server = JIRA(server=config.url,
              basic_auth=(config.login, config.password))


def get_repository_from_stash():
    stash = stashy.connect(config.stash, config.login, config.password)
    repository = stash.projects['BUDG'].repos['web_bb']
    return repository


def filter_opened_bobuh_pulreq(pull_requests):
    requests = pull_requests.list()
    return [request for request in requests if
            'BOBUH' in request['title'] and request['open']]


def is_reviewer_in_admin_list(reviewer_email):
    is_reviewer_in_admin_list = reviewer_email not in [
        u'yuri.lya@fogstream.ru',
        u's.istomin@bars-open.ru',
        u'dechernyshov@bars-open.ru',
        u'kirov@bars-open.ru']
    return is_reviewer_in_admin_list


def get_unapproves(pulrequest):
    approves = []
    for approve in list(pulrequest['reviewers']):
        reviewer_email = approve[u'user'][u'emailAddress']
        if is_reviewer_in_admin_list(reviewer_email):
            approves.append(approve)

    return [issue for issue in approves if not issue['approved']]


def change_issue_assignee_in_unapproved_pulreq(opened, pull_requests):
    pulrequest = pull_requests[opened['id']].get()
    unapproves = get_unapproves(pulrequest)
    issues = get_jira_issues_for_pulreq(pulrequest, pull_requests, config)
    # Если к пулреквесту привязана одна задача и пулреквест не проаппрувлен
    # кем нибудь кроме меня передаем задачу ему
    if unapproves:

        for issue in issues:
            issue_key = issue[u'key']

            jira_issue = server.search_issues(u"issue = {}".format(issue_key))

            print u"Проверяю " + issue_key

            if (jira_issue[0].fields.assignee.emailAddress == u's.istomin@bars-open.ru' and
                    (jira_issue[0].fields.status.name == u"Ревью" or jira_issue[0].fields.status.name == u"На ревью")):
                print u'Изменяю assignee в задаче ' + issue_key + u' на ' + \
                      unapproves[0][u'user'][u'name']
                server.assign_issue(jira_issue[0],
                                    unapproves[0][u'user'][u'name'])


if __name__ == '__main__':
    repository = get_repository_from_stash()
    pull_requests = repository.pull_requests
    opened_requests = filter_opened_bobuh_pulreq(pull_requests)

    for opened in opened_requests:
        change_issue_assignee_in_unapproved_pulreq(opened, pull_requests)
