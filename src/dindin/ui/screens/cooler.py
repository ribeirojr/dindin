"""Comprar isopor. Compra unica que cobre varios dias.

Diferente do gelo (consumivel diario), a caixa e capital: voce paga uma
vez e ela te serve por uns dias, ate rachar. A escolha e entre gastar
pouco agora e repor sempre, ou investir numa caixa boa que cabe mais,
derrete menos e dura mais.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from ...content.coolers import ISOPORES, ORDEM_ISOPORES
from ...i18n import money


class CoolerScreen(Screen[str | None]):
    BINDINGS = [("escape", "cancelar", "Agora não")]

    def __init__(self, state, tr, obrigatorio: bool = False) -> None:
        super().__init__()
        self.state, self.tr = state, tr
        self.obrigatorio = obrigatorio

    def compose(self) -> ComposeResult:
        yield Static("Isopor", classes="titulo-tela")
        motivo = ("Sem isopor não dá pra vender na rua."
                  if self.obrigatorio else "Seu isopor tá acabando.")
        yield Static(motivo, classes="subtitulo-tela")
        with Vertical(id="lista-isopores"):
            for key in ORDEM_ISOPORES:
                c = ISOPORES[key]
                pode = self.state.caixa >= c.custo
                with Horizontal(classes="painel"):
                    yield Static(
                        f"[b]{c.nome}[/]  [dim]{c.descricao}[/]\n"
                        f"[dim]Dura[/] {c.dias} dias · "
                        f"[dim]cabe[/] {c.capacidade} · "
                        f"[dim]derrete[/] {int(c.derretimento * 100)}% · "
                        f"[dim]sai por[/] {money(c.custo_por_dia)}/dia",
                        classes="iso-desc",
                    )
                    yield Button(
                        money(c.custo), id=f"iso-{key}",
                        variant="success" if pode else "default",
                        disabled=not pode,
                    )
        yield Static(f"[dim]Seu caixa: {money(self.state.caixa)}[/]",
                     classes="aviso")
        if not self.obrigatorio:
            with Horizontal(classes="linha-botoes"):
                yield Button("Agora não", id="pular")
        elif not self._pode_alguma():
            # Sem dinheiro pra caixa nenhuma a tela viraria beco sem saida:
            # todo botao desabilitado e escape mudo. A saida e vender de casa.
            yield Static("[red]Não dá pra pagar nenhuma caixa hoje.[/]",
                         classes="aviso")
            with Horizontal(classes="linha-botoes"):
                yield Button("Vender de casa hoje", variant="warning",
                             id="pular")
        yield Footer()

    def _pode_alguma(self) -> bool:
        return any(self.state.caixa >= ISOPORES[k].custo
                   for k in ORDEM_ISOPORES)

    def action_cancelar(self) -> None:
        if not self.obrigatorio or not self._pode_alguma():
            self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id or ""
        if bid == "pular":
            self.dismiss(None)
        elif bid.startswith("iso-"):
            self.dismiss(bid.removeprefix("iso-"))
