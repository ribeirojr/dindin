"""Copia a camada portavel do jogo pro diretorio web/py.

Roda antes de servir o site. Sim/, content/ e i18n/ vao INTACTOS -- e esse
o ponto do porte: o navegador roda o mesmo codigo que os testes conferem.
"""

import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "src" / "dindin"
DESTINO = RAIZ / "web" / "py"

# ui/ e persistence/ ficam de fora: Textual nao roda no navegador e
# salvar em arquivo vira localStorage no lado JS.
IGNORAR = {"ui", "persistence", "__pycache__"}
IGNORAR_ARQUIVOS = {"__main__.py"}


def main() -> int:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    DESTINO.mkdir(parents=True)

    copiados = []
    for caminho in sorted(ORIGEM.rglob("*.py")):
        rel = caminho.relative_to(ORIGEM)
        if set(rel.parts) & IGNORAR or rel.name in IGNORAR_ARQUIVOS:
            continue
        alvo = DESTINO / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(caminho, alvo)
        copiados.append(rel)

    linhas = sum(len(p.read_text(encoding="utf-8").splitlines())
                 for p in DESTINO.rglob("*.py"))
    print(f"{len(copiados)} modulos -> web/py ({linhas} linhas)")
    for rel in copiados:
        print(f"  {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
