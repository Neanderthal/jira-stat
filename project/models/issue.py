from peewee import *
from aenum import Enum, AutoNumberEnum

class ISSUE_TYPE(AutoNumberEnum):
    fogstream = u"Фогстрим"


db = SqliteDatabase('jira.db')

class Issue(Model):
    issue = CharField()
    status = IntegerField()
    assignee = CharField()
    my_type = IntegerField()

    class Meta:
        database = db # This model uses the "people.db" database.


class Flags(Model):
    fogstream_empty = TimeField(null=True)

    class Meta:
        database = db # This model uses the "people.db" database.

class IssueLists(Model):
    list_type = IntegerField(choices=ISSUE_TYPE.fogstream)
    time = DateTimeField()
    issues = TextField()
