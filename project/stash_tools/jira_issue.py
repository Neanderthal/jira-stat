from stashy.client import StashClient, Stash
from stashy.errors import response_or_error
from stashy.helpers import ResourceBase


class StashIssue(ResourceBase):
    def __init__(self, url, client, parent):
        super(StashIssue, self).__init__(url, client, parent)

    @response_or_error
    def get(self):
        """
        Retrieve a pull request.
        """
        return self._client.get(self.url())


class StashJiraClient(StashClient):
    core_api_name = 'jira'
    core_api_path = 'jira/1.0'

class StashJira(Stash):
    def __init__(self, base_url, username=None, password=None, oauth=None, verify=True, session=None):
        self._client = StashJiraClient(base_url, username, password, oauth, verify, session=session)

def get_jira_issue(pulrequest, pull_requests, config):
    stash_jira = StashJira(pull_requests._client._base_url, config.login,
                           config.password,
                           session=pull_requests._client._session)
    issue = StashIssue(pulrequest['link']['url'] + '/issues',
                       stash_jira._client, pull_requests)
    issue_res = issue.get()
    return issue_res