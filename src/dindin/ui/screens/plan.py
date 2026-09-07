"""Abertura do dia: onde voce esta, como vai estar o tempo, o que fazer.

Separa PLANEJAR de EXECUTAR. Antes o jogo caia direto na feira, sem o
jogador ver o lugar nem pensar no dia.
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Static

from ...content.flavors import sabores_disponiveis
from ...content.locations import LOCAIS
from ...i18n import money
from ..widgets import SceneCard, WeatherCard

# Dica curta por capitulo: ensina o que muda naquele ponto.
_DICAS = {
    "casa": "Comece pequeno: faça poucos e veja quantos a vizinhança quer.",
    "isopor": "Na rua o movimento é bem maior — mas chuva esvazia a calçada.",
    "praia": "Praia paga mais caro e adora cremoso. Só que chuva aqui é fatal.",
    "escola": "Criança tem pouco dinheiro: aqui o barato vende, o gourmet encalha.",
    "carrinho": "Seu ponto, suas regras. Olhe a previsão e escolha o dia certo.",
}


class PlanScreen(Screen[None]):
    BINDINGS = [("enter", "seguir", "Começar"), ("escape", "seguir", "Começar")]

    def __init__(self, state, tr, clima) -> None:
        super().__init__()
        self.state, self.tr, self.clima = state, tr, clima

    def compose(self) -> ComposeResult:
        local = LOCAIS[self.state.local_atual]
        yield Static(
            f"{self.tr.t('ui.dia')} {self.state.dia} · "
            f"{self.tr.t(f'local.{self.state.local_atual}')}",
            classes="titulo-tela",
        )
        yield Static("Antes de começar: veja como está o dia.",
                     classes="subtitulo-tela")
        with Horizontal():
            yield SceneCard(classes="painel", id="cena-plano")
            with Vertical(classes="painel"):
                yield WeatherCard(self.tr, id="clima-plano")
                yield Static("", id="plano-resumo")
        yield Static("", id="plano-dica", classes="aviso")
        with Horizontal(classes="linha-botoes"):
            yield Button("Bora trabalhar →", variant="success", id="ok")
        yield Footer()

    def on_mount(self) -> None:
        local = LOCAIS[self.state.local_atual]
        self.query_one(SceneCard).mostrar(
            self.state.local_atual, self.clima, "plano")
        self.query_one(WeatherCard).mostrar(self.clima)

        sabores = sabores_disponiveis(self.state.locais_desbloqueados)
        falta = max(0, local.meta_caixa - self.state.caixa)
        linhas = [
            f"[dim]No caixa[/]  [b]{money(self.state.caixa)}[/]",
            f"[dim]Meta[/]  {money(local.meta_caixa)}"
            + (f"  [dim](faltam {money(falta)})[/]" if falta else "  [green]batida![/]"),
            f"[dim]Sabores[/]  {len(sabores)}",
            f"[dim]Congelado[/]  {self.state.inventario.total_prontos()}",
        ]
        if self.state.local_atual != "casa" and self.state.isopor:
            linhas.append(
                f"[dim]Isopor[/]  aguenta mais {self.state.isopor_dias} dia(s)")
        self.query_one("#plano-resumo", Static).update("\n".join(linhas))

        self.query_one("#plano-dica", Static).update(
            _DICAS.get(self.state.local_atual, ""))
        self.query_one("#ok", Button).focus()

    def action_seguir(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self) -> None:
        self.dismiss(None)
