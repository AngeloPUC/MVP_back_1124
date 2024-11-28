from pydantic import BaseModel, validator
from datetime import datetime
from typing import List
from model.gasto import Gasto

class GastoSchema(BaseModel):
    """ Define como um novo Gasto a ser inserido deve ser representado
    """
    descricao: str = "restaurante banana da terra"
    data: str = "01/01"  
    @validator('data', pre=True) 
    def parse_date(cls, value): 
        if isinstance(value, str): 
            try: 
                return datetime.strptime(value, '%d/%m').strftime('%d/%m') 
            except ValueError: 
                raise ValueError('Date format should be dd/mm') 
        return value
      
    classificacao: str = "alimentacao"
    valor: float = 150.00

class GastoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
    """
    descricao: str
    data: str

class ListagemGastoSchema(BaseModel):
    """ Define como uma listagem de gasto será retornada.
    """
    gastos: List[GastoSchema]

def apresenta_gastos(gastos: List[Gasto]):
    """ Retorna uma representação do gasto seguindo o schema definido em
        GastoViewSchema.
    """
    result = []
    for gasto in gastos:
        result.append({
            "id": gasto.id,
            "descricao": gasto.descricao,
            "data": gasto.data,
            "classificacao": gasto.classificacao,
            "valor": gasto.valor,
        })

    return {"gastos": result}

class GastoViewSchema(BaseModel):
    """ Define como um gasto será retornado.
    """
    id: int = 1
    descricao: str = "restaurante banana da terra"
    data: str = "01/01"
    classificacao: str = "alimentacao"
    valor: float = 150.00

class GastoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str 
    descricao: str

def apresenta_gasto(gasto: Gasto):
    """ Retorna uma representação do gasto seguindo o schema definido em
        GastoViewSchema.
    """
    return {
        "id": gasto.id,
        "descricao": gasto.descricao,
        "data": gasto.data,
        "classificacao": gasto.classificacao,
        "valor": gasto.valor,
    }
