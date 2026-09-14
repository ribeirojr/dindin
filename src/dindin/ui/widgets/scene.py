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

# Excecoes por regiao: mesmo capitulo, outro lugar. Nem toda capital tem
# praia de mar -- cada uma dessas ganha uma cena propria (ver local.praia
# no i18n pra cada override de nome/texto):
#   df: Esplanada dos Ministerios (sem litoral, capital planejada)
#   mg: Lagoa da Pampulha (Belo Horizonte e mineira do interior)
#   rs: Orla do Guaiba (Porto Alegre fica no rio/lago, nao no litoral)
#   pa: Ver-o-Peso (Belem fica na Baia do Guajara, estuario de rio)
CENAS_REGIAO: dict[str, dict[str, dict[str, str]]] = {
    "df": {
        "praia": {
            "plano": r"""
    ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄
    █ ▓ █  █ ▓ █  █ ▓ █  █ ▓ █    ___________
    █ ▓ █  █ ▓ █  █ ▓ █  █ ▓ █   /  ISOPOR  /|
    ▔▔▔▔▔  ▔▔▔▔▔  ▔▔▔▔▔  ▔▔▔▔▔  /__________/ |
   ─────────────────────────────|░░░░░░░░░| /
         esplanada               |_________|/
""",
            "venda": r"""
    ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄
    █ ▓ █  █ ▓ █  █ ▓ █  █ ▓ █  o/  ___________
    █ ▓ █  █ ▓ █  █ ▓ █  █ ▓ █  /| /  ISOPOR  /|
    ▔▔▔▔▔  ▔▔▔▔▔  ▔▔▔▔▔  ▔▔▔▔▔  / \/__________/ |
   ───────────────────────────────|▓▓▓▓▓▓▓▓▓| /  "um geladim!"
                                   |_________|/
""",
        },
    },
    "mg": {
        "praia": {
            "plano": r"""
        .-~"~-.        ___
       (  igreja )    /   \    ___________
        `-.___.-'    | lago|  /  ISOPOR  /|
   ~~~~~~~~~~~~~~~~~~~`---'~~/__________/ |
        pampulha              |░░░░░░░░░| /
                               |_________|/
""",
            "venda": r"""
        .-~"~-.        ___
       (  igreja )    /   \  o/  ___________
        `-.___.-'    | lago|  /| /  ISOPOR  /|
   ~~~~~~~~~~~~~~~~~~~`---'~~ / \/__________/ |
                               |▓▓▓▓▓▓▓▓▓| /  "um trem bão!"
                               |_________|/
""",
        },
    },
    "rs": {
        "praia": {
            "plano": r"""
       \   |   /        orla do guaíba
        \  |  /   ___________
     ────( sol )─/  ISOPOR  /|
    ~~~~~~~~~~~~/__________/ |
    ~~ guaíba ~~|░░░░░░░░░| /
   ~~~~~~~~~~~~~|_________|/
""",
            "venda": r"""
       \   |   /
        \  |  /   o/  ___________
     ────( sol )──/| /  ISOPOR  /|
    ~~~~~~~~~~~~~ / \/__________/ |
    ~~~~~~~~~~~~~~|▓▓▓▓▓▓▓▓▓| /  "bah, um gelinho, tchê!"
    ~~~~~~~~~~~~~~|_________|/
""",
        },
    },
    "pa": {
        "praia": {
            "plano": r"""
    ver-o-peso    ▲    ▲     ___________
    ═╦═   ═╦═    /█\  /█\   /  ISOPOR  /|
    ║barraca║   /___\/___\ /__________/ |
   ~~~~~~~~~~~~~~~~~~~~~~~~|░░░░░░░░░| /
   ~~ baía do guajará ~~~~~|_________|/
""",
            "venda": r"""
    ═╦═   ═╦═    ▲    ▲    o/  ___________
    ║barraca║   /█\  /█\   /| /  ISOPOR  /|
   ~~~~~~~~~~~ /___\/___\ / \/__________/ |
   ~~~~~~~~~~~~~~~~~~~~~~~~|▓▓▓▓▓▓▓▓▓| /  "égua, um chup-chup!"
   ~~~~~~~~~~~~~~~~~~~~~~~~|_________|/
""",
        },
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
_COR_PONTO_REGIAO = {
    "df": {"praia": "grey78"},        # concreto da Esplanada, nao sol de praia
    "mg": {"praia": "green3"},        # verde da lagoa e do gramado ao redor
    "rs": {"praia": "orange1"},       # por do sol na Orla, marca registrada
    "pa": {"praia": "dark_orange3"},  # barracas e madeira do Ver-o-Peso
}


class SceneCard(Static):
    """Desenho do ponto. modo='plano' antes de vender, 'venda' durante."""

    def mostrar(self, local: str, clima=None, modo: str = "plano",
                regiao: str | None = None) -> None:
        grupo_regiao = CENAS_REGIAO.get(regiao or "", {})
        cenas_local = grupo_regiao.get(local) or CENAS.get(local) or CENAS["casa"]
        cena = cenas_local.get(modo, "")
        cor = _COR_PONTO_REGIAO.get(regiao or "", {}).get(local) \
            or _COR_PONTO.get(local, "white")

        topo = ""
        if clima is not None:
            arte, cor_ceu = _CEU.get(clima.kind, ("", "white"))
            topo = f"[{cor_ceu}]{arte}[/]\n"

        self.update(f"{topo}[{cor}]{cena}[/]")
