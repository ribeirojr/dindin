"""Guarda as regioes ja vencidas, fora do save da partida.

O save.json guarda UMA partida e some quando ela acaba. A conquista e o
contrario: ela so existe depois que a partida acabou, e tem que durar.
Por isso mora em arquivo proprio.
"""

import json
from pathlib import Path

from ..sim import campaign

VERSAO = 1


def caminho_padrao() -> Path:
    base = Path.home() / ".local" / "share" / "dindin"
    base.mkdir(parents=True, exist_ok=True)
    return base / "conquistas.json"


def carregar(caminho: Path | None = None) -> set[str]:
    """Nunca levanta: arquivo faltando ou corrompido vira campanha zerada."""
    origem = caminho or caminho_padrao()
    try:
        dados = json.loads(origem.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    if not isinstance(dados, dict) or dados.get("versao") != VERSAO:
        return set()
    return campaign.normalizar(dados.get("regioes"))


def salvar(conquistas: set[str], caminho: Path | None = None) -> Path:
    destino = caminho or caminho_padrao()
    destino.write_text(
        json.dumps({"versao": VERSAO,
                    "regioes": sorted(campaign.normalizar(conquistas))},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return destino


def registrar_vitoria(regiao: str, caminho: Path | None = None) -> set[str]:
    """Le, soma a regiao e grava de volta. Devolve o conjunto novo."""
    novas = campaign.registrar_vitoria(carregar(caminho), regiao)
    salvar(novas, caminho)
    return novas
