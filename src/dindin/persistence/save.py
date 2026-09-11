"""Salvar e carregar o jogo em JSON."""

import json
from pathlib import Path

from ..sim.state import GameState, Inventory, Lote

VERSAO = 1


def caminho_padrao() -> Path:
    base = Path.home() / ".local" / "share" / "dindin"
    base.mkdir(parents=True, exist_ok=True)
    return base / "save.json"


def salvar(state: GameState, caminho: Path | None = None) -> Path:
    destino = caminho or caminho_padrao()
    dados = {
        "versao": VERSAO,
        "seed": state.seed,
        "regiao": state.regiao,
        "dia": state.dia,
        "caixa": state.caixa,
        "reputacao": state.reputacao,
        "local_atual": state.local_atual,
        "locais_desbloqueados": list(state.locais_desbloqueados),
        "capacidade_freezer": state.capacidade_freezer,
        "upgrades": sorted(state.upgrades),
        "vendas_recentes": dict(state.vendas_recentes),
        "socorro_usado": state.socorro_usado,
        "isopor": state.isopor,
        "isopor_dias": state.isopor_dias,
        "encerrado": state.encerrado,
        "inventario": {
            "ingredientes": {
                k: [[l.qtd, l.dia_validade] for l in lotes]
                for k, lotes in state.inventario.ingredientes.items()
            },
            "prontos": dict(state.inventario.prontos),
            "gelo_sacos": state.inventario.gelo_sacos,
        },
    }
    destino.write_text(json.dumps(dados, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    return destino


def carregar(caminho: Path | None = None) -> GameState | None:
    origem = caminho or caminho_padrao()
    if not origem.exists():
        return None
    dados = json.loads(origem.read_text(encoding="utf-8"))
    if dados.get("versao") != VERSAO:
        return None

    inv = Inventory(
        ingredientes={
            k: [Lote(qtd, val) for qtd, val in lotes]
            for k, lotes in dados["inventario"]["ingredientes"].items()
        },
        prontos=dict(dados["inventario"]["prontos"]),
        gelo_sacos=dados["inventario"]["gelo_sacos"],
    )
    return GameState(
        versao=VERSAO, seed=dados["seed"], regiao=dados["regiao"],
        dia=dados["dia"], caixa=dados["caixa"], reputacao=dados["reputacao"],
        local_atual=dados["local_atual"],
        locais_desbloqueados=list(dados["locais_desbloqueados"]),
        inventario=inv, capacidade_freezer=dados["capacidade_freezer"],
        upgrades=set(dados["upgrades"]),
        vendas_recentes=dict(dados.get("vendas_recentes", {})),
        # .get com default: saves antigos (sem estes campos) continuam validos.
        socorro_usado=bool(dados.get("socorro_usado", False)),
        isopor=dados.get("isopor"),
        isopor_dias=int(dados.get("isopor_dias", 0)),
        encerrado=dados.get("encerrado"),
    )
