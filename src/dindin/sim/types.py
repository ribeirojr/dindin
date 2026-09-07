"""Enums e tipos primitivos da simulacao."""

from enum import StrEnum

type Centavos = int


class Tier(StrEnum):
    SIMPLES = "simples"
    GOURMET = "gourmet"


class WeatherKind(StrEnum):
    ESCALDANTE = "escaldante"
    QUENTE = "quente"
    ABAFADO = "abafado"
    NUBLADO = "nublado"
    CHUVA = "chuva"
    TEMPORAL = "temporal"
    FRIO = "frio"


class Season(StrEnum):
    VERAO = "verao"
    OUTONO = "outono"
    INVERNO = "inverno"
    PRIMAVERA = "primavera"


class EventKind(StrEnum):
    CLIMA = "clima"
    SOCIAL = "social"
    PROBLEMA = "problema"
    SORTE = "sorte"
    CALENDARIO = "calendario"


class BarkTag(StrEnum):
    COMPRA_SIMPLES = "compra_simples"
    COMPRA_GOURMET = "compra_gourmet"
    PRECO_ALTO = "preco_alto"
    PRECO_BARATO = "preco_barato"
    FILA = "fila"
    SELLOUT = "sellout"
    CALOR = "calor"
    CHUVA = "chuva"


# Multiplicador de trafego por dia da semana (0=segunda .. 6=domingo).
DIA_SEMANA_MOD: tuple[float, ...] = (0.85, 0.88, 0.92, 0.98, 1.15, 1.30, 1.20)

# Escola inverte: movimento em dia letivo, deserto no fim de semana.
DIA_SEMANA_MOD_ESCOLA: tuple[float, ...] = (1.20, 1.22, 1.20, 1.18, 1.10, 0.25, 0.20)

PENALIDADE_CLIMA: dict[WeatherKind, float] = {
    WeatherKind.ESCALDANTE: 1.15,
    WeatherKind.QUENTE: 1.00,
    WeatherKind.ABAFADO: 1.05,
    WeatherKind.NUBLADO: 0.80,
    WeatherKind.CHUVA: 0.42,
    WeatherKind.TEMPORAL: 0.18,
    WeatherKind.FRIO: 0.30,
}
