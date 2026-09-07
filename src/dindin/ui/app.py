"""DindinApp: amarra as telas no ciclo do dia."""

from textual.app import App

from ..content.flavors import SABORES
from ..i18n import Translator
from ..sim import progression
from ..sim.engine import advance_day, clima_do_dia, tolerancia_efetiva_do_dia
from ..sim.economy import comprar, produzir
from ..sim.freezer import capacidade_dia
from ..sim.state import DayPlan, GameState
from .screens.chapter_unlock import ChapterUnlockScreen
from .screens.cooler import CoolerScreen
from .screens.game_over import GameOverScreen
from .screens.help import HelpScreen
from .screens.ice import IceScreen
from .screens.kitchen import KitchenScreen
from .screens.market import MarketScreen
from .screens.plan import PlanScreen
from .screens.pricing import PricingScreen
from .screens.region_select import RegionSelectScreen
from .screens.report import ReportScreen
from .screens.simulation import SimulationScreen
from .screens.title import TitleScreen


class DindinApp(App[None]):
    CSS_PATH = "dindin.tcss"
    TITLE = "DinDin"
    BINDINGS = [("question_mark", "ajuda", "Ajuda"), ("ctrl+q", "quit", "Sair")]

    def __init__(self, seed: int | None = None, regiao: str | None = None) -> None:
        super().__init__()
        self.seed = seed if seed is not None else 20260907
        self.regiao_inicial = regiao
        self.state: GameState | None = None
        self.tr = Translator("ce")

    async def on_mount(self) -> None:
        self.run_worker(self._jogo(), exclusive=True)

    def action_ajuda(self) -> None:
        self.push_screen(HelpScreen(self.tr))

    async def _jogo(self) -> None:
        while True:
            if self.regiao_inicial is None:
                escolha = await self.push_screen_wait(TitleScreen())
                if escolha == "ajuda":
                    await self.push_screen_wait(HelpScreen(self.tr))
                    continue
                regiao = await self.push_screen_wait(RegionSelectScreen())
            else:
                regiao = self.regiao_inicial

            self.tr = Translator(regiao)
            self.state = GameState(seed=self.seed, regiao=regiao,
                                   local_atual="casa")
            motivo = await self._campanha()
            de_novo = await self.push_screen_wait(
                GameOverScreen(self.state, self.tr, motivo)
            )
            if de_novo != "denovo":
                return
            self.regiao_inicial = None
            self.seed += 1

    async def _campanha(self) -> str:
        state = self.state
        assert state is not None
        while not state.encerrado:
            await self._um_dia()
            if state.encerrado:
                break
            prox = progression.pode_desbloquear(state)
            if prox:
                aceitou = await self.push_screen_wait(
                    ChapterUnlockScreen(self.tr, prox, state.caixa)
                )
                if aceitou:
                    progression.desbloquear(state, prox)
                    await self._garantir_isopor()
                    state.encerrado = progression.checar_fim(state)
        return state.encerrado or "falencia"

    async def _garantir_isopor(self) -> bool:
        """Fora de casa e preciso ter caixa. Devolve False se nao deu."""
        state = self.state
        assert state is not None
        if progression.precisa_de_isopor(state):
            escolha = await self.push_screen_wait(
                CoolerScreen(state, self.tr, obrigatorio=True)
            )
            if escolha:
                progression.comprar_isopor(state, escolha)
            return not progression.precisa_de_isopor(state)
        if progression.isopor_acabando(state):
            escolha = await self.push_screen_wait(
                CoolerScreen(state, self.tr, obrigatorio=False)
            )
            if escolha:
                progression.comprar_isopor(state, escolha)
        return True

    async def _um_dia(self) -> None:
        state = self.state
        assert state is not None
        if not await self._garantir_isopor():
            # Sem caixa e sem dinheiro pra comprar: volta pra casa.
            state.local_atual = "casa"
        clima = clima_do_dia(state, state.dia)

        # 1) PLANEJAR: ve o ponto e o tempo antes de decidir qualquer coisa.
        await self.push_screen_wait(PlanScreen(state, self.tr, clima))

        # 2) EXECUTAR: feira -> cozinha -> gelo -> preco -> venda.
        compras = await self.push_screen_wait(MarketScreen(state, self.tr, clima))
        gasto_insumos = comprar(state, compras) if compras else 0

        producao = await self.push_screen_wait(KitchenScreen(state, self.tr))
        if producao:
            produzir(state, producao)

        vendaveis = sorted(state.inventario.prontos)
        if not vendaveis:
            # Sem estoque nao tem o que vender: passa o dia com plano vazio.
            resultado = advance_day(
                state, DayPlan({}, {}, state.local_atual),
                gasto_previo=gasto_insumos,
            )
            await self.push_screen_wait(ReportScreen(state, self.tr, resultado))
            return

        tol = tolerancia_efetiva_do_dia(state, state.local_atual, clima)
        precos = await self.push_screen_wait(
            PricingScreen(state, self.tr, tol, vendaveis)
        )
        if not precos:
            precos = {k: SABORES[k].preco_ref for k in vendaveis}

        # Fora de casa o jogador decide quanto gelo levar -- e uma aposta
        # contra o calor, nao uma taxa automatica.
        gelo = 0
        if state.local_atual != "casa":
            levando = min(state.inventario.total_prontos(),
                          capacidade_dia(state, state.local_atual))
            gelo = await self.push_screen_wait(
                IceScreen(state, self.tr, clima, levando)
            )

        plano = DayPlan(producao={}, precos=precos, local=state.local_atual,
                        compras={}, gelo=gelo)
        resultado = advance_day(state, plano, gasto_previo=gasto_insumos)

        await self.push_screen_wait(SimulationScreen(state, self.tr, resultado))
        await self.push_screen_wait(ReportScreen(state, self.tr, resultado))


def main() -> None:
    DindinApp().run()
