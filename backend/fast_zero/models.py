from datetime import datetime
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.UUIDField(primary_key=True)
    username = fields.CharField(max_length=30)
    email = fields.CharField(max_length=100)
    password = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(default=datetime.now)
    is_admin = fields.BooleanField(default=False)
    estabelecimento = fields.ForeignKeyField('models.Estabelecimento',related_name='estabelecimento',on_delete=fields.OnDelete.CASCADE)

    def __str__(self):
        return self.username

class Funcionalidade(Model):
    id = fields.IntField(primary_key=True)
    nome = fields.CharField(max_length=100)

class Pacote(Model):
    id = fields.UUIDField(primary_key=True)
    funcionalidades = fields.ManyToManyField('models.Funcionalidade')
    created_at = fields.DatetimeField(default=datetime.now)

class Estabelecimento(Model):
    id = fields.UUIDField(primary_key=True)
    icone_path = fields.CharField(max_length=255)
    pacote = fields.OneToOneField('models.Pacote')
    created_at = fields.DatetimeField(default=datetime.now)
    cidade = fields.CharField(max_length=100)

class Orgao(Model):
    id = fields.UUIDField(primary_key=True)
    estabelecimento = fields.ForeignKeyField('models.Estabelecimento',related_name='orgaos',on_delete=fields.OnDelete.CASCADE)
    descricao = fields.CharField(max_length=200)
    cnpj = fields.CharField(max_length=11)
    endereco = fields.CharField(max_length=150)

class Document(Model):
    id = fields.UUIDField(primary_key=True)
    file_name = fields.CharField(max_length=100)
    file_path = fields.CharField(max_length=255)
    sender = fields.ForeignKeyField('models.User',related_name='user',on_delete=fields.OnDelete.CASCADE)
    uploaded_at = fields.DatetimeField(default=datetime.now)
    orgao = fields.ForeignKeyField('models.Orgao',related_name='orgaos',on_delete=fields.OnDelete.CASCADE)
    tipo = fields.CharField(max_length=30)
    numero = fields.IntField(unique=True,auto_increment=True)

    def __str__(self):
        return self.file_name

class DiarioOficial(Model):
    id = fields.UUIDField(primary_key=True)
    titulo = fields.CharField(max_length=50)
    file_path = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(default=datetime.now)
    published_at = fields.DatetimeField(null=True)
    is_published = fields.BooleanField(default=False)
    signed = fields.BooleanField(default=False)
    sender = fields.ForeignKeyField('models.User',related_name='user',on_delete=fields.OnDelete.CASCADE)