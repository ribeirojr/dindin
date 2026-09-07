"""Modal de desbloqueio de ponto novo."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

from ...content.locations import LOCAIS
from ...i18n import money


class ChapterUnlockScreen(ModalScreen[bool]):
    def __init__(self, tr, local_key: str, caixa: int) -> None:
        super().__init__()
        self.tr, self.local_key, self.caixa = tr, local_key, caixa

    def compose(self) -> ComposeResult:
        local = LOCAIS[self.local_key]
        pode = self.caixa >= local.custo_entrada
        with Vertical(id="caixa-modal"):
            yield Static(f"[b yellow]{self.tr.t('cap.desbloqueou')}[/]\n")
            yield Static(
                f"Agora dá pra vender em: [b]{self.tr.t(f'local.{self.local_key}')}[/]\n\n"
                f"[dim]Movimento:[/] {local.trafego_base} pessoas/dia\n"
                f"[dim]Cabe no ponto:[/] {local.capacidade} unidades\n"
                f"[dim]Custo fixo:[/] {money(local.custo_fixo_dia)}/dia\n"
                f"[dim]Gourmet vende:[/] {local.gourmet_afinidade:.2f}x\n\n"
                f"[b]{self.tr.t('cap.entrada')}: {money(local.custo_entrada)}[/]\n"
                f"[dim]Seu caixa:[/] {money(self.caixa)}\n"
            )
            if not pode:
                yield Static("[red]Ainda não dá pra pagar a entrada.[/]")
            with Horizontal(classes="linha-botoes"):
                yield Button("Mudar pra lá!", variant="success", id="sim",
                             disabled=not pode)
                yield Button("Fico aqui", id="nao")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "sim")
