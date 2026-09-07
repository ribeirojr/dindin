"""O coracao do jogo: quantas unidades sao vendidas.

Modelo multiplicativo sobre fatores independentes, com uma unica curva
logistica de preco. O ruido e aplicado UMA vez sobre o trafego total
(nunca por sabor), para que a pericia domine o acaso.
"""

import math
from collections.abc import Mapping
from random import Random

from ..content.locations import LOCAIS
from ..content.regions import REGIOES
from .models import Flavor, Location, Region, Weather
from .types import (
    DIA_SEMANA_MOD,
    DIA_SEMANA_MOD_ESCOLA,
    PENALIDADE_CLIMA,
    Centavos,
    Tier,
    WeatherKind,
)

# Curva de preco: logistica 1/(1+exp(K*(r-MID))).
# MID=1.30 coloca o otimo de receita em r~1.027, ou seja, uma margem
# modesta ACIMA do preco de referencia. Com MID=1.12 o otimo cairia em
# r~0.878 e furar preco seria dominante -- o oposto do desenho.
CURVA_K = 6.0
CURVA_MID = 1.30

# Fracao da demanda nao atendida que migra para outro sabor com estoque.
CONVERSAO_SOBRA = 0.35

TEMP_NEUTRA = 26.0
NOVIDADE_PENAL = 0.85
DIAS_PARA_ENJOAR = 5


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def heat_index(temp_c: float, umidade: float) -> float:
    """Sensacao termica simplificada: umidade alta amplifica o calor."""
    if temp_c < 20.0:
        return temp_c
    return temp_c + 0.9 * (umidade - 0.5) * max(0.0, temp_c - 20.0) * 0.35


def f_clima(hi: float, kind: WeatherKind, sensibilidade: float) -> float:
    base = clamp(1.0 + 0.055 * (hi - TEMP_NEUTRA), 0.35, 2.10)
    raw = base * PENALIDADE_CLIMA[kind]
    return 1.0 + (raw - 1.0) * sensibilidade


def f_dia_semana(weekday: int, local: Location) -> float:
    tabela = DIA_SEMANA_MOD_ESCOLA if local.escala_semana_escolar else DIA_SEMANA_MOD
    return tabela[weekday % 7]


def f_reputacao(rep: float) -> float:
    return clamp(0.75 + 0.005 * rep, 0.75, 1.25)


def tolerancia_efetiva(regiao: Region, local: Location, hi: float) -> float:
    """Calor faz o cliente aceitar pagar mais -- subir preco na onda de calor compensa."""
    base = regiao.tolerancia_preco * local.tolerancia_mod
    return base * (1.0 + 0.10 * max(0.0, hi - 32.0) / 6.0)


def f_preco(preco: Centavos, preco_ref: Centavos, tolerancia: float) -> float:
    justo = preco_ref * tolerancia
    if justo <= 0:
        return 0.0
    r = preco / justo
    return 1.0 / (1.0 + math.exp(CURVA_K * (r - CURVA_MID)))


def tier_mod(tier: Tier, local: Location, hi: float) -> float:
    if tier is Tier.GOURMET:
        return local.gourmet_afinidade
    # No calor extremo o pessoal quer barato e gelado, rapido.
    return 1.10 if hi > 34.0 else 1.0


def trafego(
    local: Location,
    clima: Weather,
    weekday: int,
    reputacao: float,
    mod_eventos: float,
    rng: Random,
    bonus_banner: float = 1.0,
) -> int:
    ruido = rng.triangular(0.90, 1.10, 1.0)
    t = (
        local.trafego_base
        * f_clima(clima.heat_index, clima.kind, local.sensibilidade_clima)
        * f_dia_semana(weekday, local)
        * mod_eventos
        * f_reputacao(reputacao)
        * bonus_banner
        * ruido
    )
    return max(0, round(t))


def apelo(
    flavor: Flavor,
    regiao: Region,
    local: Location,
    hi: float,
    dias_seguidos: int,
) -> float:
    novidade = NOVIDADE_PENAL if dias_seguidos >= DIAS_PARA_ENJOAR else 1.0
    return (
        flavor.apelo_base
        * regiao.pref(flavor.key)
        * tier_mod(flavor.tier, local, hi)
        * novidade
    )


def calcular_demanda(
    ofertados: Mapping[str, int],
    precos: Mapping[str, Centavos],
    sabores: Mapping[str, Flavor],
    regiao_key: str,
    local_key: str,
    clima: Weather,
    weekday: int,
    reputacao: float,
    rng: Random,
    mod_eventos: float = 1.0,
    dias_seguidos: Mapping[str, int] | None = None,
    bonus_banner: float = 1.0,
) -> tuple[dict[str, int], dict[str, int], int]:
    """Retorna (demanda_por_sabor, vendidos_por_sabor, trafego_total)."""
    regiao, local = REGIOES[regiao_key], LOCAIS[local_key]
    seguidos = dias_seguidos or {}
    ativos = [k for k, n in ofertados.items() if n > 0]
    total_trafego = trafego(local, clima, weekday, reputacao, mod_eventos, rng,
                            bonus_banner)
    if not ativos:
        return {}, {}, total_trafego

    hi = clima.heat_index
    apelos = {k: apelo(sabores[k], regiao, local, hi, seguidos.get(k, 0))
              for k in ativos}
    soma = sum(apelos.values()) or 1.0
    tol = tolerancia_efetiva(regiao, local, hi)

    demanda: dict[str, int] = {}
    for k in ativos:
        resposta = f_preco(precos[k], sabores[k].preco_ref, tol)
        demanda[k] = max(0, round(total_trafego * (apelos[k] / soma) * resposta))

    vendidos = {k: min(demanda[k], ofertados[k]) for k in ativos}

    # Sobra migra para quem ainda tem estoque, proporcional ao apelo.
    nao_atendida = sum(demanda[k] - vendidos[k] for k in ativos)
    if nao_atendida > 0:
        migrantes = round(nao_atendida * CONVERSAO_SOBRA)
        while migrantes > 0:
            com_estoque = [k for k in ativos if ofertados[k] - vendidos[k] > 0]
            if not com_estoque:
                break
            peso = sum(apelos[k] for k in com_estoque) or 1.0
            distribuiu = 0
            for k in com_estoque:
                livre = ofertados[k] - vendidos[k]
                extra = min(livre, round(migrantes * apelos[k] / peso))
                if extra > 0:
                    vendidos[k] += extra
                    demanda[k] += extra
                    distribuiu += extra
            if distribuiu == 0:
                # Resto pequeno: entrega uma unidade para o primeiro com estoque.
                k = com_estoque[0]
                vendidos[k] += 1
                demanda[k] += 1
                distribuiu = 1
            migrantes -= distribuiu

    return demanda, vendidos, total_trafego
