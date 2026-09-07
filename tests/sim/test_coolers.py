"""O isopor como equipamento: compra unica que dura varios dias e acaba."""

import pytest

from dindin.content.coolers import ISOPORES, ORDEM_ISOPORES
from dindin.sim import progression
from dindin.sim.engine import advance_day
from dindin.sim.freezer import capacidade_dia, fator_derretimento, isopor_vivo
from dindin.sim.state import DayPlan, GameState


def test_isopor_gasta_um_dia_por_dia_na_rua():
    s = GameState(seed=1, regiao="ce", local_atual="isopor", caixa=50000,
                  isopor="simples", isopor_dias=3)
    s.inventario.prontos = {"coco": 40}
    advance_day(s, DayPlan({}, {"coco": 200}, "isopor", {}, gelo=1))
    assert s.isopor_dias == 2


def test_isopor_nao_gasta_em_casa():
    s = GameState(seed=1, regiao="ce", local_atual="casa",
                  isopor="simples", isopor_dias=5)
    s.inventario.prontos = {"coco": 30}
    advance_day(s, DayPlan({}, {"coco": 200}, "casa", {}))
    assert s.isopor_dias == 5, "em casa o freezer resolve, a caixa nao gasta"


def test_isopor_racha_e_avisa():
    s = GameState(seed=1, regiao="pa", local_atual="isopor", caixa=50000,
                  isopor="simples", isopor_dias=1)
    s.inventario.prontos = {"coco": 40}
    r = advance_day(s, DayPlan({}, {"coco": 200}, "isopor", {}, gelo=1))
    assert s.isopor is None
    assert not isopor_vivo(s)
    assert any(e.key == "isopor_acabou" for e in r.eventos)


def test_sem_isopor_nao_vende_na_rua():
    s = GameState(local_atual="praia")
    assert capacidade_dia(s, "praia") == 0


def test_caixa_melhor_cabe_mais_e_derrete_menos():
    caps, derr = [], []
    for k in ORDEM_ISOPORES:
        s = GameState(isopor=k, isopor_dias=9)
        caps.append(capacidade_dia(s, "praia"))
        derr.append(fator_derretimento(s))
    assert caps == sorted(caps), "caixa melhor tem que caber mais"
    assert derr == sorted(derr, reverse=True), "caixa melhor tem que derreter menos"


def test_comprar_isopor_cobra_e_reseta_a_vida():
    s = GameState(caixa=20000)
    assert progression.comprar_isopor(s, "bom")
    c = ISOPORES["bom"]
    assert s.caixa == 20000 - c.custo
    assert s.isopor == "bom" and s.isopor_dias == c.dias


def test_sem_dinheiro_nao_compra():
    s = GameState(caixa=100)
    assert not progression.comprar_isopor(s, "termico")
    assert s.isopor is None


def test_avisa_quando_esta_acabando():
    s = GameState(local_atual="isopor", isopor="simples", isopor_dias=2)
    assert progression.isopor_acabando(s)
    s.isopor_dias = 10
    assert not progression.isopor_acabando(s)


def test_precisa_de_isopor_so_fora_de_casa():
    assert not progression.precisa_de_isopor(GameState(local_atual="casa"))
    assert progression.precisa_de_isopor(GameState(local_atual="praia"))


@pytest.mark.parametrize("key", ORDEM_ISOPORES)
def test_caixa_mais_cara_sai_mais_barato_por_unidade_de_vida(key):
    """A caixa boa custa mais mas nao pode ser um roubo por dia."""
    c = ISOPORES[key]
    assert c.custo_por_dia < 400, f"{key} sai caro demais por dia"


def test_caixa_nunca_fica_negativo():
    """Sem dinheiro pro ponto o jogador quebra, nao endivida."""
    s = GameState(seed=1, regiao="sp", local_atual="praia", caixa=1000,
                  isopor="simples", isopor_dias=5)
    for _ in range(4):
        advance_day(s, DayPlan({}, {}, "praia", {}))
        assert s.caixa >= 0
