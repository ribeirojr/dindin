"""Cobertura de traducao: chaves erradas e placeholders quebrados sao crash em jogo."""

import re

import pytest

from dindin.i18n import REGIOES_I18N, Translator, carregar_override, money
from dindin.i18n.base_ptbr import BASE
from dindin.sim.types import BarkTag

PLACEHOLDER = re.compile(r"\{(\w+)\}")


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_toda_chave_de_override_existe_na_base(regiao):
    """Pega erro de digitacao: um override que nao sobrescreve nada."""
    extras = set(carregar_override(regiao)) - set(BASE)
    assert not extras, f"{regiao} tem chaves que nao existem na base: {extras}"


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_placeholders_batem_com_a_base(regiao):
    """Se a base usa {perdidos}, o override tem que usar tambem, senao quebra."""
    over = carregar_override(regiao)
    for key, texto in over.items():
        esperados = set(PLACEHOLDER.findall(BASE[key]))
        achados = set(PLACEHOLDER.findall(texto))
        assert achados <= esperados, f"{regiao}.{key}: placeholder a mais {achados - esperados}"


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_nenhuma_chave_da_base_fica_faltando(regiao):
    t = Translator(regiao)
    for key in BASE:
        assert not t.t(key).startswith("⟨missing:")


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_cada_regiao_tem_nome_proprio_do_produto(regiao):
    """O ponto do jogo: o produto muda de nome em cada estado."""
    assert Translator(regiao).produto != BASE["produto.sing"]


def test_produtos_sao_todos_diferentes():
    nomes = {Translator(r).produto for r in REGIOES_I18N}
    assert nomes == {"dindin", "sacolé", "laranjinha", "geladinho",
                     "gelinho", "chup-chup", "geladim"}


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_toda_regiao_responde_todos_os_barks(regiao):
    from random import Random

    t = Translator(regiao)
    for tag in BarkTag:
        assert t.bark(tag, Random(0)), f"{regiao} sem bark para {tag}"


def test_chave_inexistente_fica_visivel():
    assert Translator("ce").t("xxx.yyy") == "⟨missing:xxx.yyy⟩"


@pytest.mark.parametrize("valor,esperado", [
    (0, "R$ 0,00"), (80, "R$ 0,80"), (12345, "R$ 123,45"),
    (645000, "R$ 6.450,00"), (-1250, "-R$ 12,50"),
])
def test_formato_de_dinheiro_brasileiro(valor, esperado):
    assert money(valor) == esperado


@pytest.mark.parametrize("modulo", ["base_ptbr", "base_en"])
def test_nenhuma_chave_repetida_na_base(modulo):
    """Chave repetida no dict literal e invisivel: a segunda apaga a primeira
    em silencio e a traducao que o autor escreveu nunca aparece em jogo.
    Foi o que aconteceu com ui.escolha_regiao."""
    import ast
    import collections
    import pathlib

    caminho = pathlib.Path(__file__).parents[2] / "src" / "dindin" / "i18n" / f"{modulo}.py"
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    repetidas: list[str] = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Dict):
            chaves = [k.value for k in no.keys
                      if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            repetidas += [k for k, n in collections.Counter(chaves).items() if n > 1]
    assert not repetidas, f"{modulo} tem chaves repetidas: {sorted(set(repetidas))}"
