"""Fim de jogo: vitoria ou falencia."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from ...i18n import money


class GameOverScreen(Screen[str]):
    def __init__(self, state, tr, motivo: str) -> None:
        super().__init__()
        self.state, self.tr, self.motivo = state, tr, motivo

    def compose(self) -> ComposeResult:
        venceu = self.motivo == "vitoria"
        titulo = self.tr.t("cap.vitoria" if venceu else "cap.falencia")
        cor = "green" if venceu else "red"
        h = self.state.historico
        melhor = max((r.lucro for r in h), default=0)
        vendidos = sum(r.vendidos for r in h)
        with Vertical(id="menu-principal"):
            yield Static(f"[b {cor}]{titulo}[/]\n")
            yield Static(
                f"[dim]Dias jogados:[/] {self.state.dia - 1}\n"
                f"[dim]{self.tr.t('produto.plur').capitalize()} vendidos:[/] {vendidos}\n"
                f"[dim]Melhor dia:[/] {money(melhor)}\n"
                f"[dim]Caixa final:[/] {money(self.state.caixa)}\n"
                f"[dim]Reputação:[/] {self.state.reputacao:.0f}/100\n"
            )
            with Horizontal(classes="linha-botoes"):
                yield Button("Jogar de novo", variant="success", id="denovo")
                yield Button("Sair", id="sair")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sair":
            self.app.exit()
        else:
            self.dismiss("denovo")
