"""Relatorio do dia. A coluna 'queriam comprar' e o que ensina o jogo:
sem ela o jogador nao entende por que vendeu pouco."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, ProgressBar, Static

from ...content.flavors import SABORES
from ...content.locations import LOCAIS
from ...i18n import money
from ...sim.engine import resumo_do_dia
from ..widgets import StatTile, WeatherCard


class ReportScreen(Screen[None]):
    BINDINGS = [("enter", "seguir", "Próximo dia"), ("escape", "seguir", "Seguir")]

    def __init__(self, state, tr, resultado) -> None:
        super().__init__()
        self.state, self.tr, self.resultado = state, tr, resultado

    def compose(self) -> ComposeResult:
        r = self.resultado
        yield Static(f"{self.tr.t('rel.titulo')} — {self.tr.t('ui.dia')} {r.dia}",
                     classes="titulo-tela")
        yield Static(self.tr.t(resumo_do_dia(r)), classes="subtitulo-tela")
        with Horizontal():
            yield WeatherCard(self.tr, classes="painel")
            yield Static("", id="eventos-dia", classes="painel")
        yield DataTable(id="tabela-rel", cursor_type="none")
        with Horizontal():
            yield StatTile(self.tr.t("rel.receita"), id="t-receita")
            yield StatTile(self.tr.t("rel.custos"), id="t-custos")
            yield StatTile(self.tr.t("rel.lucro"), id="t-lucro")
            yield StatTile(self.tr.t("ui.caixa"), id="t-caixa")
        yield Static("", id="meta-label", classes="aviso")
        yield ProgressBar(total=100, show_eta=False, id="barra-meta")
        with Horizontal(classes="linha-botoes"):
            yield Button(self.tr.t("ui.proximo_dia"), variant="success", id="ok")
        yield Footer()

    def on_mount(self) -> None:
        r = self.resultado
        self.query_one(WeatherCard).mostrar(r.clima, self.tr.t("ui.dia"))

        linhas = [self.tr.t(e.text_key, **e.params) for e in r.eventos]
        if r.demanda_nao_atendida > 0:
            linhas.append("[yellow]" +
                          self.tr.t("rel.sellout", perdidos=r.demanda_nao_atendida) +
                          "[/]")
        sobra = self.state.inventario.total_prontos()
        if sobra:
            linhas.append("[dim]" + self.tr.t("rel.sobrou", sobra=sobra) + "[/]")
        if not r.vendidos:
            linhas.append("[red]" + self.tr.t("rel.nada_vendido") + "[/]")
        self.query_one("#eventos-dia", Static).update(
            "\n".join(linhas) or "[dim]Dia tranquilo.[/]"
        )

        t = self.query_one(DataTable)
        t.add_columns(self.tr.t("rel.sabor"), self.tr.t("rel.levou"),
                      self.tr.t("rel.vendeu"), self.tr.t("rel.queria"),
                      self.tr.t("rel.derreteu"), self.tr.t("rel.receita"))
        for f in r.por_sabor:
            faltou = f.demanda_potencial > f.ofertados
            queria = (f"[yellow]{f.demanda_potencial}[/]" if faltou
                      else str(f.demanda_potencial))
            t.add_row(SABORES[f.flavor].nome, str(f.ofertados), str(f.vendidos),
                      queria,
                      str(f.perdidos_derretimento) if f.perdidos_derretimento else "-",
                      money(f.receita))

        self.query_one("#t-receita", StatTile).atualizar(money(r.receita))
        self.query_one("#t-custos", StatTile).atualizar(
            money(r.custo_insumos + r.custo_fixo))
        self.query_one("#t-lucro", StatTile).atualizar(
            money(r.lucro), "lucro" if r.lucro >= 0 else "prejuizo")
        self.query_one("#t-caixa", StatTile).atualizar(money(r.caixa_final))

        meta = LOCAIS[self.state.local_atual].meta_caixa
        pct = max(0, min(100, round(100 * r.caixa_final / meta)))
        self.query_one("#meta-label", Static).update(
            f"{self.tr.t('ui.meta')}: {money(r.caixa_final)} / {money(meta)}"
        )
        self.query_one("#barra-meta", ProgressBar).update(progress=pct)
        self.query_one("#ok", Button).focus()

    def action_seguir(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self) -> None:
        self.dismiss(None)
