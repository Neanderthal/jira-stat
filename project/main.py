#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from project import process
import project.process as pr


def get_projects(args):
    server = pr.open_jira()
    for project in pr.get_projects_list(server):
        print(project)


def get_users_in_project(args):
    server = pr.open_jira()
    print(pr.get_users_by_project(server, args.key))


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_append = subparsers.add_parser('projects', help='Get project by key')
    parser_append.set_defaults(func=get_projects)

    parser_append = subparsers.add_parser('users', help='Get users in project')
    parser_append.add_argument('key', help='The key of project')
    parser_append.set_defaults(func=get_users_in_project)

    return parser.parse_args()


def main():
    server = process.open_jira()
    process.process_for_user()


if __name__=="__main__":
    main()
