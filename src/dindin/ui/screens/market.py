"""Feira: compra de insumos."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Static

from ...content.ingredients import INSUMOS, insumos_disponiveis
from ...content.regions import REGIOES
from ...i18n import money
from ...sim.economy import custo_compras
from ..widgets import WeatherCard

# Gelo fica de fora: o jogo compra sozinho a quantidade necessaria pro ponto
# (ver ui/app.py). Deixar na feira faria o jogador pagar duas vezes.


class MarketScreen(Screen[dict]):
    BINDINGS = [("escape", "cancelar", "Voltar")]

    def __init__(self, state, tr, clima) -> None:
        super().__init__()
        self.state, self.tr, self.clima = state, tr, clima
        self.carrinho: dict[str, int] = {}
        # So mostra o que o jogador ja pode usar: no dia 1 sao 4 itens.
        self._ordem = tuple(i.key for i in
                            insumos_disponiveis(state.locais_desbloqueados))

    def compose(self) -> ComposeResult:
        yield Static(self.tr.t("feira.titulo"), classes="titulo-tela")
        yield Static(self.tr.t("feira.subtitulo"), classes="subtitulo-tela")
        with Horizontal():
            yield WeatherCard(self.tr, classes="painel")
            yield Static("", id="feira-total", classes="painel")
        yield DataTable(id="tabela-feira", cursor_type="row")
        yield Static("[dim]+/- ou setas pra mudar a quantidade. "
                     "Comprando mais, sai mais barato.[/]", classes="aviso")
        with Horizontal(classes="linha-botoes"):
            yield Button("Confirmar compra", variant="success", id="ok")
            yield Button("Não comprar nada", id="pular")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(WeatherCard).mostrar(self.clima)
        t = self.query_one(DataTable)
        t.add_columns(self.tr.t("feira.insumo"), self.tr.t("feira.unidade"),
                      self.tr.t("feira.preco"), self.tr.t("feira.estoque"),
                      self.tr.t("feira.carrinho"))
        self._recarregar()
        t.focus()
        self._atualizar_total()

    def _recarregar(self) -> None:
        t = self.query_one(DataTable)
        linha = t.cursor_row
        t.clear()
        mod = REGIOES[self.state.regiao].custo_insumo_mod
        for key in self._ordem:
            ing = INSUMOS[key]
            qtd = self.carrinho.get(key, 0)
            preco = ing.preco_unitario(max(1, qtd), mod)
            tem = self.state.inventario.total(key)
            t.add_row(ing.nome, ing.unidade, money(preco),
                      f"{tem:.1f}", str(qtd) if qtd else "-", key=key)
        if linha < t.row_count:
            t.move_cursor(row=linha)

    def _atualizar_total(self) -> None:
        total = custo_compras(self.carrinho, self.state.regiao)
        falta = total > self.state.caixa
        botao = self.query_one("#ok", Button)
        botao.disabled = falta
        botao.label = ("Falta dinheiro" if falta else "Confirmar compra")
        cor = "red" if falta else "green"
        aviso = f"\n[red]{self.tr.t('feira.sem_dinheiro')}[/]" if falta else ""
        self.query_one("#feira-total", Static).update(
            f"[dim]{self.tr.t('ui.caixa')}[/]  [b]{money(self.state.caixa)}[/]\n"
            f"[dim]{self.tr.t('feira.total')}[/]  [b {cor}]{money(total)}[/]\n"
            f"[dim]Sobra[/]  {money(self.state.caixa - total)}{aviso}"
        )

    def _mudar(self, delta: int) -> None:
        t = self.query_one(DataTable)
        if t.cursor_row < 0:
            return
        key = self._ordem[t.cursor_row]
        novo = max(0, self.carrinho.get(key, 0) + delta)
        if novo:
            self.carrinho[key] = novo
        else:
            self.carrinho.pop(key, None)
        self._recarregar()
        self._atualizar_total()

    def key_plus(self) -> None:
        self._mudar(1)

    def key_minus(self) -> None:
        self._mudar(-1)

    def key_right(self) -> None:
        self._mudar(1)

    def key_left(self) -> None:
        self._mudar(-1)

    def action_cancelar(self) -> None:
        self.dismiss({})

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "pular":
            self.dismiss({})
            return
        if custo_compras(self.carrinho, self.state.regiao) > self.state.caixa:
            self.app.bell()
            return
        self.dismiss(dict(self.carrinho))
