"""Datas comemorativas que mexem no movimento."""

from datetime import date, timedelta

from .state import EventOutcome

# key -> (nome_i18n, multiplicador de trafego)
_FIXOS: dict[tuple[int, int], tuple[str, float]] = {
    (6, 12): ("dia_namorados", 1.15),
    (6, 24): ("sao_joao", 1.55),
    (6, 29): ("sao_pedro", 1.35),
    (9, 7): ("independencia", 1.25),
    (10, 12): ("dia_criancas", 1.60),
    (12, 25): ("natal", 0.70),
    (1, 1): ("ano_novo", 0.75),
}


def _pascoa(ano: int) -> date:
    a = ano % 19
    b, c = divmod(ano, 100)
    d, e = divmod(b, 4)
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l) // 433
    mes = (h + l - 7 * m + 90) // 25
    dia = (h + l - 7 * m + 33 * mes + 19) % 32
    return date(ano, mes, dia)


def eventos_do_dia(d: date) -> list[tuple[str, float]]:
    """Retorna [(key, mod_trafego)] das datas especiais de hoje."""
    achados: list[tuple[str, float]] = []
    if (d.month, d.day) in _FIXOS:
        achados.append(_FIXOS[(d.month, d.day)])

    # Terca de carnaval = 47 dias antes da Pascoa; a folia vai de sabado a terca.
    terca = _pascoa(d.year) - timedelta(days=47)
    if terca - timedelta(days=3) <= d <= terca:
        achados.append(("carnaval", 1.70))

    # Junho inteiro tem clima de festa junina.
    if d.month == 6 and not any(k == "sao_joao" for k, _ in achados):
        achados.append(("mes_junino", 1.10))

    # Ferias escolares: janeiro, e julho.
    if d.month in (1, 7):
        achados.append(("ferias", 1.20))

    return achados


def mod_calendario(d: date) -> float:
    mod = 1.0
    for _, m in eventos_do_dia(d):
        mod *= m
    return mod


def outcomes_calendario(d: date) -> tuple[EventOutcome, ...]:
    return tuple(EventOutcome(key=k, text_key=f"evento.{k}")
                 for k, _ in eventos_do_dia(d))
