"""Preco: o termometro mostra como a freguesia enxerga cada valor."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Static

from ...content.flavors import SABORES
from ...i18n import money
from ...sim.economy import custo_unitario
from ..widgets import PriceThermometer


class PricingScreen(Screen[dict]):
    BINDINGS = [("escape", "cancelar", "Voltar")]

    def __init__(self, state, tr, tolerancia: float, sabores: list[str]) -> None:
        super().__init__()
        self.state, self.tr, self.tolerancia = state, tr, tolerancia
        self.sabores = sabores
        self.precos: dict[str, int] = {
            k: SABORES[k].preco_ref for k in sabores
        }
        self.idx = 0

    def compose(self) -> ComposeResult:
        yield Static(self.tr.t("preco.titulo"), classes="titulo-tela")
        yield Static(self.tr.t("preco.subtitulo"), classes="subtitulo-tela")
        with Vertical(id="lista-precos"):
            for k in self.sabores:
                with Vertical(classes="painel"):
                    yield Label("", id=f"lbl-{k}")
                    yield PriceThermometer(self.tr, id=f"term-{k}")
        yield Static("[dim]↑↓ escolhe o sabor · ←→ muda o preço de 10 em 10 "
                     "centavos[/]", classes="aviso")
        with Horizontal(classes="linha-botoes"):
            yield Button("Vender!", variant="success", id="ok")
        yield Footer()

    def on_mount(self) -> None:
        for k in self.sabores:
            term = self.query_one(f"#term-{k}", PriceThermometer)
            term.preco_ref = SABORES[k].preco_ref
            term.tolerancia = self.tolerancia
            term.preco = self.precos[k]
        self._atualizar()

    def _atualizar(self) -> None:
        for i, k in enumerate(self.sabores):
            sabor = SABORES[k]
            custo = custo_unitario(k, self.state.regiao)
            margem = self.precos[k] - custo
            seta = "[b yellow]▸[/] " if i == self.idx else "  "
            cor = "green" if margem > 0 else "red"
            self.query_one(f"#lbl-{k}", Label).update(
                f"{seta}[b]{sabor.nome}[/]   "
                f"[dim]{self.tr.t('preco.custo')}[/] {money(custo)}   "
                f"[dim]{self.tr.t('preco.preco')}[/] [b]{money(self.precos[k])}[/]   "
                f"[dim]{self.tr.t('preco.margem')}[/] [{cor}]{money(margem)}[/]"
            )
            self.query_one(f"#term-{k}", PriceThermometer).preco = self.precos[k]

    def key_down(self) -> None:
        self.idx = (self.idx + 1) % len(self.sabores)
        self._atualizar()

    def key_up(self) -> None:
        self.idx = (self.idx - 1) % len(self.sabores)
        self._atualizar()

    def _mudar(self, delta: int) -> None:
        k = self.sabores[self.idx]
        self.precos[k] = max(10, self.precos[k] + delta)
        self._atualizar()

    def key_right(self) -> None:
        self._mudar(10)

    def key_left(self) -> None:
        self._mudar(-10)

    def key_plus(self) -> None:
        self._mudar(10)

    def key_minus(self) -> None:
        self._mudar(-10)

    def action_cancelar(self) -> None:
        self.dismiss({})

    def on_button_pressed(self) -> None:
        self.dismiss(dict(self.precos))
