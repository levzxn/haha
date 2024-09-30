from datetime import datetime
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=30)
    email = fields.CharField(max_length=100)
    password = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(default=datetime.now)

    def __str__(self):
        return self.username