from sqlalchemy import Column, String, Integer, Float
from datetime import datetime
from model import Base
from enum import Enum as PyEnum

class ClassificacaoOpcao(PyEnum):
    Recorrente = "Recorrente"
    Alimentacao = "Alimentacao"
    Transporte = "Transporte"
    Entretenimento = "Entretenimento"
    Saude = "Saude"
    Educacao = "Educacao"
    Vestuario = "Vestuario"
    Outros = "Outros"

class Gasto(Base):
    __tablename__ = 'gasto'

    id = Column("pk_gasto", Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(140))
    data = Column(String(5))
    
    @staticmethod 
    def validate_date_format(value): 
        if isinstance(value, str): 
            try:
                day, month = map(int, value.split('/'))
                if 1 <= day <= 31 and 1 <= month <= 12: 
                    return value 
                else: 
                    raise ValueError('Dia ou mês fora do intervalo válido') 
            except (ValueError, IndexError): 
                raise ValueError('Date format should be dd/mm') 
        raise ValueError('Date must be a string in dd/mm format')

    classificacao = Column(String(50))

    @staticmethod
    def validate_classificacao(value): 
        if value not in ClassificacaoOpcao._value2member_map_: 
            raise ValueError(f'Classificação inválida: {value}') 
        return value
    
    valor = Column(Float)

    def __init__(self, descricao: str, data: str, classificacao: str, valor: float):
        """
        Cria um Gasto

        Arguments:
            descricao: Descrição do gasto.
            data: Data do gasto
            classificacao: Classe do gasto.
            valor: valor gasto.
        """
        self.descricao = descricao
        self.data = self.validate_date_format(data)
        self.classificacao = self.validate_classificacao(classificacao)
        self.valor = valor
    