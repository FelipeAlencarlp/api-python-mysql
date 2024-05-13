from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CONNECTION, Pessoa, Tokens
from secrets import token_hex

app = FastAPI()


def conectaBanco():
    engine = create_engine(CONNECTION, echo=True)
    Session = sessionmaker(bind=engine)

    return Session()


@app.post('/cadastro')
def cadastro(nome: str, usuario: str, senha: str):
    session = conectaBanco()
    usuario = session.query(Pessoa).filter_by(usuario=usuario, senha=senha).all()

    if len(usuario) == 0:
        if senha < 4:
            return {'mensagem' : 'Senha deve conter mais que 4 caracteres'}
        
        cadastrarPessoa = Pessoa(nome=nome, usuario=usuario, senha=senha)
        session.add(cadastrarPessoa)
        session.commit()

        return {'status' : 'sucesso'}

    elif len(usuario) > 1:
        return {'status' : 'Esse usuário já existe.'}
    

@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBanco()
    usuarioExiste = session.query(Pessoa).filter_by(usuario=usuario, senha=senha).all()

    if len(usuarioExiste) == 0:
        return {'status' : 'Usuário inexistente'}

    # verifica se o usuário já fez login, se sim ele já tem um token, então altera o token
    while True:
        token = token_hex(50) # 50 * 2 caracteres = 100
        tokenExiste = session.query(Tokens).filter_by(token=token).all()

        if len(tokenExiste) == 0:
            usuarioToken = session.query(Tokens).filter_by(id_pessoa=usuarioExiste[0].id).all()

            if len(usuarioToken) == 0:
                novoToken = Tokens(id_pessoa=usuarioExiste[0].id, token=token)
                session.add(novoToken)
            
            elif len(usuarioToken) > 0:
                usuarioToken[0].token = token

            session.commit()
            
            break

    return token

