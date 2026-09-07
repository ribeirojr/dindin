"""Quadradinho de numero: rotulo em cima, valor grande embaixo."""

from textual.widgets import Static


class StatTile(Static):
    def __init__(self, rotulo: str, valor: str = "", classe: str = "", **kwargs):
        super().__init__(**kwargs)
        self.add_class("tile")
        self._rotulo, self._valor, self._classe = rotulo, valor, classe

    def on_mount(self) -> None:
        self.atualizar(self._valor, self._classe)

    def atualizar(self, valor: str, classe: str = "") -> None:
        self._valor, self._classe = valor, classe
        cor = {"lucro": "green", "prejuizo": "red"}.get(classe, "white")
        self.update(f"[dim]{self._rotulo}[/]\n[b {cor}]{valor}[/]")
