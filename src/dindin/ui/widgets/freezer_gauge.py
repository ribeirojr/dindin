"""Barra de ocupacao do freezer. Fica vermelha quando passa da capacidade."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, ProgressBar

from ...i18n import Translator


class FreezerGauge(Vertical):
    def __init__(self, tr: Translator, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tr = tr
        self._usado = 0
        self._cap = 1

    def compose(self) -> ComposeResult:
        yield Label("", id="freezer-label")
        yield ProgressBar(total=100, show_eta=False, id="freezer-bar")

    def atualizar(self, usado: int, capacidade: int) -> None:
        self._usado, self._cap = usado, max(1, capacidade)
        pct = min(100, round(100 * usado / self._cap))
        cor = "red" if usado > self._cap else ("yellow" if pct > 80 else "green")
        rotulo = self.tr.t("cozinha.freezer")
        self.query_one("#freezer-label", Label).update(
            f"[{cor}]{rotulo}: {usado}/{self._cap}[/]"
        )
        self.query_one("#freezer-bar", ProgressBar).update(progress=pct)
