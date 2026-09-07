"""Capacidade de estoque congelado, derretimento e gelo do isopor."""

from ..content.ingredients import UNIDADES_POR_SACO_GELO
from ..content.locations import (
    BONUS_AJUDANTE_CAPACIDADE,
    BONUS_FREEZER_MAIOR,
    LOCAIS,
)
from .state import GameState


def capacidade_total(state: GameState) -> int:
    cap = state.capacidade_freezer
    if "freezer_maior" in state.upgrades:
        cap += BONUS_FREEZER_MAIOR
    return cap


def capacidade_dia(state: GameState, local_key: str) -> int:
    """Quantas unidades da pra levar e vender no ponto hoje.

    Fora de casa quem manda e o isopor: sem caixa boa nao adianta o ponto
    ser movimentado.
    """
    cap = LOCAIS[local_key].capacidade
    if local_key != "casa":
        from ..content.coolers import ISOPORES
        if not isopor_vivo(state):
            return 0  # sem isopor nao tem como levar mercadoria pra rua
        cap = min(cap, ISOPORES[state.isopor].capacidade)
    if "ajudante" in state.upgrades:
        cap += BONUS_AJUDANTE_CAPACIDADE
    return cap


def fator_derretimento(state: GameState) -> float:
    """Quanto o isopor em uso segura o derretimento."""
    if state.isopor:
        from ..content.coolers import ISOPORES
        return ISOPORES[state.isopor].derretimento
    return 1.0


def isopor_vivo(state: GameState) -> bool:
    return bool(state.isopor) and state.isopor_dias > 0


def excesso(state: GameState) -> int:
    return max(0, state.inventario.total_prontos() - capacidade_total(state))


def derretimento_por_excesso(state: GameState) -> dict[str, int]:
    """Estoque acima da capacidade derrete. Isopor termico corta pela metade."""
    sobra = excesso(state)
    if sobra <= 0:
        return {}
    sobra = round(sobra * fator_derretimento(state))
    return _tirar_proporcional(state, sobra)


def cobertura_do_saco(heat_index: float) -> int:
    """Quantas unidades um saco de gelo segura num dia desse calor.

    No calor o gelo derrete mais rapido, entao um saco rende menos. E isso
    que faz a decisao ter peso: no dia escaldante voce vende mais E precisa
    de mais gelo, com o mesmo dinheiro no bolso.
    """
    fator = 1.0 + max(0.0, heat_index - 28.0) * 0.06
    return max(20, round(UNIDADES_POR_SACO_GELO / fator))


def falta_de_gelo(state: GameState, local_key: str, gelo_sacos: int,
                  unidades: int, heat_index: float = 26.0) -> dict[str, int]:
    """Fora de casa, sem gelo suficiente o estoque do dia derrete."""
    if local_key == "casa" or unidades <= 0:
        return {}
    coberto = gelo_sacos * cobertura_do_saco(heat_index)
    descoberto = max(0, unidades - coberto)
    if descoberto <= 0:
        return {}
    perde = round(descoberto * fator_derretimento(state))
    return _tirar_proporcional(state, perde)


def _tirar_proporcional(state: GameState, quantidade: int) -> dict[str, int]:
    """Remove N unidades do estoque pronto, proporcional ao que tem de cada sabor."""
    prontos = state.inventario.prontos
    total = sum(prontos.values())
    if total <= 0 or quantidade <= 0:
        return {}
    quantidade = min(quantidade, total)
    perdas: dict[str, int] = {}
    restante = quantidade
    for k in sorted(prontos, key=lambda x: -prontos[x]):
        if restante <= 0:
            break
        tira = min(prontos[k], round(quantidade * prontos[k] / total))
        tira = min(tira, restante)
        if tira > 0:
            prontos[k] -= tira
            perdas[k] = perdas.get(k, 0) + tira
            restante -= tira
    # Arredondamento pode deixar sobra: tira de quem ainda tiver.
    for k in sorted(prontos, key=lambda x: -prontos[x]):
        if restante <= 0:
            break
        tira = min(prontos[k], restante)
        if tira > 0:
            prontos[k] -= tira
            perdas[k] = perdas.get(k, 0) + tira
            restante -= tira
    for k in [k for k, v in prontos.items() if v <= 0]:
        del prontos[k]
    return perdas
