"""Quanto gelo levar pro isopor.

A aposta: gelo custa pouco, mas no calor rende menos. Levar de menos
derrete a mercadoria; levar demais e dinheiro parado. So aparece fora
de casa -- em casa o freezer resolve.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from ...content.ingredients import INSUMOS
from ...content.regions import REGIOES
from ...i18n import money
from ...sim.freezer import cobertura_do_saco
from ..widgets import WeatherCard


class IceScreen(Screen[int]):
    BINDINGS = [("escape", "cancelar", "Voltar")]

    def __init__(self, state, tr, clima, unidades: int) -> None:
        super().__init__()
        self.state, self.tr, self.clima = state, tr, clima
        self.unidades = unidades
        self.cobertura = cobertura_do_saco(clima.heat_index)
        # Comeca sugerindo o suficiente, mas o jogador pode cortar.
        self.sacos = max(1, -(-unidades // self.cobertura))
        self.preco = INSUMOS["gelo"].preco_unitario(
            1, REGIOES[state.regiao].custo_insumo_mod
        )

    def compose(self) -> ComposeResult:
        yield Static("Gelo", classes="titulo-tela")
        yield Static("Quanto gelo você vai levar pro isopor?",
                     classes="subtitulo-tela")
        with Horizontal():
            yield WeatherCard(self.tr, classes="painel")
            yield Static("", id="gelo-info", classes="painel")
        yield Static("", id="gelo-conta", classes="aviso")
        yield Static("[dim]←→ ou +/- muda a quantidade[/]", classes="aviso")
        with Horizontal(classes="linha-botoes"):
            yield Button("Confirmar", variant="success", id="ok")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(WeatherCard).mostrar(self.clima)
        self._atualizar()
        self.query_one("#ok", Button).focus()

    def _atualizar(self) -> None:
        coberto = self.sacos * self.cobertura
        derrete = max(0, self.unidades - coberto)
        custo = self.sacos * self.preco

        calor = ""
        if self.cobertura < 50:
            calor = (f"\n[yellow]Tá quente: hoje um saco só segura "
                     f"{self.cobertura} (normal é 50).[/]")

        self.query_one("#gelo-info", Static).update(
            f"[dim]Você vai levar[/] [b]{self.unidades}[/] "
            f"{self.tr.t('produto.plur')}\n"
            f"[dim]Um saco segura[/] [b]{self.cobertura}[/] hoje\n"
            f"[dim]Preço do saco[/] [b]{money(self.preco)}[/]{calor}"
        )

        if derrete:
            aviso = (f"[red]Vai derreter {derrete} "
                     f"{self.tr.t('produto.plur')}![/]")
        else:
            folga = coberto - self.unidades
            aviso = (f"[green]Cobre tudo.[/]" +
                     (f" [dim](sobra pra mais {folga})[/]" if folga else ""))

        self.query_one("#gelo-conta", Static).update(
            f"[b]{self.sacos}[/] saco(s) = [b]{money(custo)}[/]   {aviso}"
        )

    def _mudar(self, d: int) -> None:
        maximo = max(0, self.state.caixa // self.preco)
        self.sacos = max(0, min(maximo, self.sacos + d))
        self._atualizar()

    def key_right(self) -> None:
        self._mudar(1)

    def key_left(self) -> None:
        self._mudar(-1)

    def key_plus(self) -> None:
        self._mudar(1)

    def key_minus(self) -> None:
        self._mudar(-1)

    def action_cancelar(self) -> None:
        self.dismiss(self.sacos)

    def on_button_pressed(self) -> None:
        self.dismiss(self.sacos)
