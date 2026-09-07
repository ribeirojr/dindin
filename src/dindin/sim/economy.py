"""Compras na feira, producao e contabilidade."""

from collections.abc import Mapping

from ..content.flavors import SABORES
from ..content.ingredients import INSUMOS
from ..content.regions import REGIOES
from .state import GameState
from .types import Centavos


def custo_compras(compras: Mapping[str, int], regiao_key: str) -> Centavos:
    mod = REGIOES[regiao_key].custo_insumo_mod
    return sum(INSUMOS[k].preco_unitario(q, mod) * q
               for k, q in compras.items() if q > 0)


def comprar(state: GameState, compras: Mapping[str, int]) -> Centavos:
    """Debita o caixa e guarda os lotes. Retorna o custo. Nao valida saldo."""
    total = custo_compras(compras, state.regiao)
    for key, qtd in compras.items():
        if qtd <= 0:
            continue
        ing = INSUMOS[key]
        validade = None if ing.validade_dias is None else state.dia + ing.validade_dias
        state.inventario.adicionar(key, float(qtd), validade)
    state.caixa -= total
    return total


def custo_unitario(flavor_key: str, regiao_key: str) -> Centavos:
    """Custo de produzir uma unidade, a preco de balcao (sem desconto por volume)."""
    mod = REGIOES[regiao_key].custo_insumo_mod
    sabor = SABORES[flavor_key]
    total = sum(INSUMOS[k].preco_base * mod * (q / 10.0)
                for k, q in sabor.receita.items())
    return round(total)


def pode_produzir(state: GameState, flavor_key: str) -> int:
    """Quantas unidades o estoque de insumos permite fazer."""
    sabor = SABORES[flavor_key]
    limite = 10**9
    for ing_key, por_dez in sabor.receita.items():
        if por_dez <= 0:
            continue
        disponivel = state.inventario.total(ing_key)
        limite = min(limite, int(disponivel * 10.0 / por_dez + 1e-9))
    return max(0, limite)


def pode_produzir_com_reserva(
    state: GameState, flavor_key: str, reservado: Mapping[str, int] | None = None
) -> int:
    """Quanto da pra fazer deste sabor descontando o que outros ja reservaram.

    Insumo e compartilhado: coco e maracuja saem da MESMA polpa. Sem isso a
    tela mostra que da pra fazer 38 de maracuja mesmo depois de voce ter
    comprometido a polpa toda com o coco.
    """
    sabor = SABORES[flavor_key]
    limite = 10**9
    for ing_key, por_dez in sabor.receita.items():
        if por_dez <= 0:
            continue
        gasto = 0.0
        for outro_key, qtd in (reservado or {}).items():
            if outro_key == flavor_key or not qtd:
                continue
            gasto += SABORES[outro_key].consumo(int(qtd)).get(ing_key, 0.0)
        sobra = max(0.0, state.inventario.total(ing_key) - gasto)
        limite = min(limite, int(sobra * 10.0 / por_dez + 1e-9))
    return max(0, limite)


def produzir(state: GameState, producao: Mapping[str, int]) -> dict[str, int]:
    """Consome insumos e gera unidades prontas. Retorna o que realmente saiu."""
    feito: dict[str, int] = {}
    for flavor_key, qtd in producao.items():
        if qtd <= 0:
            continue
        real = min(qtd, pode_produzir(state, flavor_key))
        if real <= 0:
            continue
        for ing_key, precisa in SABORES[flavor_key].consumo(real).items():
            state.inventario.consumir(ing_key, precisa)
        state.inventario.prontos[flavor_key] = (
            state.inventario.prontos.get(flavor_key, 0) + real
        )
        feito[flavor_key] = real
    return feito
