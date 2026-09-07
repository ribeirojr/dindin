"""Termometro de preco: mostra como a freguesia enxerga o preco.

Junto com a demanda potencial no relatorio, e o que transforma a formula
em algo aprendivel em vez de adivinhacao.
"""

from textual.reactive import reactive
from textual.widgets import Static

from ...i18n import Translator
from ...sim.demand import f_preco

_FAIXAS = (
    (0.90, "preco.barato", "green"),
    (0.70, "preco.justo", "green"),
    (0.45, "preco.salgado", "yellow"),
    (0.20, "preco.caro", "dark_orange"),
    (0.00, "preco.absurdo", "red"),
)


class PriceThermometer(Static):
    preco: reactive[int] = reactive(0)
    preco_ref: reactive[int] = reactive(200)
    tolerancia: reactive[float] = reactive(1.0)

    def __init__(self, tr: Translator, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tr = tr

    def _render_barra(self) -> str:
        resposta = f_preco(self.preco, self.preco_ref, self.tolerancia)
        rotulo, cor = "preco.absurdo", "red"
        for minimo, chave, c in _FAIXAS:
            if resposta >= minimo:
                rotulo, cor = chave, c
                break
        cheias = max(0, min(20, round(resposta * 20)))
        barra = "█" * cheias + "░" * (20 - cheias)
        texto = self.tr.t(rotulo)
        return f"[{cor}]{barra}[/] [b {cor}]{texto}[/]  ({resposta * 100:.0f}%)"

    def watch_preco(self) -> None:
        self.update(self._render_barra())

    def watch_tolerancia(self) -> None:
        self.update(self._render_barra())

    def watch_preco_ref(self) -> None:
        self.update(self._render_barra())

    def on_mount(self) -> None:
        self.update(self._render_barra())
