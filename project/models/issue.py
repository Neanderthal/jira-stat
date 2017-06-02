# coding=utf-8
from datetime import datetime, time

from aenum import Enum
from peewee import *
from pytz import timezone
from tzlocal import get_localzone

from db import db


class TEAMS(Enum):
    BOBUH = "БО.Разработка Бух"

class ISSUE_TYPE(Enum):
    multitasking = u"Многозадачность"

    @classmethod
    def to_tuple_array(cls):
        for type_ in cls:
            yield (type_.name, type_.value)


class Issue(Model):
    issue = CharField()
    status = IntegerField()
    assignee = CharField()
    my_type = IntegerField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class FlagType(Model):
    name = CharField()
    repeat_time_minutes = IntegerField()
    message = TextField()
    teamlead_message = TextField()

    class Meta:
        database = db  # This model uses the "people.db" database.



class IssueLists(Model):
    list_type = IntegerField(choices=ISSUE_TYPE.to_tuple_array())
    time = DateTimeField()
    issues = TextField()

    def __eq__(self, other):
        result = set(self.issues) - set(other.issues)
        return bool(result)

    def is_new(self):
        latest = IssueLists.select().where(
            IssueLists.list_type==self.list_type).order_by(IssueLists.time.desc()).get()

        return self == latest

class Team(Model):
    name = CharField()
    jira_name = CharField

    class Meta:
        database = db  # This model uses the "people.db" database.


class Region(Model):
    name = CharField()
    time_zone = CharField()

    def is_working_time(self):
        now = self.now()
        return (now.hour > 8 and now.hour < 20)

    def now(self):
        now = datetime.now()
        local_tz = get_localzone()
        tz = timezone(local_tz.zone)
        localize = tz.localize(now)
        return localize.astimezone(timezone(self.time_zone))

    class Meta:
        database = db  # This model uses the "people.db" database.


class Developer(Model):
    email = CharField()
    name = CharField()
    telegram = CharField()
    telegram_id = CharField()
    is_admin = BooleanField()
    region = ForeignKeyField(Region)

    class Meta:
        database = db  # This model uses the "people.db" database.


class DeveloperInTeam(Model):
    team = ForeignKeyField(Team)
    developer = ForeignKeyField(Developer)

    class Meta:
        db_table = 'developer_in_team'
        database = db  # This model uses the "people.db" database.


class DeveloperFlags(Model):
    start_time = DateTimeField()
    type = ForeignKeyField(FlagType)
    developer = ForeignKeyField(Developer)
    count = IntegerField()

    class Meta:
        database = db  # This model uses the "people.db" database.

class FileStat(Model):
    path = CharField(max_length=1024)
    file_name = CharField()
    issues = CharField(max_length=2024)
    incidents = IntegerField()
    errors = IntegerField()

    class Meta:
        database = db  # This model uses the "people.db" database.
