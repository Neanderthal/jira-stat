import stashy
from jira import JIRA

from project.config import Config
from jira_issue import get_jira_issue

config = Config()


if __name__ == '__main__':
    stash = stashy.connect(config.stash, config.login, config.password)
    repository = stash.projects['BUDG'].repos['web_bb']
    pull_requests = repository.pull_requests
    requests = pull_requests.list()
    opened_requests = [request for request in requests if 'BOBUH' in request['title'] and request['open']]

    for opened in opened_requests:
        pulrequest = pull_requests[opened['id']].get()
        reviewers = []
        for approver in list(pulrequest['reviewers']):
            if (approver[u'user'][u'emailAddress'] != u'yuri.lya@fogstream.ru' and
                approver[u'user'][
                    u'emailAddress'] != u's.istomin@bars-open.ru' and
                approver[u'user'][
                    u'emailAddress'] != u'dechernyshov@bars-open.ru'):
                reviewers.append(approver)

        unapprovers = [issue for issue in reviewers if not issue['approved']]

        issue = get_jira_issue(pulrequest, pull_requests, config)
        print "Проверяю " + issue[0][u'key']

        # Если к пулреквесту привязана одна задача и пулреквест не проаппрувлен
        # кем нибудь кроме меня передаем задачу ему
        if len(issue) == 1 and unapprovers:
            server = JIRA(server=config.url,
                          basic_auth=(config.login, config.password))
            issues = server.search_issues(u"issue = {}".format(issue[0][u'key']))

            if issues[0].fields.assignee.emailAddress == u's.istomin@bars-open.ru':
                print u'Изменяю assignee в задаче ' + issue[0][u'key'] + u'на' + unapprovers[0][u'user'][u'name']
                server.assign_issue(issues[0], unapprovers[0][u'user'][u'name'])


