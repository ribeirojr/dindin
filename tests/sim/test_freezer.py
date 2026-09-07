"""Capacidade, derretimento e gelo."""

from dindin.sim.freezer import (
    cobertura_do_saco,
    capacidade_dia,
    capacidade_total,
    derretimento_por_excesso,
    falta_de_gelo,
)
from dindin.sim.state import GameState


def test_dentro_da_capacidade_nao_derrete():
    s = GameState()
    s.inventario.prontos = {"coco": 50}
    assert derretimento_por_excesso(s) == {}
    assert s.inventario.total_prontos() == 50


def test_excesso_derrete_proporcionalmente():
    s = GameState(capacidade_freezer=60)
    s.inventario.prontos = {"coco": 60, "acai": 40}
    perdas = derretimento_por_excesso(s)
    assert sum(perdas.values()) == 40
    assert s.inventario.total_prontos() == 60


def test_caixa_boa_corta_o_derretimento():
    """A caixa em uso e que define quanto derrete."""
    from dindin.content.coolers import ISOPORES

    s = GameState(capacidade_freezer=60, isopor="bom", isopor_dias=10)
    s.inventario.prontos = {"coco": 100}
    perdas = derretimento_por_excesso(s)
    esperado = round(40 * ISOPORES["bom"].derretimento)
    assert sum(perdas.values()) == esperado

    sem = GameState(capacidade_freezer=60, isopor="simples", isopor_dias=10)
    sem.inventario.prontos = {"coco": 100}
    assert sum(derretimento_por_excesso(sem).values()) > esperado


def test_freezer_maior_aumenta_capacidade():
    s = GameState(capacidade_freezer=60)
    assert capacidade_total(s) == 60
    s.upgrades = {"freezer_maior"}
    assert capacidade_total(s) == 180


def test_em_casa_nao_precisa_de_gelo():
    s = GameState()
    s.inventario.prontos = {"coco": 100}
    assert falta_de_gelo(s, "casa", 0, 100) == {}


def test_gelo_insuficiente_derrete_o_descoberto():
    s = GameState()
    s.inventario.prontos = {"coco": 100}
    perdas = falta_de_gelo(s, "isopor", 1, 100)  # 1 saco cobre 50
    assert sum(perdas.values()) == 50


def test_gelo_suficiente_nao_perde_nada():
    s = GameState()
    s.inventario.prontos = {"coco": 100}
    assert falta_de_gelo(s, "isopor", 2, 100) == {}


def test_ajudante_aumenta_capacidade_do_dia():
    s = GameState(isopor="termico", isopor_dias=10)
    base = capacidade_dia(s, "praia")
    s.upgrades = {"ajudante"}
    assert capacidade_dia(s, "praia") == base + 40


def test_sem_isopor_nao_da_pra_vender_na_rua():
    s = GameState(local_atual="praia")
    assert capacidade_dia(s, "praia") == 0
    assert capacidade_dia(s, "casa") > 0, "em casa o freezer resolve"


def test_isopor_melhor_cabe_mais():
    caps = [capacidade_dia(GameState(isopor=k, isopor_dias=9), "praia")
            for k in ("simples", "bom", "termico")]
    assert caps == sorted(caps), caps


def test_calor_faz_o_saco_de_gelo_render_menos():
    """E isso que da peso a decisao: no dia quente voce vende mais E
    precisa de mais gelo, com o mesmo dinheiro."""
    from dindin.sim.freezer import cobertura_do_saco

    ameno = cobertura_do_saco(26.0)
    quente = cobertura_do_saco(32.0)
    escaldante = cobertura_do_saco(39.0)
    assert ameno > quente > escaldante
    assert ameno == 50
    assert escaldante < 35


def test_gelo_de_menos_derrete_mais_no_calor():
    s_frio = GameState()
    s_frio.inventario.prontos = {"coco": 100}
    perda_fria = falta_de_gelo(s_frio, "isopor", 2, 100, 26.0)

    s_quente = GameState()
    s_quente.inventario.prontos = {"coco": 100}
    perda_quente = falta_de_gelo(s_quente, "isopor", 2, 100, 39.0)

    assert sum(perda_fria.values()) == 0, "2 sacos cobrem 100 no frio"
    assert sum(perda_quente.values()) > 0, "no calor 2 sacos nao cobrem 100"


def test_escolha_do_gelo_muda_o_resultado():
    """Se levar 1 ou 3 sacos desse no mesmo, nao seria decisao nenhuma."""
    from dindin.sim.engine import advance_day
    from dindin.sim.state import DayPlan

    lucros = []
    for sacos in (1, 2, 3):
        s = GameState(seed=304, regiao="ce", local_atual="isopor",
                      caixa=50000, capacidade_freezer=200)
        s.inventario.prontos = {"coco": 100}
        r = advance_day(s, DayPlan({}, {"coco": 200}, "isopor", {}, gelo=sacos))
        lucros.append(r.lucro)
    assert len(set(lucros)) > 1, "a quantidade de gelo tem que mudar o lucro"
