"""Ajuda, no vocabulario da regiao escolhida."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class HelpScreen(ModalScreen[None]):
    BINDINGS = [("escape", "dismiss", "Fechar")]

    def __init__(self, tr) -> None:
        super().__init__()
        self.tr = tr

    def compose(self) -> ComposeResult:
        p, ps = self.tr.produto, self.tr.t("produto.plur")
        with Vertical(id="caixa-modal"):
            yield Static(
                f"[b yellow]Como se joga[/]\n\n"
                f"Todo dia você repete quatro passos:\n\n"
                f"[b]1. Feira[/] — compra polpa, açúcar e saquinho.\n"
                f"   Comprando em quantidade, sai mais barato.\n\n"
                f"[b]2. Cozinha[/] — decide quantos {ps} vai fazer.\n"
                f"   Cuidado: o que passar da capacidade do freezer derrete.\n\n"
                f"[b]3. Preço[/] — o termômetro mostra o que o povo acha.\n"
                f"   Barato vende muito e ganha pouco. Caro é o contrário.\n"
                f"   Em dia de calor, dá pra cobrar mais.\n\n"
                f"[b]4. Vender[/] — o dia acontece e sai o relatório.\n\n"
                f"[b yellow]O segredo:[/] olhe a coluna [b]'queriam comprar'[/].\n"
                f"Se ela for maior que o que você levou, faltou {p} —\n"
                f"faça mais amanhã. Se sobrou, você fez demais.\n\n"
                f"O clima manda em tudo: calor vende, chuva mata a venda.\n"
                f"Fora de casa, o gelo do isopor entra sozinho nos custos do dia.\n"
                f"Bata a meta do capítulo pra liberar um ponto melhor.\n"
            )
            yield Button("Entendi", variant="success", id="ok")

    def on_button_pressed(self) -> None:
        self.dismiss(None)

    def action_dismiss(self) -> None:
        self.dismiss(None)
