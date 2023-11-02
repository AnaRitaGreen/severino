from typing import Any

from source.helpers.avaliador_regex import AvaliadorRegex
from source.excecoes.expressao_invalida import ExpressaoInvalida
from source.excecoes.formato_desconhecido import FormatoDesconhecido
from source.modelos.regex_grupo_interesse import RegexGrupoInteresse
from source.modelos.habilidade import Habilidade
from source.io_manager import IOManager

class HabilidadeCalculadora(Habilidade):
    __regex = r'^([-,+]?\d+(\.\d+)?) ?([\+,\-,\*,\/]) ?([-,+]?\d+(\.\d+)?$)'
    __index_numero_esquerda = 0
    __index_operador = 2
    __index_numero_direita = 3

    @property
    def textos_ajuda(self) -> list[str]:
        return [
            'Consigo resolver cálculos no formato: operando_1 operador operando_2',
            '\toperando_1 e operando_2 devem ser números;',
            '\toperador deve ser: +, -, * ou /;',
            '\texemplo: -5 * 56.78'
        ]

    def __init__(self, io_manager: IOManager) -> None:
        self.__io_manager = io_manager
        self.__avaliar_regex = AvaliadorRegex(HabilidadeCalculadora.__regex, [
            RegexGrupoInteresse(HabilidadeCalculadora.__index_numero_esquerda, float),
            RegexGrupoInteresse(HabilidadeCalculadora.__index_operador, str),
            RegexGrupoInteresse(HabilidadeCalculadora.__index_numero_direita, float),
        ])

    def execute_ou_raise(self, comando: str) -> None:
        numero_esquerda, operador, numero_direita = self.__validar(comando)
        resultado = self.__calcular(numero_esquerda, operador, numero_direita)
        self.__io_manager.imprimir(resultado)

    def __validar(self, comando: str) -> list[Any]:
        try:
            return self.__avaliar_regex.avaliar(comando)
        except ExpressaoInvalida:
            raise FormatoDesconhecido()

    def __calcular(self, numero_esquerda: float, operador: str, numero_direita: float) -> str:
        match(operador):
            case '+': return f'{numero_esquerda + numero_direita}'
            case '-': return f'{numero_esquerda - numero_direita}'
            case '*': return f'{numero_esquerda * numero_direita}'
            case '/': return self.__tentar_dividir(numero_esquerda, numero_direita)
            case _: raise FormatoDesconhecido() # nunca atingido

    def __tentar_dividir(self, ne: float, nd: float) -> str:
        try:
            return f'{ne / nd}'
        except ZeroDivisionError:
            return 'Divisão inválida.'
