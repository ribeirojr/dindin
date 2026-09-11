"""Ingles: a interface traduz, o sotaque fica.

Regra do desenho: nome do produto (dindin, sacole...) e giria de rua sao
nomes proprios/fala diegetica -- continuam em portugues em qualquer idioma.
"""

import re
from random import Random

import pytest

from dindin.i18n import REGIOES_I18N, Translator
from dindin.i18n.base_en import BASE_EN, OVERRIDES_EN
from dindin.i18n.base_ptbr import BASE
from dindin.sim.types import BarkTag

PLACEHOLDER = re.compile(r"\{(\w+)\}")


def test_base_en_cobre_exatamente_as_chaves_da_base():
    """Chave sem traducao vazaria portugues no meio do ingles (ou vice-versa)."""
    faltam = set(BASE) - set(BASE_EN)
    sobram = set(BASE_EN) - set(BASE)
    assert not faltam, f"sem traducao: {sorted(faltam)}"
    assert not sobram, f"chaves orfas no ingles: {sorted(sobram)}"


def test_placeholders_iguais_nas_duas_linguas():
    """Se o pt usa {perdidos}, o ingles tem que usar tambem, senao quebra."""
    for key, texto in BASE_EN.items():
        esperados = set(PLACEHOLDER.findall(BASE[key]))
        achados = set(PLACEHOLDER.findall(texto))
        assert achados == esperados, f"{key}: {achados} != {esperados}"


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_produto_regional_e_o_mesmo_nas_duas_linguas(regiao):
    pt = Translator(regiao, "pt")
    en = Translator(regiao, "en")
    assert en.produto == pt.produto, "nome proprio nao se traduz"
    assert en.t("produto.plur") == pt.t("produto.plur")


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_interface_sai_em_ingles(regiao):
    en = Translator(regiao, "en")
    assert en.t("ui.novo_jogo") == "New game"
    assert en.t("feira.titulo") == "Market"
    assert en.t("local.praia") == "Beach"
    assert not en.t("rel.sellout", perdidos=3).startswith("⟨missing:")


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_nenhuma_chave_falta_em_ingles(regiao):
    en = Translator(regiao, "en")
    for key in BASE:
        assert not en.t(key).startswith("⟨missing:"), key


def test_idioma_desconhecido_cai_no_portugues():
    assert Translator("ce", "xx").lang == "pt"
    assert Translator("ce", "xx").t("ui.novo_jogo") == "Jogo novo"


@pytest.mark.parametrize("regiao", REGIOES_I18N)
def test_barks_existem_em_ingles(regiao):
    en = Translator(regiao, "en")
    for tag in BarkTag:
        fala = en.bark(tag, Random(0))
        assert fala, f"{regiao}/{tag.value} sem fala em ingles"


def test_bark_em_ingles_mantem_o_sotaque():
    """O sotaque regional e o charme: 'ma broca' sobrevive a traducao."""
    en = Translator("ce", "en")
    falas = {en.bark(BarkTag.PRECO_ALTO, Random(i)) for i in range(20)}
    assert any("ma broca" in f or "Vixe" in f for f in falas)


def test_toda_regiao_tem_override_de_produto_em_ingles():
    assert set(OVERRIDES_EN) == set(REGIOES_I18N)
    for regiao, over in OVERRIDES_EN.items():
        assert "produto.sing" in over and "produto.plur" in over


def test_nomes_de_conteudo_viram_chave_nas_duas_linguas():
    """Sabor e insumo precisam de nome traduzivel na feira e na cozinha."""
    from dindin.content.flavors import SABORES
    from dindin.content.ingredients import INSUMOS

    pt = Translator("ce", "pt")
    en = Translator("ce", "en")
    for k, f in SABORES.items():
        assert pt.t(f"sabor.{k}") == f.nome, "pt vem do content, sem duplicar"
        assert not en.t(f"sabor.{k}").startswith("⟨missing:")
    for k in INSUMOS:
        assert not en.t(f"insumo.{k}").startswith("⟨missing:")
        assert not en.t(f"insumo.unidade.{k}").startswith("⟨missing:")
