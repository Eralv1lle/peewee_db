from peewee import *


con = SqliteDatabase(r"C:\Users\user\PycharmProjects\peewee_db\users.db")

class Person(Model):
    id = PrimaryKeyField(primary_key=True, unique=True)
    login = CharField()
    password = CharField()

    class Meta:
        database = con
        db_table = "Users"

