"""A camada sim/ nunca pode importar textual ou rich."""

import ast
from pathlib import Path

SIM = Path(__file__).resolve().parents[2] / "src" / "dindin" / "sim"


def test_sim_nao_importa_textual():
    for path in SIM.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        nomes: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                nomes.add(node.module or "")
            elif isinstance(node, ast.Import):
                nomes.update(a.name for a in node.names)
        proibidos = [m for m in nomes if m.startswith(("textual", "rich"))]
        assert not proibidos, f"{path.name} importa {proibidos}"
