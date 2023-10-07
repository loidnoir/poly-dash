from peewee import *

from app import BaseModel


class User(BaseModel):
    id = IntegerField()
    group = IntegerField()
    lab = IntegerField()
    english = IntegerField() # 0->9703, 1->2127, 2->9706, 3->9708, 4->2353ա, 5->2353, 6->2338