# -*- coding: utf-8 -*-
import stashy
from jira import JIRA

from jira_issue import get_jira_issues_for_pulreq, get_commits_for_task
from project.models.issue_repository import Projects, Statuses
from project.config import Config

config = Config()
server = JIRA(server=config.url,
              basic_auth=(config.login, config.password))

def get_repository_from_stash():
    stash = stashy.connect(config.stash, config.login, config.password)
    repository = stash.projects['BUDG'].repos['web_bb']
    return repository


def get_realised_issues():
    status__format = u"project = {} AND status = {}".format(
        Projects.bobuh.value, Statuses.realized.value)
    jira_issue = server.search_issues(status__format)

    return jira_issue

def get_tested(commits, key, test_commits):
    latest_commits = []
    for commit in commits['values']:
        for f_commit in test_commits:
            if f_commit == commit['toCommit']['displayId']:
                yield key, True
    yield key, False


def check_issue_commits_in_test():
    pass
    in_test_commits = []
    for f_commit in repository.commits(until='refs/heads/test'):
        if f_commit['displayId'] == u'43e1f54870f':
            break
        in_test_commits.append(f_commit['displayId'])

    # for key in realized_names:
    #     after_issue_commits = get_commits_for_task('/issues/{}/commits'.format(key),
    #                                                repository, repository._client, config)['values']
    #     #all_tested = list(get_tested(after_issue_commits, key, in_test_commits))
    #
    #     #key_false = True
    #     for commit in after_issue_commits:
    #         if commit['toCommit']['displayId'] == u'e3f97890f92':
    #             result.append(key)


if __name__ == '__main__':
    realized = get_realised_issues()
    realized_names = [issue.key for issue in realized]
    repository = get_repository_from_stash()


    #check_issue_commits_in_test()
    for jira_issue in realized:
        transitions = server.transitions(jira_issue)
        transition_id = [trans for trans in transitions if Statuses.approve.value in trans['name'] ][0]['id']
        server.transition_issue(jira_issue.key, transition_id)
        print u"{} в приемке".format(jira_issue.key)



