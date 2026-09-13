"""O dia acontecendo. O resultado JA foi calculado: isso aqui e so teatro,
o que mantem a simulacao deterministica."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Digits, Footer, ProgressBar, RichLog, Static

from ...i18n import money
from ...sim.rng import stream
from ..widgets import SceneCard


class SimulationScreen(Screen[None]):
    BINDINGS = [("escape", "pular", "Pular")]
    PASSOS = 24

    def __init__(self, state, tr, resultado) -> None:
        super().__init__()
        self.state, self.tr, self.resultado = state, tr, resultado
        self.passo = 0
        self._timer = None

    def compose(self) -> ComposeResult:
        yield Static(self.tr.t("dia.vendendo"), classes="titulo-tela")
        yield SceneCard(id="cena-venda")
        with Horizontal():
            yield Digits("0", id="contador")
        yield ProgressBar(total=self.PASSOS, show_eta=False, id="relogio")
        yield RichLog(id="feed-barks", markup=True, wrap=True)
        with Horizontal(classes="linha-botoes"):
            yield Button("Pular", id="pular")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(SceneCard).mostrar(
            self.resultado.local, self.resultado.clima, "venda",
            self.state.regiao)
        self._rng = stream(self.state.seed, self.resultado.dia, "playback")
        self._timer = self.set_interval(0.09, self._tick)

    def _tick(self) -> None:
        self.passo += 1
        frac = self.passo / self.PASSOS
        parcial = int(self.resultado.receita * frac)
        self.query_one("#contador", Digits).update(money(parcial))
        self.query_one("#relogio", ProgressBar).update(progress=self.passo)

        barks = self.resultado.barks
        if barks and self.passo % 2 == 0:
            i = (self.passo // 2 - 1) % len(barks)
            tag, _ = barks[i]
            fala = self.tr.bark(tag, self._rng)
            if fala:
                cor = "red" if "preco_alto" in str(tag) else "white"
                self.query_one(RichLog).write(f"[{cor}]— {fala}[/]")

        if self.passo >= self.PASSOS:
            self.action_pular()

    def action_pular(self) -> None:
        if self._timer:
            self._timer.stop()
            self._timer = None
        self.query_one("#contador", Digits).update(money(self.resultado.receita))
        self.query_one("#relogio", ProgressBar).update(progress=self.PASSOS)
        self.dismiss(None)

    def on_button_pressed(self) -> None:
        self.action_pular()
