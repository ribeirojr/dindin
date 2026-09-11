"""A ponte JSON: o que atravessa pro navegador tem que ser JSON puro."""

import json

import pytest

from dindin import bridge


def test_estado_novo_e_json_puro():
    st = bridge.novo_jogo("pa", 77)
    assert json.loads(json.dumps(st)) == st
    assert st["regiao"] == "pa"
    assert st["dia"] == 1
    assert st["caixa"] == 8000


@pytest.mark.parametrize("regiao", ["ce", "rj", "mg", "sp", "rs", "pa"])
def test_catalogo_serializa_em_json(regiao):
    cat = bridge.catalogo(regiao)
    assert json.loads(json.dumps(cat, ensure_ascii=False)) == cat
    assert len(cat["textos"]) > 100
    assert cat["sabores"] and cat["insumos"] and cat["locais"]
    assert not any(v.startswith("⟨missing:") for v in cat["textos"].values())


def test_cada_regiao_tem_produto_proprio_na_ponte():
    produtos = {r["key"]: r["produto"] for r in bridge.regioes()}
    assert produtos == {
        "ce": "dindin", "rj": "sacolé", "mg": "laranjinha",
        "sp": "geladinho", "rs": "gelinho", "pa": "chup-chup",
    }


def test_dia_inteiro_atravessa_json():
    st = bridge.novo_jogo("pa", 77)
    plano = {
        "compras": {"polpa_comum": 3, "acucar": 1, "saquinho": 1},
        "producao": {"coco": 40},
        "precos": {"coco": 190},
        "gelo": 0,
    }
    out = bridge.jogar_dia(st, plano)
    assert json.loads(json.dumps(out, ensure_ascii=False)) == out

    r = out["resultado"]
    assert r["dia"] == 1
    assert r["receita"] - r["custo_insumos"] - r["custo_fixo"] == r["lucro"]
    assert out["estado"]["dia"] == 2


def test_eventos_atravessam_como_chave_e_nao_texto():
    """O sim nao pode mandar texto pronto: quem traduz e o front."""
    st = bridge.novo_jogo("pa", 5)
    out = bridge.jogar_dia(st, {"producao": {}, "precos": {}, "compras": {}})
    for e in out["resultado"]["eventos"]:
        assert e["text_key"].startswith("evento.")
        assert "key" in e


def test_curva_de_preco_acha_o_melhor_lucro():
    st = bridge.novo_jogo("pa", 77)
    c = bridge.curva_de_preco(st, "coco")
    assert json.loads(json.dumps(c)) == c
    assert c["melhor_preco"] > c["custo"], "vender abaixo do custo nunca e o melhor"
    melhor = max(c["pontos"], key=lambda p: p["lucro_rel"])
    assert melhor["preco"] == c["melhor_preco"]


def test_curva_cai_quando_o_preco_sobe():
    st = bridge.novo_jogo("ce", 1)
    pontos = bridge.curva_de_preco(st, "coco")["pontos"]
    respostas = [p["resposta"] for p in pontos]
    assert respostas == sorted(respostas, reverse=True)


def test_estado_sobrevive_ida_e_volta():
    st = bridge.novo_jogo("rs", 3)
    st2 = bridge.estado_para_json(bridge.estado_de_json(st))
    for campo in ("seed", "regiao", "dia", "caixa", "local_atual"):
        assert st2[campo] == st[campo]


def test_nenhum_enum_vaza_pra_ponte():
    """Enum tem que virar string, senao JSON.stringify quebra no JS."""
    st = bridge.novo_jogo("pa", 9)
    out = bridge.jogar_dia(st, {"producao": {}, "precos": {}, "compras": {}})
    clima = out["resultado"]["clima"]
    assert isinstance(clima["kind"], str)


def test_gelo_nao_aparece_na_feira():
    """O jogo compra gelo sozinho conforme o ponto. Se ele tambem estivesse
    a venda na feira, o jogador pagaria duas vezes pelo mesmo saco."""
    for regiao in ("ce", "pa"):
        keys = [i["key"] for i in bridge.catalogo(regiao)["insumos"]]
        assert "gelo" not in keys


def test_isopor_atravessa_a_ponte():
    st = bridge.novo_jogo("pa", 77)
    st["local_atual"] = "isopor"
    info = bridge.isopores(st)
    assert json.loads(json.dumps(info, ensure_ascii=False)) == info
    assert info["precisa"] is True
    assert len(info["opcoes"]) == 3
    assert all(o["custo_por_dia"] > 0 for o in info["opcoes"])


def test_comprar_isopor_pela_ponte():
    st = bridge.novo_jogo("pa", 77)
    out = bridge.comprar_isopor(st, "simples")
    assert out["ok"]
    assert out["estado"]["isopor"] == "simples"
    assert out["estado"]["isopor_dias"] == 14
    assert out["estado"]["caixa"] < st["caixa"]


def test_carrinho_entra_na_conta_de_quanto_da_pra_fazer():
    """Bug da web: 'Da pra fazer' ficava congelado em 0 porque a conta
    era feita antes de o jogador por as coisas no carrinho."""
    st = bridge.novo_jogo("pa", 1)
    antes = {s["key"]: s["pode_produzir"] for s in bridge.sabores_do_jogador(st)}
    assert antes["coco"] == 0

    carrinho = {"polpa_comum": 3, "acucar": 1, "saquinho": 1}
    depois = {s["key"]: s["pode_produzir"]
              for s in bridge.sabores_do_jogador(st, carrinho)}
    assert depois["coco"] > 0, "comprar no carrinho tem que liberar producao"


def test_sabores_dizem_a_receita_e_o_que_falta():
    st = bridge.novo_jogo("pa", 1)
    coco = next(s for s in bridge.sabores_do_jogador(st) if s["key"] == "coco")
    assert coco["receita"], "precisa da receita pro tooltip"
    assert {"key", "nome", "unidade", "por_dez", "tem"} <= set(coco["receita"][0])
    assert coco["faltando"], "sem insumo nenhum, tem que listar o que falta"

    completo = next(s for s in bridge.sabores_do_jogador(
        st, {"polpa_comum": 3, "acucar": 1, "saquinho": 1}) if s["key"] == "coco")
    assert completo["faltando"] == []


def test_carrinho_nao_altera_o_estado_de_verdade():
    """A previa nao pode gastar insumo que o jogador ainda nao comprou."""
    st = bridge.novo_jogo("pa", 1)
    bridge.sabores_do_jogador(st, {"polpa_comum": 99})
    assert st["inventario"]["ingredientes"] == {}


def test_producao_pendente_reduz_o_maximo_dos_outros_sabores():
    """Bug: 'Da pra fazer' do maracuja nao caia ao reservar a polpa no coco."""
    st = bridge.novo_jogo("pa", 1)
    carrinho = {"polpa_comum": 3, "acucar": 1, "saquinho": 1}

    livre = {s["key"]: s["pode_produzir"]
             for s in bridge.sabores_do_jogador(st, carrinho)}
    apertado = {s["key"]: s["pode_produzir"]
                for s in bridge.sabores_do_jogador(st, carrinho, {"coco": 40})}

    assert apertado["maracuja"] < livre["maracuja"]
    assert apertado["limao"] < livre["limao"]
    assert apertado["coco"] == livre["coco"], "o proprio pedido nao baixa o teto"


def test_socorro_usado_sobrevive_ida_e_volta():
    """Bug: o campo se perdia no JSON e o socorro de falencia renascia todo
    dia -- no navegador era impossivel perder o jogo."""
    st = bridge.novo_jogo("ce", 1)
    assert st["socorro_usado"] is False
    st["socorro_usado"] = True
    assert bridge.estado_para_json(bridge.estado_de_json(st))["socorro_usado"] is True


def test_segunda_falencia_encerra_o_jogo_na_ponte():
    st = bridge.novo_jogo("ce", 1)
    st["caixa"] = 0
    st["socorro_usado"] = True
    out = bridge.jogar_dia(st, {"producao": {}, "precos": {}, "compras": {}})
    assert out["estado"]["encerrado"] == "falencia"


def test_validade_dos_insumos_sobrevive_ida_e_volta():
    """Bug: a volta do JSON zerava a validade dos lotes e insumo perecivel
    nunca vencia no navegador."""
    from dindin.sim.economy import comprar

    state = bridge.estado_de_json(bridge.novo_jogo("ce", 1))
    comprar(state, {"polpa_comum": 2})   # validade de 30 dias
    d = bridge.estado_para_json(state)

    voltou = bridge.estado_de_json(d)
    lotes = voltou.inventario.ingredientes["polpa_comum"]
    assert all(l.dia_validade == 31 for l in lotes)

    # E vencendo de verdade: no dia 40 a polpa some.
    perdas = voltou.inventario.expirar(40)
    assert perdas.get("polpa_comum", 0) == 2


def test_capacidade_base_do_freezer_sobrevive_ida_e_volta():
    st = bridge.novo_jogo("ce", 1)
    assert st["capacidade_freezer_base"] == 60
    st["upgrades"] = ["freezer_maior"]
    st2 = bridge.estado_para_json(bridge.estado_de_json(st))
    assert st2["capacidade_freezer_base"] == 60, "base nao inclui o upgrade"
    assert st2["capacidade_freezer"] == 180, "total inclui o upgrade"


def test_catalogo_traz_as_falas_regionais():
    """A web usava falas pt-BR neutras; o catalogo agora leva as da regiao."""
    from dindin.sim.types import BarkTag

    ce = bridge.catalogo("ce")["barks"]
    pa = bridge.catalogo("pa")["barks"]
    assert any("dindin" in f for f in ce["compra_simples"])
    assert any("maninho" in f for f in pa["compra_simples"])
    for tag in BarkTag:
        assert ce[tag.value], f"ce sem falas para {tag.value}"


def test_gelo_nao_conta_o_que_nem_cabe_no_isopor():
    """Sugerir gelo pra estoque que nao vai pro ponto era dinheiro jogado fora."""
    st = bridge.novo_jogo("ce", 1)
    st["local_atual"] = "isopor"
    st["locais_desbloqueados"] = ["casa", "isopor"]
    st["isopor"] = "simples"        # cabe 100
    st["isopor_dias"] = 10
    info = bridge.info_do_gelo(st, 250)
    assert info["unidades"] == 100
    assert info["sugestao"] <= -(-100 // 20), "sugestao dimensionada pro que cabe"


def test_dia_comeca_no_melhor_ponto_ja_liberado():
    """Depois do socorro o jogador volta pra casa -- mas o ponto continua
    dele: o dia seguinte tem que voltar pra la sem pagar entrada de novo."""
    st = bridge.novo_jogo("ce", 1)
    st["local_atual"] = "casa"
    st["locais_desbloqueados"] = ["casa", "isopor"]
    st["isopor"] = "simples"
    st["isopor_dias"] = 10
    caixa_antes = st["caixa"]
    out = bridge.jogar_dia(st, {"producao": {}, "precos": {}, "compras": {}})
    assert out["resultado"]["local"] == "isopor"
    # Voltar e de graca: nada de custo de entrada (so o custo fixo do dia).
    assert caixa_antes - out["estado"]["caixa"] <= 300


def test_sem_isopor_vivo_o_dia_roda_de_casa():
    st = bridge.novo_jogo("ce", 1)
    st["local_atual"] = "isopor"
    st["locais_desbloqueados"] = ["casa", "isopor"]
    st["isopor"] = None
    out = bridge.jogar_dia(st, {"producao": {}, "precos": {}, "compras": {}})
    assert out["resultado"]["local"] == "casa"
    assert out["resultado"]["custo_fixo"] == 0, "em casa nao paga o fixo da rua"
    # O ponto continua do jogador: e o que mantem a vitrine de isopor visivel.
    assert out["estado"]["local_atual"] == "isopor"


def test_catalogo_em_ingles_traduz_a_interface():
    cat = bridge.catalogo("ce", lang="en")
    assert cat["lang"] == "en"
    assert cat["textos"]["feira.titulo"] == "Market"
    assert cat["textos"]["ui.novo_jogo"] == "New game"
    assert not any(v.startswith("⟨missing:") for v in cat["textos"].values())
    # Nome proprio fica: o produto continua sendo dindin.
    assert cat["produto"]["sing"] == "dindin"
    nomes = {s["key"]: s["nome"] for s in cat["sabores"]}
    assert nomes["coco"] == "Coconut"
    insumos = {i["key"]: i["nome"] for i in cat["insumos"]}
    assert insumos["acucar"] == "Sugar"
    assert any("pricey" in f for f in cat["barks"]["preco_alto"])


def test_catalogo_default_continua_em_portugues():
    cat = bridge.catalogo("ce")
    assert cat["lang"] == "pt"
    assert cat["textos"]["feira.titulo"] == "Feira"
    nomes = {s["key"]: s["nome"] for s in cat["sabores"]}
    assert nomes["coco"] == "Coco"


def test_regioes_em_ingles_mantem_a_giria():
    """A giria e fala de rua: fica em portugues ate no modo ingles."""
    en = {r["key"]: r for r in bridge.regioes("en")}
    assert en["ce"]["produto"] == "dindin"
    assert "Vixe" in en["ce"]["giria"]
    assert any(f["nome"] == "Coconut" for f in en["ce"]["favoritos"])


def test_isopores_e_sabores_do_jogador_em_ingles():
    st = bridge.novo_jogo("pa", 1)
    st["local_atual"] = "isopor"
    st["locais_desbloqueados"] = ["casa", "isopor"]
    info = bridge.isopores(st, lang="en")
    assert all(not o["nome"].startswith("⟨missing:") for o in info["opcoes"])
    assert "styrofoam" in info["opcoes"][0]["nome"].lower()

    sabores = bridge.sabores_do_jogador(st, lang="en")
    coco = next(s for s in sabores if s["key"] == "coco")
    assert coco["nome"] == "Coconut"
    assert all("nome" in r and not r["nome"].startswith("⟨missing:")
               for r in coco["receita"])
    assert coco["faltando"], "sem estoque, lista o que falta (em ingles)"
    assert "Sugar" in coco["faltando"]
