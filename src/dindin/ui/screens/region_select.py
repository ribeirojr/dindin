"""Escolha do estado. Muda o vocabulario E a economia do jogo."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, OptionList, Static
from textual.widgets.option_list import Option

from ...content.flavors import SABORES
from ...content.regions import ORDEM_REGIOES, REGIOES
from ...i18n import Translator
from ...persistence import conquistas as conquistas_salvas
from ...sim import campaign

_DIFICULDADE = {"ce": 2, "rj": 2, "mg": 3, "sp": 3, "rs": 4, "pa": 2, "df": 3}
_CLIMA_TXT = {
    "ce": "Calor o ano inteiro, quase nunca chove.",
    "rj": "Quente, mas o temporal chega sem avisar.",
    "mg": "Clima ameno, inverno atrapalha as vendas.",
    "sp": "Instável: quatro estações num dia só.",
    "rs": "Verão forte, inverno congela as vendas.",
    "pa": "Calor e a chuva das duas, todo santo dia.",
    "df": "Verão chuvoso, mas o inverno é seco de rachar.",
}


class RegionSelectScreen(Screen[str]):
    BINDINGS = [("escape", "app.pop_screen", "Voltar")]

    def __init__(self) -> None:
        super().__init__()
        self.conquistas = conquistas_salvas.carregar()

    def compose(self) -> ComposeResult:
        feitas = campaign.quantas(self.conquistas)
        total = campaign.total()
        sub = "Cada estado tem seu nome pro doce, seu clima e seu gosto."
        if feitas:
            sub += (f"  [green]★ {feitas} de {total} vencidas.[/]"
                    if not campaign.zerou_tudo(self.conquistas)
                    else "  [yellow]★ Brasil inteiro vencido![/]")
        yield Static("De onde você é?", classes="titulo-tela")
        yield Static(sub, classes="subtitulo-tela")
        with Horizontal():
            yield OptionList(
                *[Option(self._rotulo(k), id=k) for k in ORDEM_REGIOES],
                id="lista-regioes",
            )
            with Vertical(id="preview-regiao"):
                yield Static("", id="preview-texto")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(OptionList).focus()
        self._preview(ORDEM_REGIOES[0])

    def _rotulo(self, key: str) -> str:
        """Marca no proprio item da lista o que ja foi vencido."""
        if campaign.venceu_regiao(self.conquistas, key):
            return f"[green]✓[/] {REGIOES[key].nome}"
        return f"  {REGIOES[key].nome}"

    def _preview(self, key: str) -> None:
        regiao = REGIOES[key]
        tr = Translator(key)
        favoritos = sorted(regiao.preferencia.items(), key=lambda kv: -kv[1])[:3]
        nomes = ", ".join(SABORES[k].nome for k, _ in favoritos if k in SABORES)
        estrelas = "★" * _DIFICULDADE[key] + "☆" * (5 - _DIFICULDADE[key])
        selo = ("  [green]✓ vencida[/]"
                if campaign.venceu_regiao(self.conquistas, key) else "")
        self.query_one("#preview-texto", Static).update(
            f"[b yellow]{regiao.nome}[/]  ([i]{regiao.gentilico}[/]){selo}\n\n"
            f"Aqui o doce se chama [b]{tr.produto}[/].\n\n"
            f"[dim]Gíria:[/] {tr.t('interj.surpresa')}, {tr.t('interj.positivo')}, "
            f"{tr.t('vocativo')}\n\n"
            f"[dim]Clima:[/] {_CLIMA_TXT[key]}\n\n"
            f"[dim]Sabor que mais sai:[/] {nomes}\n\n"
            f"[dim]Preço que o povo aceita:[/] {regiao.tolerancia_preco:.2f}x\n"
            f"[dim]Custo dos insumos:[/] {regiao.custo_insumo_mod:.2f}x\n\n"
            f"[dim]Dificuldade:[/] [yellow]{estrelas}[/]"
        )

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        if event.option.id:
            self._preview(event.option.id)

    def on_option_list_option_selected(
        self, event: OptionList.OptionSelected
    ) -> None:
        if event.option.id:
            self.dismiss(event.option.id)
