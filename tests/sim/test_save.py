"""Salvar e carregar tem que devolver o mesmo jogo."""

from dindin.persistence.save import carregar, salvar
from dindin.sim.economy import comprar
from dindin.sim.state import GameState


def test_ida_e_volta(tmp_path):
    s = GameState(seed=42, regiao="pa", dia=13, caixa=123456, reputacao=71.5,
                  local_atual="praia",
                  locais_desbloqueados=["casa", "isopor", "praia"])
    s.upgrades = {"gerador", "banner"}
    comprar(s, {"polpa_premium": 4, "saquinho": 2})
    s.inventario.prontos = {"acai": 40, "coco": 15}
    s.vendas_recentes = {"acai": 3}

    destino = tmp_path / "save.json"
    salvar(s, destino)
    voltou = carregar(destino)

    assert voltou is not None
    assert voltou.seed == s.seed
    assert voltou.regiao == "pa"
    assert voltou.dia == 13
    assert voltou.caixa == s.caixa
    assert voltou.reputacao == 71.5
    assert voltou.local_atual == "praia"
    assert voltou.locais_desbloqueados == s.locais_desbloqueados
    assert voltou.upgrades == {"gerador", "banner"}
    assert voltou.inventario.prontos == {"acai": 40, "coco": 15}
    assert voltou.inventario.total("polpa_premium") == 4
    assert voltou.vendas_recentes == {"acai": 3}


def test_arquivo_inexistente_devolve_none(tmp_path):
    assert carregar(tmp_path / "nao_existe.json") is None


def test_versao_incompativel_e_ignorada(tmp_path):
    destino = tmp_path / "save.json"
    destino.write_text('{"versao": 999}', encoding="utf-8")
    assert carregar(destino) is None
