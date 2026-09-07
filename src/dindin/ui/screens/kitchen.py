"""Cozinha: quantas unidades fazer de cada sabor."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Static

from ...content.flavors import sabores_disponiveis
from ...i18n import money
from ...sim.economy import (
    custo_unitario,
    pode_produzir,
    pode_produzir_com_reserva,
)
from ...sim.freezer import capacidade_total
from ..widgets import FreezerGauge


class KitchenScreen(Screen[dict]):
    BINDINGS = [("escape", "cancelar", "Voltar")]

    def __init__(self, state, tr) -> None:
        super().__init__()
        self.state, self.tr = state, tr
        self.sabores = sabores_disponiveis(state.locais_desbloqueados)
        self.producao: dict[str, int] = {}

    def compose(self) -> ComposeResult:
        yield Static(self.tr.t("cozinha.titulo"), classes="titulo-tela")
        yield Static(self.tr.t("cozinha.subtitulo"), classes="subtitulo-tela")
        yield FreezerGauge(self.tr)
        yield DataTable(id="tabela-cozinha", cursor_type="row")
        yield Static("", id="aviso-freezer", classes="aviso")
        with Horizontal(classes="linha-botoes"):
            yield Button("Confirmar", variant="success", id="ok")
            yield Button("Não fazer nada", id="pular")
        yield Footer()

    def on_mount(self) -> None:
        t = self.query_one(DataTable)
        t.add_columns(self.tr.t("cozinha.sabor"), self.tr.t("cozinha.custo"),
                      self.tr.t("cozinha.pronto"), self.tr.t("cozinha.maximo"),
                      self.tr.t("cozinha.produzir"))
        self._recarregar()
        t.focus()

    def _recarregar(self) -> None:
        t = self.query_one(DataTable)
        linha = t.cursor_row
        t.clear()
        for f in self.sabores:
            t.add_row(
                f.nome,
                money(custo_unitario(f.key, self.state.regiao)),
                str(self.state.inventario.prontos.get(f.key, 0)),
                str(pode_produzir_com_reserva(self.state, f.key, self.producao)),
                str(self.producao.get(f.key, 0)) or "-",
                key=f.key,
            )
        if linha < t.row_count:
            t.move_cursor(row=linha)
        usado = self.state.inventario.total_prontos() + sum(self.producao.values())
        cap = capacidade_total(self.state)
        self.query_one(FreezerGauge).atualizar(usado, cap)
        self.query_one("#aviso-freezer", Static).update(
            self.tr.t("cozinha.freezer_cheio") if usado > cap else ""
        )

    def _mudar(self, delta: int) -> None:
        t = self.query_one(DataTable)
        if t.cursor_row < 0:
            return
        f = self.sabores[t.cursor_row]
        maximo = pode_produzir_com_reserva(self.state, f.key, self.producao)
        novo = max(0, min(maximo, self.producao.get(f.key, 0) + delta))
        if novo:
            self.producao[f.key] = novo
        else:
            self.producao.pop(f.key, None)
        self._recarregar()

    def key_plus(self) -> None:
        self._mudar(5)

    def key_minus(self) -> None:
        self._mudar(-5)

    def key_right(self) -> None:
        self._mudar(5)

    def key_left(self) -> None:
        self._mudar(-5)

    def action_cancelar(self) -> None:
        self.dismiss({})

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss({} if event.button.id == "pular" else dict(self.producao))
