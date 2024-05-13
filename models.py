from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

USUARIO = 'root'
SENHA = ''
HOST = 'localhost'
BANCO = 'api_python'
PORT = 3306
CONNECTION = f'mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}'

engine = create_engine(CONNECTION, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Pessoa(Base):
    __tablename__ = 'pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    usuario = Column(String(20))
    senha = Column(String(10))


class Tokens(Base): # responsável por gerar tokens
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('pessoa.id'))
    token = Column(DateTime, default=datetime.datetime.now())


Base.metadata.create_all(engine)
