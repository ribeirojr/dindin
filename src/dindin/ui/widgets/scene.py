"""Desenho do ponto de venda. Da cara ao lugar onde a pessoa trabalha.

Duas versoes de cada cena: 'plano' (antes de vender, o ponto vazio) e
'venda' (o dia rolando, com gente). Ver o lugar mudar de freezer de casa
pra carrinho proprio e a recompensa visual da campanha.
"""

from textual.widgets import Static

from ...sim.types import WeatherKind

CENAS: dict[str, dict[str, str]] = {
    "casa": {
        "plano": r"""
        ┌───────────────┐
        │  ▄▄▄▄▄▄▄▄▄▄▄  │
        │  █ FREEZER █  │
        │  █ ░░░░░░░ █  │
        │  ▀▀▀▀▀▀▀▀▀▀▀  │
        │   cozinha     │
        └───────────────┘
""",
        "venda": r"""
        ┌───────────────┐
        │  ▄▄▄▄▄▄▄▄▄▄▄  │
        │  █ FREEZER █   o/
        │  █ ▓▓▓▓▓▓▓ █  /|
        │  ▀▀▀▀▀▀▀▀▀▀▀  / \
        │  "vizinha!"   │
        └───────────────┘
""",
    },
    "isopor": {
        "plano": r"""
           ___________
          /  ISOPOR  /|
         /__________/ |
         |░░░░░░░░░| /
         |_________|/
        ─────────────────
           calçada
""",
        "venda": r"""
      o/   ___________   \o
      /|  /  ISOPOR  /|   |\
      / \/__________/ |   / \
        |▓▓▓▓▓▓▓▓▓|  /
        |_________|/     "me vê um!"
     ─────────────────────────
""",
    },
    "praia": {
        "plano": r"""
      ~  ~   ~   ~   ~  ~
    ~~~~~~~~~~~~~~~~~~~~~~~
       ___________
      /  ISOPOR  /|    __
     /__________/ |   /  \
     |░░░░░░░░░| /   |    |
     |_________|/     areia
""",
        "venda": r"""
      ~  ~   ~   ~   ~  ~
    ~~~~~~~~~~~~~~~~~~~~~~~
   o/  ___________   \o  o/
   /| /  ISOPOR  /|   |\  |\
   /\/__________/ |   /\  /\
     |▓▓▓▓▓▓▓▓▓| /  "tá gelado?"
     |_________|/
""",
    },
    "escola": {
        "plano": r"""
     ╔═══════════════════╗
     ║  ESCOLA MUNICIPAL ║
     ╚═══════════════════╝
       ▌▌▌ portão ▌▌▌
        ___________
       /  ISOPOR  /|
      /__________/ |
""",
        "venda": r"""
     ╔═══════════════════╗
     ║  ESCOLA MUNICIPAL ║
     ╚═══════════════════╝
      ▌▌▌ portão ▌▌▌
   o/ o/ o/  ___________
   /| /| /| /  ISOPOR  /|
   /\ /\ /\/__________/ |
      "professora, um!"
""",
    },
    "carrinho": {
        "plano": r"""
        ╔═══════════════════╗
        ║   ★  DINDIN  ★    ║
        ╠═══════════════════╣
        ║ ░░░░░░░░░░░░░░░░░ ║
        ╚═══════════════════╝
           ◯           ◯
""",
        "venda": r"""
     o/ ╔═══════════════════╗ \o
     /| ║   ★  DINDIN  ★    ║  |\
     /\ ╠═══════════════════╣  /\
        ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ║
        ╚═══════════════════╝
           ◯           ◯
""",
    },
}

_CEU: dict[WeatherKind, tuple[str, str]] = {
    WeatherKind.ESCALDANTE: (r"    \ | /      ", "bright_yellow"),
    WeatherKind.QUENTE: (r"     \|/       ", "yellow"),
    WeatherKind.ABAFADO: (r"   ~~~~~~~     ", "orange1"),
    WeatherKind.NUBLADO: (r"   (~~~~~)     ", "grey70"),
    WeatherKind.CHUVA: (r"  (~~~~~) ' '  ", "blue"),
    WeatherKind.TEMPORAL: (r"  (~~~~~)/'/'  ", "bright_blue"),
    WeatherKind.FRIO: (r"    * * * *    ", "cyan"),
}

_COR_PONTO = {
    "casa": "grey70", "isopor": "orange1", "praia": "yellow",
    "escola": "cyan", "carrinho": "magenta",
}


class SceneCard(Static):
    """Desenho do ponto. modo='plano' antes de vender, 'venda' durante."""

    def mostrar(self, local: str, clima=None, modo: str = "plano") -> None:
        cena = CENAS.get(local, CENAS["casa"]).get(modo, "")
        cor = _COR_PONTO.get(local, "white")

        topo = ""
        if clima is not None:
            arte, cor_ceu = _CEU.get(clima.kind, ("", "white"))
            topo = f"[{cor_ceu}]{arte}[/]\n"

        self.update(f"{topo}[{cor}]{cena}[/]")
