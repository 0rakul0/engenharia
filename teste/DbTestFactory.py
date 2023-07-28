from pdjus.conexao.Conexao import db, SqliteExtDatabase, default_schema, Singleton, SessionDB
from pdjus.modelo import *

class DbTestFactory(metaclass=Singleton):


    def __init__(self):
        default_schema = None

        test_db = SqliteExtDatabase(':memory:')
        db = test_db
        db.connect()
        tran = SessionDB().transaction
        tran.db = db
        base = BaseClass()
        MODELS = base.subclasses
        for model in MODELS:
            model._meta.database = db
            model._meta.schema = None
            for attr in model._meta.columns:
                model._meta.columns[attr].null = True

        db.create_tables(MODELS)

# RODAR SÓ EM TESTES, PORQUE É CRIADO UM BANCO EM MEMÓRIA E QUALQUER EXECUÇÃO SERÁ FEITO NO BANCO E MEMÓRIA!