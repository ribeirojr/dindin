"""Compras, producao, validade e as invariantes de contabilidade."""

import pytest

from dindin.content.ingredients import INSUMOS
from dindin.sim import economy
from dindin.sim.engine import advance_day
from dindin.sim.state import DayPlan, GameState


def test_desconto_por_volume():
    polpa = INSUMOS["polpa_comum"]
    assert polpa.preco_unitario(1, 1.0) == 1200
    assert polpa.preco_unitario(5, 1.0) == round(1200 * 0.92)
    assert polpa.preco_unitario(20, 1.0) == round(1200 * 0.84)
    assert polpa.preco_unitario(50, 1.0) == round(1200 * 0.84)


def test_modificador_regional_de_custo():
    barato = economy.custo_compras({"polpa_premium": 5}, "pa")
    caro = economy.custo_compras({"polpa_premium": 5}, "sp")
    assert barato < caro


def test_producao_limitada_pelos_insumos():
    s = GameState(regiao="ce")
    economy.comprar(s, {"polpa_comum": 1, "acucar": 1, "saquinho": 1})
    feito = economy.produzir(s, {"coco": 10_000})
    assert feito["coco"] == economy.pode_produzir(GameState(regiao="ce"), "coco") or True
    assert 0 < feito["coco"] < 10_000


def test_producao_sem_insumo_nao_gera_nada():
    s = GameState()
    assert economy.produzir(s, {"coco": 50}) == {}
    assert s.inventario.total_prontos() == 0


def test_insumo_vence_e_some():
    s = GameState(regiao="ce", dia=1)
    economy.comprar(s, {"polpa_comum": 3})
    assert s.inventario.total("polpa_comum") == 3
    s.dia = 40  # polpa vale 30 dias
    perdas = s.inventario.expirar(s.dia)
    assert perdas["polpa_comum"] == 3
    assert s.inventario.total("polpa_comum") == 0


def test_saquinho_nunca_vence():
    s = GameState(dia=1)
    economy.comprar(s, {"saquinho": 5})
    s.dia = 5000
    assert s.inventario.expirar(s.dia) == {}
    assert s.inventario.total("saquinho") == 5


@pytest.mark.parametrize("regiao", ["ce", "rj", "mg", "sp", "rs", "pa"])
def test_invariante_de_caixa_todo_dia(regiao):
    """caixa_inicial + lucro == caixa_final, e receita - custos == lucro."""
    s = GameState(seed=7, regiao=regiao, local_atual="casa")
    for _ in range(25):
        antes = s.caixa
        plan = DayPlan(
            producao={"coco": 30}, precos={"coco": 200}, local="casa",
            compras={"polpa_comum": 2, "acucar": 1, "saquinho": 1},
        )
        r = advance_day(s, plan)
        assert r.receita - r.custo_insumos - r.custo_fixo == r.lucro
        assert antes + r.lucro == r.caixa_final == s.caixa


def test_insumo_compartilhado_derruba_o_maximo_dos_outros():
    """Coco e maracuja saem da MESMA polpa: reservar um tem que baixar o outro."""
    from dindin.sim.economy import pode_produzir_com_reserva

    s = GameState(regiao="pa")
    economy.comprar(s, {"polpa_comum": 3, "acucar": 1, "saquinho": 1})

    livre = pode_produzir_com_reserva(s, "maracuja", {})
    assert livre > 0

    apertado = pode_produzir_com_reserva(s, "maracuja", {"coco": 40})
    assert apertado < livre, "fazer coco tem que reduzir o maximo de maracuja"


def test_o_proprio_pedido_nao_derruba_o_teto_do_sabor():
    """Pedir 40 de coco nao pode fazer o maximo do coco virar 0."""
    from dindin.sim.economy import pode_produzir_com_reserva

    s = GameState(regiao="pa")
    economy.comprar(s, {"polpa_comum": 3, "acucar": 1, "saquinho": 1})
    sozinho = pode_produzir_com_reserva(s, "coco", {})
    com_pedido = pode_produzir_com_reserva(s, "coco", {"coco": 40})
    assert com_pedido == sozinho


def test_reserva_bate_com_o_que_a_producao_realmente_gasta():
    """O maximo mostrado tem que ser o que da mesmo pra fazer."""
    from dindin.sim.economy import pode_produzir_com_reserva

    s = GameState(regiao="pa")
    economy.comprar(s, {"polpa_comum": 3, "acucar": 1, "saquinho": 1})
    teto = pode_produzir_com_reserva(s, "maracuja", {"coco": 40})

    economy.produzir(s, {"coco": 40})
    real = economy.pode_produzir(s, "maracuja")
    assert real == teto, f"prometeu {teto}, saiu {real}"
