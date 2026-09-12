"""Conquistas da campanha: vencer uma regiao fica registrado entre partidas."""

from dindin.content.regions import ORDEM_REGIOES
from dindin.sim import campaign


def test_comeca_sem_nenhuma_conquista():
    assert campaign.quantas(None) == 0
    assert campaign.quantas(set()) == 0
    assert not campaign.zerou_tudo(set())


def test_registrar_vitoria_marca_a_regiao():
    c = campaign.registrar_vitoria(set(), "ce")
    assert campaign.venceu_regiao(c, "ce")
    assert not campaign.venceu_regiao(c, "rj")


def test_registrar_nao_muda_o_conjunto_original():
    """Funcao pura: quem chamou continua com o conjunto que tinha."""
    antes = {"ce"}
    depois = campaign.registrar_vitoria(antes, "rj")
    assert antes == {"ce"}
    assert depois == {"ce", "rj"}


def test_vencer_a_mesma_regiao_duas_vezes_nao_duplica():
    c = campaign.registrar_vitoria({"ce"}, "ce")
    assert c == {"ce"}
    assert campaign.quantas(c) == 1


def test_chave_desconhecida_e_descartada():
    """Save antigo com regiao que nao existe mais nao pode inflar o placar."""
    assert campaign.normalizar({"ce", "zz", "atlantida"}) == {"ce"}
    assert campaign.registrar_vitoria(set(), "zz") == set()


def test_pendentes_segue_a_ordem_do_jogo():
    c = {ORDEM_REGIOES[0], ORDEM_REGIOES[2]}
    faltam = campaign.pendentes(c)
    assert faltam == [k for k in ORDEM_REGIOES if k not in c]
    assert ORDEM_REGIOES[1] in faltam


def test_zerar_todas_as_regioes():
    c = set()
    for k in ORDEM_REGIOES:
        c = campaign.registrar_vitoria(c, k)
    assert campaign.zerou_tudo(c)
    assert campaign.quantas(c) == campaign.total()
    assert campaign.pendentes(c) == []
