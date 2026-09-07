"""Estado mutavel do jogo, plano do dia e resultado do dia."""

from collections.abc import Mapping
from dataclasses import dataclass, field

from .models import Weather
from .types import BarkTag, Centavos


@dataclass
class Lote:
    """Lote de insumo com validade, consumido em FIFO."""

    qtd: float
    dia_validade: int | None  # dia do jogo em que vence; None = nao perece


@dataclass
class Inventory:
    ingredientes: dict[str, list[Lote]] = field(default_factory=dict)
    prontos: dict[str, int] = field(default_factory=dict)
    gelo_sacos: int = 0

    def total(self, key: str) -> float:
        return sum(l.qtd for l in self.ingredientes.get(key, ()))

    def total_prontos(self) -> int:
        return sum(self.prontos.values())

    def adicionar(self, key: str, qtd: float, dia_validade: int | None) -> None:
        self.ingredientes.setdefault(key, []).append(Lote(qtd, dia_validade))

    def consumir(self, key: str, qtd: float) -> bool:
        """Consome em FIFO. Retorna False (sem alterar nada) se faltar."""
        if self.total(key) + 1e-9 < qtd:
            return False
        restante = qtd
        lotes = self.ingredientes.get(key, [])
        for lote in lotes:
            if restante <= 1e-9:
                break
            usa = min(lote.qtd, restante)
            lote.qtd -= usa
            restante -= usa
        self.ingredientes[key] = [l for l in lotes if l.qtd > 1e-9]
        return True

    def expirar(self, dia: int) -> dict[str, float]:
        """Remove lotes vencidos. Retorna o que foi perdido por insumo."""
        perdas: dict[str, float] = {}
        for key, lotes in list(self.ingredientes.items()):
            vivos, mortos = [], 0.0
            for lote in lotes:
                if lote.dia_validade is not None and lote.dia_validade < dia:
                    mortos += lote.qtd
                else:
                    vivos.append(lote)
            if mortos > 1e-9:
                perdas[key] = mortos
            self.ingredientes[key] = vivos
        return perdas


@dataclass
class GameState:
    versao: int = 1
    seed: int = 0
    regiao: str = "ce"
    dia: int = 1
    caixa: Centavos = 8000
    reputacao: float = 50.0
    local_atual: str = "casa"
    locais_desbloqueados: list[str] = field(default_factory=lambda: ["casa"])
    inventario: Inventory = field(default_factory=Inventory)
    capacidade_freezer: int = 60
    upgrades: set[str] = field(default_factory=set)
    historico: list["DayResult"] = field(default_factory=list)
    vendas_recentes: dict[str, int] = field(default_factory=dict)
    socorro_usado: bool = False        # a ajuda de recomeco ja foi dada?
    isopor: str | None = None          # qual caixa esta em uso
    isopor_dias: int = 0               # dias de uso que ainda aguenta
    encerrado: str | None = None  # None | "falencia" | "vitoria"


@dataclass(frozen=True, slots=True)
class DayPlan:
    producao: Mapping[str, int]
    precos: Mapping[str, Centavos]
    local: str
    compras: Mapping[str, int] = field(default_factory=dict)
    gelo: int = 0


@dataclass(frozen=True, slots=True)
class FlavorOutcome:
    flavor: str
    ofertados: int
    vendidos: int
    preco: Centavos
    receita: Centavos
    perdidos_derretimento: int
    demanda_potencial: int


@dataclass(frozen=True, slots=True)
class EventOutcome:
    key: str
    text_key: str
    params: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DayResult:
    dia: int
    clima: Weather
    local: str
    eventos: tuple[EventOutcome, ...]
    por_sabor: tuple[FlavorOutcome, ...]
    receita: Centavos
    custo_insumos: Centavos
    custo_fixo: Centavos
    lucro: Centavos
    caixa_final: Centavos
    reputacao_delta: float
    barks: tuple[tuple[BarkTag, str], ...] = ()

    @property
    def vendidos(self) -> int:
        return sum(f.vendidos for f in self.por_sabor)

    @property
    def demanda_nao_atendida(self) -> int:
        return sum(max(0, f.demanda_potencial - f.vendidos) for f in self.por_sabor)
