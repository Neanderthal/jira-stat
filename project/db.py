import os

from peewee import *

fileDir = os.path.dirname(os.path.realpath(__file__))
db = SqliteDatabase(os.path.join(fileDir, 'jira.db'))
