# coding: utf-8
from aenum import Enum

class Statuses(Enum):
    closed = u"Закрыт"
    for_dev = u"'К разработке'"
    in_dev = u"Разработка"
    re_dev = u"'К доработке'"
    analize = u"Анализ"
    eval = u"Оценка"
    review = u"Ревью"
    check = u"Тестирование"
    approve = u"Приемка"


class Projects(Enum):
    bobuh = u"BOBUH"
    bozik = u"BOZIK"
    itosdabug = u"ITOSDABUG"


class IssueRepository(object):
    def __init__(self, server):
        self.server = server

    def get_stat_for_user_inchange(self, user, status=Statuses.closed,
                          during=30, since_days_back = 0, max_results=1000):
        start = u"-{}d".format(since_days_back+during)
        finish = u"-{}d".format(since_days_back)
        template = (u"(assignee ={email} OR assignee was {email}) " +
                    u"AND status changed TO '{status}' BY '{email}'" +
                    u" DURING (endOfDay(" + start + u"),endOfDay("+ finish +u")) " +
                    u"ORDER BY updatedDate DESC")
        # search_string = 'project={project} and {}'
        search_string = template.format(email=user.name, status=status.value,
                                        days=during)
        issues = []

        try:
            issues = self.server.search_issues(search_string,
                                               maxResults=max_results)
        except UnicodeEncodeError as error:
            print(error.__dict__)
        return issues


    def get_stat_for_user_fixed(self, user, status=Statuses.closed,
            was_in=Statuses.in_dev, during=30, since_days_back = 0, max_results=1000):
        '''Все задачи для которых статус сейчас соответствует status
        а на пользователе были в статусе was_in'''
        start = u"-{}d".format(since_days_back + during)
        finish = u"-{}d".format(since_days_back)
        template =  (u"(assignee = '{email}' OR assignee was '{email}') " +
                     u"AND status changed to '{was_in}' BY '{email}' "+
                     u"DURING (endOfDay(" + start + u"),endOfDay("+ finish +u")) " +
                     u"AND status = '{status}'  ORDER BY updatedDate ASC")
        # search_string = 'project={project} and {}'
        search_string = template.format(email=user.name, status=status.value,
                                        days=during, was_in=was_in.value)
        issues = []
        try:
            issues = self.server.search_issues(search_string, maxResults=max_results)
        except UnicodeEncodeError as error:
            print(error.__dict__)
        return issues


    def get_stat_for_team(self, status=Statuses.closed, during=30, since_days_back = 0,
                          max_results=1000):
        start = u"-{}d".format(since_days_back + during)
        finish = u"-{}d".format(since_days_back)
        template = (u"(assignee in team(БО.РазработкаПитер)" +
            u"OR assignee was in team (БО.РазработкаПитер))" +
            u"AND status changed TO \'{}\' " +
            u"DURING (endOfDay(" + start + u"),endOfDay("+ finish +u")) " +
            u"ORDER BY updatedDate DESC")
        # search_string = 'project={project} and {}'
        issues = self.server.search_issues(template.format(status.value, during),
                                      maxResults=max_results)
        return issues

