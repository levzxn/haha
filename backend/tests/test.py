from fastapi import FastAPI
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

app = FastAPI()

# Modelos de exemplo
class Funcionalidade(Model):
    id = fields.IntField(pk=True)
    nome = fields.CharField(max_length=100)

class Pacote(Model):
    id = fields.UUIDField(pk=True)
    funcionalidades = fields.ManyToManyField('models.Funcionalidade', related_name='pacotes')

# Função de inicialização
async def init():
    await Tortoise.init(
        db_url="sqlite://:memory:",  # Usando banco de dados na memória
        modules={"models": ["__main__"]}  # Apontando para o módulo atual
    )
    await Tortoise.generate_schemas()  # Gerando as tabelas

# Função de teste para criar objetos
async def teste():
    # Criando uma funcionalidade e associando-a a um pacote
    f1 = await Funcionalidade.create(nome='DOEM')
    f2 = await Funcionalidade.create(nome="Licitação")
    pacote = await Pacote.create()
    await pacote.funcionalidades.add(f1)
    await pacote.funcionalidades.add(f2)


    lista =[funcionalidade for funcionalidade in await pacote.funcionalidades.all()]
    for func in lista:
        print(func.nome)
# Função principal para rodar tudo
async def run():
    await init()  # Inicializando o banco de dados
    await teste()  # Executando o teste
    await Tortoise.close_connections()  # Fechando conexões ao final

# Executando o código assíncrono
#run_async(run())
