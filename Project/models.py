from database.db import database

class Person(database):
    def __init__(self,name,age):
        self.name = name
        self.age = age