from tortoise.models import Model
from tortoise import fields
from datetime import datetime

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
    funcionalidades = fields.ManyToManyField('models.Funcionalidade',related_name='funcionalidades')
    created_at = fields.DatetimeField(default=datetime.now)

class Estabelecimento(Model):
    id = fields.UUIDField(primary_key=True)
    nome = fields.CharField(max_length=30)
    icone_path = fields.CharField(max_length=255)
    pacote = fields.OneToOneField('models.Pacote')
    created_at = fields.DatetimeField(default=datetime.now)
    cidade = fields.CharField(max_length=100)

class Orgao(Model):
    id = fields.UUIDField(primary_key=True)
    estabelecimento = fields.ForeignKeyField('models.Estabelecimento',related_name='estabelecimento_pertencente',on_delete=fields.OnDelete.CASCADE)
    descricao = fields.CharField(max_length=200)
    cnpj = fields.CharField(max_length=11)
    endereco = fields.CharField(max_length=150)
