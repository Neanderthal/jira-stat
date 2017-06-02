# coding: utf-8
import os
import shlex
import subprocess

import re

from config import Config
from models.issue import FileStat
from models.issue_repository import IssueType
from models.jira_api import server


INWORK_FILTER = U"issuetype in ('{}','{}')".format(
    IssueType.error.value,
    IssueType.accident.value) + u" and issue in ({})"


def get_issues(issues_string):
    filter_format = INWORK_FILTER.format(issues_string)
    return server.search_issues(filter_format)

if __name__ == '__main__':
    config = Config()
    for d, dirs, files in os.walk("/home/sergey/PycharmProjects/web_bb/src/web_bb"):
        if "./" in d:
            continue
        for file in files:

            remotes = shlex.split("git log --pretty=oneline --follow {}".format(os.path.join(d, file)))
            process = subprocess.Popen(remotes,
                                       cwd="/home/sergey/PycharmProjects/web_bb",
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            strings = output.split("\n")
            tasks = []
            for string in strings:
                found = re.search(r'BOBUH-\d{4}', string)
                if found:
                    tasks.append(found.group(0))
            if tasks:
                issues_string = ", ".join(tasks)
                errors_and_accidents = get_issues(issues_string)

                issues_count = len([issue for issue in errors_and_accidents
                    if issue.fields.issuetype.name == IssueType.accident.value])

                errors_count = len([issue for issue in errors_and_accidents
                    if (issue.fields.issuetype.name == IssueType.error.value) or
                       (issue.fields.issuetype.name == IssueType.problem.value)])

                if(errors_and_accidents):
                    file_stat = FileStat(
                        path=d,
                        file_name=file,
                        issues=issues_string,
                        incidents=issues_count,
                        errors=errors_count)
                    file_stat.save()
                    print u"file added {}/{}".format(d, file)


