from peewee import *

db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Result(BaseModel):
    test_name = CharField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    population_size = IntegerField()
    number_of_generations = IntegerField()
    max_fitness = DoubleField()
    min_fitness = DoubleField()
    average_fitness = DoubleField()
