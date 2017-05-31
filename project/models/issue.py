# coding=utf-8
from aenum import AutoNumberEnum, Enum
from peewee import *

db = SqliteDatabase('jira.db')


class ISSUE_TYPE(AutoNumberEnum):
    fogstream = u"Фогстрим"

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


class Flags(Model):
    fogstream_empty = TimeField(null=True)

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




