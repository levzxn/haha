from datetime import datetime
from tortoise.models import Model
from tortoise import fields

class Document(Model):
    id = fields.UUIDField(primary_key=True)
    file_name = fields.CharField(max_length=100)
    file_path = fields.CharField(max_length=255)
    sender = fields.UUIDField()
    uploaded_at = fields.DatetimeField(default=datetime.now)
    orgao = fields.UUIDField()
    tipo = fields.CharField(max_length=30)

    def __str__(self):
        return self.file_name

class DiarioOficial(Model):
    id = fields.UUIDField(primary_key=True)
    titulo = fields.CharField(max_length=50)
    file_path = fields.CharField(max_length=255)
    chunks = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.now)
    published_at = fields.DatetimeField(null=True)
    is_published = fields.BooleanField(default=False)
    signed = fields.BooleanField(default=False)
    sender = fields.UUIDField()