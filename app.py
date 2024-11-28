from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from logger import logger
from model import Session, Gasto
from schemas import *
from flask_cors import CORS
from pydantic import ValidationError  


info = Info(title="Organizacao de gastos API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
gasto_tag = Tag(name="gasto", description="Adição, visualização e remoção de produtos à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

## rota de verificação de duplicidade
@app.get('/gasto/existe', responses={"200": {"application/json": {"schema": {"type": "object", "properties": {"exists": {"type": "boolean"}}}}}})
def check_gasto_existe():
    """ 
        Verifica se um gasto com a combinação 
        de descricao e data já existe. Retorna 
        um booleano indicando a existência da combinação. 
    """ 
    descricao = request.args.get('descricao') 
    data_gasto = request.args.get('data')
    
    # Adicionando logs para depuração 
    print(f"Parâmetros recebidos: descricao={descricao}, data={data_gasto}") 
    if not descricao or not data_gasto: 
        print("Parâmetros insuficientes") 
        return {"exists": False}, 400 # Retorna um erro 400 se faltar 'descricao' ou 'data'
    
    
    ## continua
    gasto_descricao = unquote(descricao)
    gasto_data = unquote(data_gasto)

    # Log dos valores após unquote 
    print(f"Valores após unquote: descricao={gasto_descricao}, data={gasto_data}")

    session = Session()
    
    # Adicionando logs para depuração
    print(f"Verificando existencia: descricao={gasto_descricao}, data={gasto_data}")
    
    try:
        exists = session.query(Gasto).filter(Gasto.descricao == gasto_descricao, Gasto.data == gasto_data).first() is not None
        
        # Log do resultado da consulta
        print(f"Resultado da verificação: exists={exists}")
    except Exception as e:
        # Log do erro
        print(f"Erro na verificação de existencia: {str(e)}")
        return {"exists": False}, 500
    finally:
        session.close()
        
    return {"exists": exists}

@app.post('/gasto', tags=[gasto_tag],
          responses={"200": GastoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_gasto(form: GastoSchema):
    """Adiciona um novo Gasto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    novo_gasto = Gasto(
        descricao=form.descricao,
        data=form.data,
        classificacao=form.classificacao,
        valor=form.valor)
    logger.debug(f"Adicionando gasto com a seguinte descricao: '{novo_gasto.descricao}'")
    try:
        # criando conexão com a base
        session = Session()

        # !!!!!!!!!!!!!!!!!!!!!! Verificação de duplicidade de descricao e data !!!!!!!!!!!!!!!!!!!!!!
        exists = session.query(Gasto).filter(Gasto.descricao == form.descricao, Gasto.data == form.data).first()
        if exists:
            error_msg = "Gasto com a mesma descricao e data já salvo na base :/"
            logger.warning(f"Erro ao adicionar gasto '{novo_gasto.descricao}', {error_msg}")
            return {"mesage": error_msg}, 409

        # adicionando Gasto
        session.add(novo_gasto)
        # efetivando o comando de adição de novo Gasto na tabela
        session.commit()
        logger.debug(f"Adicionado gasto com a seguinte descricao: '{novo_gasto.descricao}'")
        return apresenta_gasto(novo_gasto), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar gasto '{novo_gasto.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/gastos', tags=[gasto_tag],
         responses={"200": ListagemGastoSchema, "404": ErrorSchema})
def get_gastos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando gastos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    gastos = session.query(Gasto).all()

    if not gastos:
        # se não há gastos cadastrados
        return {"gastos": []}, 200
    else:
        logger.debug(f"%d gastos encontrados" % len(gastos))
        # retorna a representação de gastos
        print(gastos)
        return apresenta_gastos(gastos), 200


@app.get('/gasto', tags=[gasto_tag],
         responses={"200": GastoViewSchema, "404": ErrorSchema})
def get_gasto(query: GastoBuscaSchema):
    """Faz a busca por um gasto a partir do id do gasto

    Retorna uma representação dos gastos e comentários associados.
    """
    gasto_id = query.id
    logger.debug(f"Coletando dados sobre gasto #{gasto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    gasto = session.query(Gasto).filter(Gasto.id == gasto_id).first()

    if not gasto:
        # se o gasto não foi encontrado
        error_msg = "Gasto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{gasto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Gasto encontrado: '{gasto.descricao}'")
        # retorna a representação de Gasto
        return apresenta_gasto(gasto), 200


@app.delete('/gasto', tags=[gasto_tag],
            responses={"200": GastoDelSchema, "404": ErrorSchema})
def del_gasto(query: GastoBuscaSchema):
    """Deleta um gasto a partir do nome de gasto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    gasto_descricao = unquote(query.descricao) ## alterado paremetro busca para delete
    gasto_data = unquote(query.data)

    logger.debug(f"Deletando dados sobre gasto com descricao '{gasto_descricao}' e data '{gasto_data}'")
    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Gasto).filter(Gasto.descricao == gasto_descricao, Gasto.data == gasto_data).delete() 
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado gasto com descricao '{gasto_descricao}' e data '{gasto_data}'")
        return {"message": "Gasto removido", "descricao": gasto_descricao, "data": gasto_data}
    else:
        # se o produto não foi encontrado
        error_msg = "Gasto não encontrado na base :/"
        logger.warning(f"Erro ao deletar gasto com descricao '{gasto_descricao}' e data '{gasto_data}', {error_msg}")
        return {"mesage": error_msg}, 404

