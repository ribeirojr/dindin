"""Sorteio e aplicacao dos eventos aleatorios do dia."""

from random import Random

from ..content.event_pool import elegiveis
from .freezer import _tirar_proporcional
from .models import GameEvent
from .state import EventOutcome, GameState
from .types import Centavos

MAX_EVENTOS_DIA = 2


def sortear(regiao: str, local: str, rng: Random) -> list[GameEvent]:
    escolhidos: list[GameEvent] = []
    for ev in elegiveis(regiao, local):
        if rng.random() < ev.peso:
            escolhidos.append(ev)
        if len(escolhidos) >= MAX_EVENTOS_DIA:
            break
    return escolhidos


def aplicar(
    state: GameState, eventos: list[GameEvent]
) -> tuple[float, Centavos, tuple[EventOutcome, ...]]:
    """Retorna (mod_trafego, custo_extra, outcomes) e mexe no estoque se preciso."""
    mod = 1.0
    custo: Centavos = 0
    outs: list[EventOutcome] = []

    for ev in eventos:
        if ev.key == "queda_energia" and "gerador" in state.upgrades:
            outs.append(EventOutcome(ev.key, "evento.queda_energia_gerador"))
            continue

        mod *= ev.trafego_mod
        custo += ev.custo_extra
        params: dict[str, object] = {}

        if ev.derrete_frac > 0:
            total = state.inventario.total_prontos()
            perde = int(total * ev.derrete_frac)
            if "isopor_termico" in state.upgrades:
                perde //= 2
            perdas = _tirar_proporcional(state, perde)
            params["perdidos"] = sum(perdas.values())

        if ev.custo_extra:
            params["valor"] = abs(ev.custo_extra)

        outs.append(EventOutcome(ev.key, f"evento.{ev.key}", params))

    return mod, custo, tuple(outs)
