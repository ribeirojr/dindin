"""Sorteio de clima por regiao e estacao."""

from datetime import date
from random import Random

from ..content.regions import REGIOES
from .demand import heat_index
from .models import Weather
from .types import Season, WeatherKind

_UMIDADE_POR_CLIMA = {
    WeatherKind.ESCALDANTE: (0.35, 0.60),
    WeatherKind.QUENTE: (0.40, 0.65),
    WeatherKind.ABAFADO: (0.70, 0.92),
    WeatherKind.NUBLADO: (0.55, 0.80),
    WeatherKind.CHUVA: (0.75, 0.95),
    WeatherKind.TEMPORAL: (0.80, 0.98),
    WeatherKind.FRIO: (0.50, 0.80),
}

# Deslocamento de temperatura em relacao a faixa base da regiao.
_TEMP_SHIFT = {
    WeatherKind.ESCALDANTE: 1.00,
    WeatherKind.QUENTE: 0.72,
    WeatherKind.ABAFADO: 0.62,
    WeatherKind.NUBLADO: 0.38,
    WeatherKind.CHUVA: 0.28,
    WeatherKind.TEMPORAL: 0.22,
    WeatherKind.FRIO: 0.00,
}


def estacao(d: date) -> Season:
    """Estacoes do hemisferio sul."""
    m, dia = d.month, d.day
    if (m == 12 and dia >= 21) or m in (1, 2) or (m == 3 and dia < 20):
        return Season.VERAO
    if (m == 3) or m in (4, 5) or (m == 6 and dia < 21):
        return Season.OUTONO
    if (m == 6) or m in (7, 8) or (m == 9 and dia < 23):
        return Season.INVERNO
    return Season.PRIMAVERA


def sortear_clima(regiao_key: str, d: date, rng: Random) -> Weather:
    regiao = REGIOES[regiao_key]
    dist = regiao.clima[estacao(d)]
    kinds = list(dist.keys())
    kind = rng.choices(kinds, weights=[dist[k] for k in kinds], k=1)[0]

    tmin, tmax = regiao.base_temp_c
    shift = _TEMP_SHIFT[kind]
    centro = tmin + (tmax - tmin) * shift
    temp = centro + rng.uniform(-1.5, 1.5)
    if kind is WeatherKind.ESCALDANTE:
        temp = max(temp, tmax + 0.5)

    ulo, uhi = _UMIDADE_POR_CLIMA[kind]
    umidade = rng.uniform(ulo, uhi)
    return Weather(kind, round(temp, 1), round(umidade, 2),
                   round(heat_index(temp, umidade), 1))


def previsao(regiao_key: str, d: date, rng: Random, acerto: float = 0.80) -> WeatherKind:
    """Previsao do dia seguinte: acerta na maior parte das vezes, mas erra as vezes."""
    real = sortear_clima(regiao_key, d, rng)
    if rng.random() < acerto:
        return real.kind
    dist = REGIOES[regiao_key].clima[estacao(d)]
    kinds = list(dist.keys())
    return rng.choices(kinds, weights=[dist[k] for k in kinds], k=1)[0]
