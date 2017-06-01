# coding=utf-8

from aenum import AutoNumberEnum, Enum
from peewee import *

from project.db import db


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


class Developer(Model):
    email = CharField()
    name = CharField()
    telegram = CharField()
    telegram_id = CharField()
    is_admin = BooleanField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Developer_in_Team(Model):
    team = ForeignKeyField(Team)
    developer = ForeignKeyField(Developer)

    class Meta:
        database = db  # This model uses the "people.db" database.


class DeveloperFlags(Model):
    start_time = DateTimeField()
    type = ForeignKeyField(FlagType)
    developer = ForeignKeyField(Developer)
    count = IntegerField()

    class Meta:
        database = db  # This model uses the "people.db" database.

