"""Tela de abertura."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

ARTE = r"""
   ___  _         ___  _
  |   \(_)_ _  __| (_)_ _
  | |) | | ' \/ _` | | ' \
  |___/|_|_||_\__,_|_|_||_|
"""


class TitleScreen(Screen[str]):
    BINDINGS = [("q", "app.quit", "Sair")]

    def compose(self) -> ComposeResult:
        with Vertical(id="menu-principal"):
            yield Static(ARTE, id="titulo-arte")
            yield Static("a vida de quem vende gelado no Brasil", id="subtitulo")
            yield Button("Jogo novo", variant="success", id="novo")
            yield Button("Como se joga", id="ajuda")
            yield Button("Sair", id="sair")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sair":
            self.app.exit()
        else:
            self.dismiss(event.button.id or "novo")
