# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

from pytg.receiver import Receiver
from pytg.sender import Sender

from models.issue import DeveloperInTeam, Team, TEAMS, FlagType, \
    ISSUE_TYPE, DeveloperFlags
from models.issue_repository import Statuses
from models.jira_api import server


receiver = Receiver(host="localhost", port=2391)
sender = Sender(host="localhost", port=2391)

response = sender.execute_function(u"contacts_list")

INWORK_FILTER = U"status in ('{}','{}','{}','{}')".format(
    Statuses.in_dev.value,
    Statuses.system_analize.value,
    Statuses.review.value,
    Statuses.re_dev.value) + u" and assignee = {}"


def is_pause_overtime(flag_type, flag):
    return datetime.now() - timedelta(
        minutes=flag_type.repeat_time_minutes) > flag.start_time


def send_message(flag_type, developer):
    message = flag_type.message.format(developer.name)
    if (developer.region.is_working_time()):
        sender.execute_function(u"msg", developer.telegram, message)

        teamlead_message = flag_type.teamlead_message.format(developer.email)
        sender.execute_function(u"msg", u"Sergey_Istomin", teamlead_message)
        return True
    return False


def get_issues(developer):
    filter_format = INWORK_FILTER.format(developer.email.split(u"@")[0])
    return server.search_issues(filter_format)


def set_flag(flag_type, developer):
    new_flag = DeveloperFlags(start_time=datetime.now(),
                              type=flag_type.id,
                              developer=developer.id,
                              count=1)
    new_flag.save()


def check_issues_and_remind():
    team = list(Team.select().where(Team.name == TEAMS.BOBUH.value)) 
    team_extended = list(
        DeveloperInTeam.select().where(DeveloperInTeam.team ==
                                       team[0].id))
    developers = [t_e.developer for t_e in team_extended]
    for developer in developers:

        flag_type = FlagType.get(
            FlagType.name == ISSUE_TYPE.multitasking.value)

        try:
            flag = DeveloperFlags.get((DeveloperFlags.type == flag_type) &
                                      (DeveloperFlags.developer == developer))
        except:
            flag = None

        issues = get_issues(developer)
        if (not flag):
            if len(issues) > 1:
                if (send_message(flag_type, developer)):
                    set_flag(flag_type, developer)
        elif is_pause_overtime(flag_type, flag):
            if (len(issues) > 1):
                send_message(flag_type, developer)
                flag.start_time = datetime.now()
                flag.count += 1
                flag.save()
            else:
                flag.delete_instance()


if __name__ == '__main__':
    while True:
        check_issues_and_remind()
        time.sleep(60)

