"""Metas de capitulo, desbloqueio de pontos e fim de jogo."""

from ..content.locations import LOCAIS, ORDEM_LOCAIS, UPGRADES
from .state import GameState
from .types import Centavos

CAIXA_MINIMO_VIVO: Centavos = 500

# Quando o jogador zera tudo, o jogo empresta o basico uma vez por partida
# pra ele voltar pra casa e recomecar. Sem isso ele fica preso em R$0,00
# sem estoque e sem insumo -- morte por travamento, nao por erro dele.
AJUDA_RECOMECO: Centavos = 8000


def melhor_local(state: GameState) -> str:
    """O ponto mais avancado ja desbloqueado.

    Quem caiu pra casa (socorro, ou isopor rachado sem dinheiro) volta por
    aqui sem pagar entrada de novo -- o ponto ja e dele.
    """
    return max(state.locais_desbloqueados, key=lambda k: LOCAIS[k].ordem)


def proximo_local(state: GameState) -> str | None:
    atual = LOCAIS[state.local_atual]
    for key in ORDEM_LOCAIS:
        if LOCAIS[key].ordem == atual.ordem + 1:
            return key
    return None


def pode_desbloquear(state: GameState) -> str | None:
    """Se bateu a meta do ponto atual, devolve o proximo ponto."""
    prox = proximo_local(state)
    if prox is None or prox in state.locais_desbloqueados:
        return None
    if state.caixa >= LOCAIS[state.local_atual].meta_caixa:
        return prox
    return None


def desbloquear(state: GameState, local_key: str) -> bool:
    """Paga a entrada e muda de ponto. Falso se nao tiver caixa."""
    custo = LOCAIS[local_key].custo_entrada
    if state.caixa < custo:
        return False
    state.caixa -= custo
    if local_key not in state.locais_desbloqueados:
        state.locais_desbloqueados.append(local_key)
    state.local_atual = local_key
    return True


def comprar_isopor(state: GameState, key: str) -> bool:
    """Compra uma caixa nova. Substitui a atual (o resto vai fora)."""
    from ..content.coolers import ISOPORES

    c = ISOPORES[key]
    if state.caixa < c.custo:
        return False
    state.caixa -= c.custo
    state.isopor = key
    state.isopor_dias = c.dias
    return True


def precisa_de_isopor(state: GameState) -> bool:
    """Fora de casa, sem caixa viva nao da pra trabalhar."""
    from .freezer import isopor_vivo

    return state.local_atual != "casa" and not isopor_vivo(state)


def isopor_acabando(state: GameState) -> bool:
    from ..content.coolers import AVISO_DIAS_RESTANTES
    from .freezer import isopor_vivo

    return (isopor_vivo(state)
            and state.isopor_dias <= AVISO_DIAS_RESTANTES)


def comprar_upgrade(state: GameState, key: str) -> bool:
    up = UPGRADES[key]
    if key in state.upgrades or state.caixa < up.custo:
        return False
    if up.desbloqueio not in state.locais_desbloqueados:
        return False
    state.caixa -= up.custo
    state.upgrades.add(key)
    return True


def venceu(state: GameState) -> bool:
    ultimo = ORDEM_LOCAIS[-1]
    return (state.local_atual == ultimo
            and state.caixa >= LOCAIS[ultimo].meta_caixa)


def faliu(state: GameState) -> bool:
    """Piso suave: so quebra sem caixa, sem estoque pronto E sem insumo pra fazer.

    Quem gastou o caixa comprando insumo fez a jogada certa -- nao pode
    perder o jogo por isso antes de ter a chance de produzir e vender.
    """
    if state.caixa >= CAIXA_MINIMO_VIVO:
        return False
    if state.inventario.total_prontos() > 0:
        return False
    return not _consegue_produzir_algo(state)


def _consegue_produzir_algo(state: GameState) -> bool:
    from ..content.flavors import sabores_disponiveis
    from .economy import pode_produzir

    return any(pode_produzir(state, f.key) > 0
               for f in sabores_disponiveis(state.locais_desbloqueados))


def tentar_socorro(state: GameState) -> bool:
    """Uma unica ajuda por partida: volta pra casa com o basico no bolso."""
    if state.socorro_usado or not faliu(state):
        return False
    state.socorro_usado = True
    state.caixa = AJUDA_RECOMECO
    state.local_atual = "casa"
    return True


def checar_fim(state: GameState) -> str | None:
    if venceu(state):
        return "vitoria"
    if faliu(state):
        if tentar_socorro(state):
            return None
        return "falencia"
    return None
