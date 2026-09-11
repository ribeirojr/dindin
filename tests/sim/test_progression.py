"""Metas, desbloqueios, upgrades e fim de jogo."""

from dindin.content.locations import LOCAIS
from dindin.sim import progression
from dindin.sim.state import GameState


def test_melhor_local_e_o_mais_avancado_ja_liberado():
    s = GameState(local_atual="casa",
                  locais_desbloqueados=["casa", "isopor", "praia"])
    assert progression.melhor_local(s) == "praia"


def test_melhor_local_no_comeco_e_casa():
    assert progression.melhor_local(GameState()) == "casa"


def test_socorro_nao_tira_o_ponto_do_jogador():
    """Depois do socorro ele volta pra casa, mas o ponto continua liberado --
    e a volta (via melhor_local) nao pode cobrar entrada de novo."""
    s = GameState(local_atual="praia", caixa=0,
                  locais_desbloqueados=["casa", "isopor", "praia"])
    assert progression.tentar_socorro(s)
    assert s.local_atual == "casa"
    assert "praia" in s.locais_desbloqueados
    assert progression.melhor_local(s) == "praia"


def test_nao_desbloqueia_antes_da_meta():
    s = GameState(local_atual="casa", caixa=LOCAIS["casa"].meta_caixa - 1)
    assert progression.pode_desbloquear(s) is None


def test_desbloqueia_exatamente_na_meta():
    s = GameState(local_atual="casa", caixa=LOCAIS["casa"].meta_caixa)
    assert progression.pode_desbloquear(s) == "isopor"


def test_mudar_de_ponto_cobra_a_entrada():
    s = GameState(local_atual="casa", caixa=30000)
    assert progression.desbloquear(s, "isopor")
    assert s.caixa == 30000 - LOCAIS["isopor"].custo_entrada
    assert s.local_atual == "isopor"
    assert "isopor" in s.locais_desbloqueados


def test_sem_caixa_nao_muda_de_ponto():
    s = GameState(local_atual="casa", caixa=100)
    assert not progression.desbloquear(s, "praia")
    assert s.local_atual == "casa"


def test_upgrade_exige_ponto_desbloqueado():
    s = GameState(caixa=999999, locais_desbloqueados=["casa"])
    assert not progression.comprar_upgrade(s, "gerador")  # exige praia
    s.locais_desbloqueados.append("praia")
    assert progression.comprar_upgrade(s, "gerador")
    assert "gerador" in s.upgrades


def test_nao_compra_upgrade_repetido():
    s = GameState(caixa=999999, locais_desbloqueados=["casa", "praia"])
    assert progression.comprar_upgrade(s, "gerador")
    assert not progression.comprar_upgrade(s, "gerador")


def test_vitoria_no_ultimo_capitulo():
    s = GameState(local_atual="carrinho", caixa=LOCAIS["carrinho"].meta_caixa)
    assert progression.venceu(s)
    assert progression.checar_fim(s) == "vitoria"


def test_nao_quebra_quem_gastou_o_caixa_em_insumo():
    """Gastar o caixa comprando insumo e a jogada certa: nao pode custar o jogo."""
    s = GameState(caixa=12)
    s.inventario.adicionar("polpa_comum", 3.0, 30)
    s.inventario.adicionar("acucar", 1.0, 365)
    s.inventario.adicionar("saquinho", 1.0, None)
    assert not progression.faliu(s)


def test_falencia_so_sem_caixa_e_sem_estoque():
    s = GameState(caixa=100)
    s.inventario.prontos = {"coco": 20}
    assert not progression.faliu(s)  # ainda da pra vender e virar o jogo
    s.inventario.prontos = {}
    s.inventario.ingredientes.clear()
    assert progression.faliu(s)

    # Na primeira vez o jogo socorre em vez de encerrar.
    assert progression.checar_fim(s) is None
    assert s.socorro_usado and s.caixa > 0 and s.local_atual == "casa"


def test_socorro_acontece_uma_vez_so():
    """Zerar tudo de novo depois do socorro acaba o jogo pra valer."""
    s = GameState(caixa=100)
    assert progression.checar_fim(s) is None      # socorro
    s.caixa = 0
    s.inventario.prontos = {}
    s.inventario.ingredientes.clear()
    assert progression.checar_fim(s) == "falencia"


def test_socorro_devolve_o_jogador_pra_casa():
    s = GameState(caixa=0, local_atual="praia")
    progression.checar_fim(s)
    assert s.local_atual == "casa", "sem isopor nao da pra ficar na rua"
