# -*- coding: utf-8 -*-
import stashy
from jira import JIRA

from issue_repository import Projects, Statuses
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
    requests = list(pull_requests)
    return [request for request in requests if
                       'BOBUH' in request['title'] and request['open']]

def filter_merged_bobuh_pulreq(requests):
    title_ = [request for request in requests if 'BOBUH' in request['title']]
    return title_

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

            if jira_issue[0].fields.assignee.emailAddress == u's.istomin@bars-open.ru':
                print u'Изменяю assignee в задаче ' + issue_key + u' на ' + \
                      unapproves[0][u'user'][u'name']
                server.assign_issue(jira_issue[0],
                                    unapproves[0][u'user'][u'name'])


def get_realised_issues():
    status__format = u"project = {} AND status = {}".format(
        Projects.bobuh.value, Statuses.approve.value)
    jira_issue = server.search_issues(status__format)

    return jira_issue



if __name__ == '__main__':
    realized = get_realised_issues()
    realized_names = [issue.key for issue in realized]
    repository = get_repository_from_stash()
    pull_requests = repository.pull_requests.all(state = 'MERGED', limit = 50)
    filtered_requests = filter_merged_bobuh_pulreq(pull_requests)

    for key in realized_names:
        for request in filtered_requests:
            pull_request = pull_requests[request['id']].get()
            print pull_request


    # pull_requests = repository.pull_requests
    # opened_requests = filter_opened_bobuh_pulreq(pull_requests)

    #for opened in opened_reque
    #       change_issue_assignee_in_unapproved_pulreq(opened, pull_requests)


