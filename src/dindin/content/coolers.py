"""Isopores: equipamento que gasta e precisa ser reposto.

Caixa de isopor nao dura pra sempre -- racha, molha o fundo, o sol come.
Depois de umas duas semanas voce compra outra. E uma compra unica que
cobre varios dias, diferente do gelo (consumivel diario).
"""

from dataclasses import dataclass

from ..sim.types import Centavos


@dataclass(frozen=True, slots=True)
class Cooler:
    key: str
    nome: str
    custo: Centavos
    dias: int              # quantos dias de uso aguenta
    capacidade: int        # quantas unidades cabem
    derretimento: float    # multiplicador de perda (1.0 = normal)
    descricao: str

    @property
    def custo_por_dia(self) -> Centavos:
        return round(self.custo / self.dias)


_C = (
    Cooler("simples", "Isopor simples", 2500, 14, 100, 1.00,
           "Barato e frágil. Racha rápido no sol."),
    Cooler("bom", "Isopor reforçado", 6000, 28, 130, 0.55,
           "Aguenta mais e conserva melhor."),
    Cooler("termico", "Caixa térmica", 13000, 45, 150, 0.40,
           "Cara, mas dura muito e quase não derrete."),
)

ISOPORES: dict[str, Cooler] = {c.key: c for c in _C}
ORDEM_ISOPORES = tuple(c.key for c in _C)

# Abaixo disso o jogo avisa que o isopor ta acabando.
AVISO_DIAS_RESTANTES = 3
