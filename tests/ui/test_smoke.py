"""Testes de fumaca da TUI. As invariantes de verdade estao em tests/sim."""

import pytest

from dindin.i18n import REGIOES_I18N
from dindin.ui.app import DindinApp

TAMANHO = (110, 40)


async def test_abre_na_tela_de_titulo():
    app = DindinApp(seed=1)
    async with app.run_test(size=TAMANHO):
        assert app.screen.__class__.__name__ == "TitleScreen"


async def test_titulo_leva_pra_escolha_de_regiao():
    app = DindinApp(seed=1)
    async with app.run_test(size=TAMANHO) as pilot:
        await pilot.click("#novo")
        await pilot.pause()
        assert app.screen.__class__.__name__ == "RegionSelectScreen"


async def test_cooler_obrigatorio_sem_dinheiro_tem_saida():
    """Softlock: sem caixa pra isopor nenhum, todo botao ficava desabilitado
    e o escape mudo -- o jogador ficava preso na tela pra sempre."""
    from textual.app import App

    from dindin.i18n import Translator
    from dindin.sim.state import GameState
    from dindin.ui.screens.cooler import CoolerScreen

    class Host(App[None]):
        pass

    app = Host()
    async with app.run_test(size=TAMANHO) as pilot:
        state = GameState(caixa=1000, local_atual="isopor")  # nem o simples
        saida: list = []
        app.push_screen(CoolerScreen(state, Translator("ce"), obrigatorio=True),
                        callback=saida.append)
        await pilot.pause()
        await pilot.click("#pular")   # "Vender de casa hoje"
        await pilot.pause()
        assert saida == [None]


async def test_cooler_obrigatorio_com_dinheiro_nao_tem_atalho():
    """Com caixa pra comprar, a unica saida e comprar mesmo."""
    from textual.app import App

    from dindin.i18n import Translator
    from dindin.sim.state import GameState
    from dindin.ui.screens.cooler import CoolerScreen

    class Host(App[None]):
        pass

    app = Host()
    async with app.run_test(size=TAMANHO) as pilot:
        state = GameState(caixa=10000, local_atual="isopor")
        app.push_screen(CoolerScreen(state, Translator("ce"), obrigatorio=True))
        await pilot.pause()
        assert not app.screen.query("#pular")


@pytest.mark.parametrize("regiao", REGIOES_I18N)
async def test_cada_regiao_inicia_o_jogo_sem_texto_faltando(regiao):
    """Nenhuma tela pode mostrar o marcador de traducao faltando."""
    app = DindinApp(seed=3, regiao=regiao)
    async with app.run_test(size=TAMANHO) as pilot:
        await pilot.pause()
        assert app.state is not None
        assert app.state.regiao == regiao
        assert app.screen.__class__.__name__ == "PlanScreen"
        texto = _texto_da_tela(app)
        assert "⟨missing:" not in texto, texto[:400]


@pytest.mark.parametrize("regiao", REGIOES_I18N)
async def test_produto_regional_aparece_na_ajuda(regiao):
    app = DindinApp(seed=3, regiao=regiao)
    async with app.run_test(size=TAMANHO) as pilot:
        await pilot.pause()
        app.action_ajuda()
        await pilot.pause()
        assert app.tr.produto in _texto_da_tela(app)


async def test_fluxo_de_um_dia_inteiro():
    """Feira -> cozinha -> preco -> venda -> relatorio, e o dia avanca."""
    app = DindinApp(seed=11, regiao="ce")
    async with app.run_test(size=TAMANHO) as pilot:
        await pilot.pause()
        assert app.state.dia == 1

        # O dia abre planejando: ve o ponto e o tempo antes de gastar.
        assert app.screen.__class__.__name__ == "PlanScreen"
        await pilot.click("#ok")
        await pilot.pause()

        # Feira: compra do insumo sob o cursor.
        assert app.screen.__class__.__name__ == "MarketScreen"
        for _ in range(3):
            await pilot.press("plus")
        await pilot.press("down")
        await pilot.press("down")
        for _ in range(2):
            await pilot.press("plus")
        await pilot.click("#ok")
        await pilot.pause()

        # Cozinha
        assert app.screen.__class__.__name__ == "KitchenScreen"
        await pilot.click("#pular")
        await pilot.pause()

        # Sem estoque o jogo pula direto pro relatorio.
        assert app.screen.__class__.__name__ in ("PricingScreen", "ReportScreen")
        if app.screen.__class__.__name__ == "PricingScreen":
            await pilot.click("#ok")
            await pilot.pause()
            await pilot.press("escape")  # pula a animacao
            await pilot.pause()
        assert app.screen.__class__.__name__ == "ReportScreen"
        assert "⟨missing:" not in _texto_da_tela(app)

        await pilot.click("#ok")
        await pilot.pause()
        assert app.state.dia == 2


async def test_termometro_de_preco_reage_ao_valor():
    from dindin.i18n import Translator
    from dindin.ui.widgets import PriceThermometer

    tr = Translator("pa")
    term = PriceThermometer(tr)
    term.preco_ref = 400
    term.tolerancia = 1.0
    term.preco = 200
    barato = term._render_barra()
    term.preco = 800
    caro = term._render_barra()
    assert barato != caro
    assert tr.t("preco.barato") in barato or tr.t("preco.justo") in barato
    assert tr.t("preco.absurdo") in caro or tr.t("preco.caro") in caro


def _texto_da_tela(app) -> str:
    """Le o que esta de fato desenhado no terminal virtual."""
    import re

    svg = app.export_screenshot()
    # O SVG guarda o texto da tela dentro das tags <text>.
    return " ".join(re.findall(r"<text[^>]*>([^<]*)</text>", svg))


async def test_relatorio_contabiliza_o_que_foi_gasto_na_feira():
    """Regressao: a UI comprava fora do plano e o relatorio mostrava custo zero."""
    app = DindinApp(seed=5, regiao="ce")
    async with app.run_test(size=TAMANHO) as pilot:
        await pilot.pause()
        caixa_inicial = app.state.caixa
        await pilot.click("#ok")   # sai da tela de plano
        await pilot.pause()

        for _ in range(3):
            await pilot.press("plus")
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("plus")
        for _ in range(5):
            await pilot.press("down")
        await pilot.press("plus")
        await pilot.click("#ok")
        await pilot.pause()

        if app.screen.__class__.__name__ == "KitchenScreen":
            for _ in range(8):
                await pilot.press("plus")
            await pilot.click("#ok")
            await pilot.pause()
        if app.screen.__class__.__name__ == "PricingScreen":
            await pilot.click("#ok")
            await pilot.pause()
        if app.screen.__class__.__name__ == "SimulationScreen":
            await pilot.press("escape")
            await pilot.pause()

        r = app.state.historico[-1]
        assert r.custo_insumos > 0, "compra da feira nao entrou no relatorio"
        assert r.receita - r.custo_insumos - r.custo_fixo == r.lucro
        assert caixa_inicial + r.lucro == r.caixa_final


def test_gelo_fora_da_feira_do_terminal():
    """Regressao: gelo na feira + compra automatica = cobranca dobrada."""
    from dindin.content.ingredients import insumos_disponiveis

    todos = insumos_disponiveis(["casa", "isopor", "praia", "escola", "carrinho"])
    assert "gelo" not in [i.key for i in todos]


def test_dia_1_comeca_com_pouca_coisa():
    """Cadencia: quem esta aprendendo nao pode levar 9 sabores na cara."""
    from dindin.content.flavors import sabores_disponiveis
    from dindin.content.ingredients import insumos_disponiveis

    assert len(sabores_disponiveis(["casa"])) == 3
    assert len(insumos_disponiveis(["casa"])) == 4


def test_cada_capitulo_abre_mais_opcoes():
    from dindin.content.flavors import sabores_disponiveis
    from dindin.content.ingredients import insumos_disponiveis

    acc, sabores, insumos = [], [], []
    for local in ("casa", "isopor", "praia", "escola"):
        acc.append(local)
        sabores.append(len(sabores_disponiveis(acc)))
        insumos.append(len(insumos_disponiveis(acc)))
    assert sabores == sorted(sabores) and sabores[0] < sabores[-1]
    assert insumos == sorted(insumos) and insumos[0] < insumos[-1]
