"""Cadencia de aprendizado: o jogo abre pouca coisa e vai crescendo."""

import pytest

from dindin.content.flavors import SABORES, sabores_disponiveis
from dindin.content.ingredients import INSUMOS, insumos_disponiveis
from dindin.content.locations import ORDEM_LOCAIS

CAMINHO = ["casa", "isopor", "praia", "escola", "carrinho"]


def test_dia_1_e_simples():
    """Tres sabores e quatro insumos: da pra entender tudo de primeira."""
    assert len(sabores_disponiveis(["casa"])) == 3
    assert len(insumos_disponiveis(["casa"])) == 4


def test_nada_de_gourmet_no_comeco():
    """Leite condensado e Nutella so quando existir sabor que use."""
    keys = {i.key for i in insumos_disponiveis(["casa"])}
    assert "leite_cond" not in keys
    assert "creme_avela" not in keys
    assert "polpa_premium" not in keys


def test_opcoes_so_crescem():
    acc, sab, ins = [], [], []
    for local in CAMINHO:
        acc.append(local)
        sab.append(len(sabores_disponiveis(acc)))
        ins.append(len(insumos_disponiveis(acc)))
    assert sab == sorted(sab), sab
    assert ins == sorted(ins), ins
    assert sab[0] < sab[-1] and ins[0] < ins[-1]


def test_no_fim_tudo_esta_liberado():
    assert len(sabores_disponiveis(CAMINHO)) == len(SABORES)
    liberados = {i.key for i in insumos_disponiveis(CAMINHO)}
    assert liberados == {k for k in INSUMOS if k != "gelo"}


def test_todo_sabor_tem_seus_insumos_liberados_junto():
    """Nao adianta abrir um sabor se o insumo dele ainda esta escondido."""
    acc = []
    for local in CAMINHO:
        acc.append(local)
        disponiveis = {i.key for i in insumos_disponiveis(acc)}
        for f in sabores_disponiveis(acc):
            faltando = set(f.receita) - disponiveis
            assert not faltando, f"{f.key} em {local} precisa de {faltando}"


@pytest.mark.parametrize("local", ORDEM_LOCAIS)
def test_todo_ponto_tem_desenho(local):
    from dindin.ui.widgets.scene import CENAS

    assert local in CENAS
    assert CENAS[local]["plano"].strip()
    assert CENAS[local]["venda"].strip()


def test_cena_de_venda_tem_gente():
    """A cena do dia rolando precisa mostrar cliente, senao nao muda nada."""
    from dindin.ui.widgets.scene import CENAS

    for local, cenas in CENAS.items():
        assert "o/" in cenas["venda"] or '"' in cenas["venda"], local
