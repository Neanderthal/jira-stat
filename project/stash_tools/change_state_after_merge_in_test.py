# -*- coding: utf-8 -*-
import stashy
from jira import JIRA

from project.config import Config
from jira_issue import get_jira_issues_for_pulreq, get_commits_for_task
from project.issue_repository import Projects, Statuses

config = Config()
server = JIRA(server=config.url,
              basic_auth=(config.login, config.password))

def get_repository_from_stash():
    stash = stashy.connect(config.stash, config.login, config.password)
    repository = stash.projects['BUDG'].repos['web_bb']
    return repository


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

def get_tested(commits, key, test_commits):
    latest_commits = []
    for commit in commits['values']:
        for f_commit in test_commits:
            if f_commit == commit['toCommit']['displayId']:
                yield key, True
    yield key, False


if __name__ == '__main__':
    realized = get_realised_issues()
    realized_names = [issue.key for issue in realized]
    repository = get_repository_from_stash()
    in_test_commits = []
    for f_commit in repository.commits(until='refs/heads/test'):
        if f_commit['displayId'] == u'43e1f54870f':
            break
        in_test_commits.append(f_commit['displayId'])

    for key in realized_names:
        after_issue_commits = get_commits_for_task('/issues/{}/commits'.format(key), repository, repository._client, config)
        all_tested = list(get_tested(after_issue_commits, key, in_test_commits))
        result = []
        key_false = True
        for key, value in all_tested:
            key_false = key_false and value
            if not key_false:
                result.append(key)


    print ''

