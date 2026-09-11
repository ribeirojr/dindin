"""A lista MODULOS do pyodide-bridge.js nao pode divergir do fonte.

Quem cria um arquivo novo em sim/, content/ ou i18n/ precisa lembrar de
listar ele no JS -- senao a versao web quebra em runtime com "nao achei".
Este teste transforma o esquecimento em falha de CI.
"""

import re
from pathlib import Path

from tools.build_web import IGNORAR, IGNORAR_ARQUIVOS, ORIGEM

RAIZ = Path(__file__).resolve().parents[1]


def _modulos_do_js() -> set[str]:
    js = (RAIZ / "web" / "pyodide-bridge.js").read_text(encoding="utf-8")
    bloco = re.search(r"const MODULOS = \[(.*?)\];", js, re.S)
    assert bloco, "nao achei a lista MODULOS no pyodide-bridge.js"
    return set(re.findall(r'"([^"]+\.py)"', bloco.group(1)))


def _modulos_do_fonte() -> set[str]:
    achados = set()
    for p in ORIGEM.rglob("*.py"):
        rel = p.relative_to(ORIGEM)
        if set(rel.parts) & IGNORAR or rel.name in IGNORAR_ARQUIVOS:
            continue
        achados.add(rel.as_posix())
    return achados


def test_modulos_do_navegador_batem_com_o_fonte():
    js, fonte = _modulos_do_js(), _modulos_do_fonte()
    assert js == fonte, (
        f"faltando no pyodide-bridge.js: {sorted(fonte - js)}; "
        f"sobrando: {sorted(js - fonte)}"
    )
