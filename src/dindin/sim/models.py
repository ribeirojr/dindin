"""Estruturas de dados de conteudo: regiao, sabor, insumo, ponto de venda."""

from collections.abc import Mapping
from dataclasses import dataclass, field

from .types import Centavos, Season, Tier, WeatherKind


@dataclass(frozen=True, slots=True)
class Region:
    key: str
    nome: str
    gentilico: str
    clima: Mapping[Season, Mapping[WeatherKind, float]]
    base_temp_c: tuple[float, float]
    preferencia: Mapping[str, float]
    tolerancia_preco: float
    custo_insumo_mod: float
    eventos_exclusivos: tuple[str, ...] = ()

    def pref(self, flavor_key: str) -> float:
        return self.preferencia.get(flavor_key, 1.0)


@dataclass(frozen=True, slots=True)
class Ingredient:
    key: str
    nome: str
    unidade: str
    preco_base: Centavos
    validade_dias: int | None
    refrigerado: bool = False
    bulk: tuple[tuple[int, float], ...] = ()

    def preco_unitario(self, qtd: int, custo_mod: float) -> Centavos:
        """Preco por unidade aplicando desconto por volume e modificador regional."""
        fator = 1.0
        for minimo, desconto in self.bulk:
            if qtd >= minimo:
                fator = desconto
        return round(self.preco_base * fator * custo_mod)


@dataclass(frozen=True, slots=True)
class Flavor:
    key: str
    nome: str
    tier: Tier
    receita: Mapping[str, float]  # insumo_key -> qtd para 10 unidades
    apelo_base: float
    preco_ref: Centavos
    desbloqueio: str | None = None

    def consumo(self, unidades: int) -> dict[str, float]:
        """Insumos necessarios para produzir N unidades."""
        return {k: v * unidades / 10.0 for k, v in self.receita.items()}


@dataclass(frozen=True, slots=True)
class Location:
    key: str
    nome: str
    ordem: int
    meta_caixa: Centavos
    custo_entrada: Centavos
    trafego_base: int
    tolerancia_mod: float
    sensibilidade_clima: float
    chuva_mod: float
    capacidade: int
    custo_fixo_dia: Centavos
    gourmet_afinidade: float
    escala_semana_escolar: bool = False


@dataclass(frozen=True, slots=True)
class Upgrade:
    key: str
    nome: str
    custo: Centavos
    desbloqueio: str
    descricao: str


@dataclass(frozen=True, slots=True)
class Weather:
    kind: WeatherKind
    temp_c: float
    umidade: float
    heat_index: float


@dataclass(frozen=True, slots=True)
class GameEvent:
    key: str
    kind: "EventKindAlias"
    peso: float
    trafego_mod: float = 1.0
    derrete_frac: float = 0.0
    custo_extra: Centavos = 0
    regioes: tuple[str, ...] = ()
    locais: tuple[str, ...] = ()
    params: Mapping[str, object] = field(default_factory=dict)


# Alias tardio para evitar import circular na anotacao acima.
from .types import EventKind as EventKindAlias  # noqa: E402
