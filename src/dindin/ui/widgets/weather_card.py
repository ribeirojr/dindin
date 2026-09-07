"""Cartao do clima com desenho em ASCII e dica de movimento."""

from textual.widgets import Static

from ...i18n import Translator
from ...sim.models import Weather
from ...sim.types import WeatherKind

_ARTE: dict[WeatherKind, tuple[str, str]] = {
    WeatherKind.ESCALDANTE: (r"\ | /   ", "yellow"),
    WeatherKind.QUENTE: (r" \|/    ", "yellow"),
    WeatherKind.ABAFADO: (r"~~~~    ", "orange1"),
    WeatherKind.NUBLADO: (r"(___)   ", "grey70"),
    WeatherKind.CHUVA: (r"(___) ' ", "blue"),
    WeatherKind.TEMPORAL: (r"(___) /_", "bright_blue"),
    WeatherKind.FRIO: (r" * * *  ", "cyan"),
}


class WeatherCard(Static):
    def __init__(self, tr: Translator, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tr = tr

    def mostrar(self, clima: Weather, titulo: str | None = None) -> None:
        arte, cor = _ARTE.get(clima.kind, ("        ", "white"))
        nome = self.tr.t(f"clima.{clima.kind.value}")
        cab = titulo or self.tr.t("ui.clima_amanha")
        dica = self._dica(clima)
        self.update(
            f"[dim]{cab}[/]\n[{cor}]{arte}[/] [b]{nome}[/]\n"
            f"{clima.temp_c:.0f}°C  (sensação {clima.heat_index:.0f}°C)\n{dica}"
        )

    def _dica(self, clima: Weather) -> str:
        if clima.kind in (WeatherKind.TEMPORAL, WeatherKind.CHUVA):
            return "[blue]Movimento fraco.[/]"
        if clima.kind is WeatherKind.FRIO:
            return "[cyan]Ninguém quer gelado.[/]"
        if clima.heat_index > 34:
            return "[yellow]Vai vender muito![/]"
        if clima.heat_index > 30:
            return "[green]Movimento bom.[/]"
        return "[dim]Movimento normal.[/]"
