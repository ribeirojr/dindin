"""Conquistas da campanha: quais regioes o jogador ja venceu.

Isso vive ACIMA de uma partida: um GameState morre no fim do jogo, a
conquista fica. Por isso nao e campo de GameState nem entra no save da
partida -- cada interface guarda esse conjunto do seu jeito (arquivo no
terminal, localStorage no navegador) e passa por aqui pra somar.

Puro de proposito: so recebe e devolve dados, nunca le nem escreve nada.
"""

from collections.abc import Iterable

from ..content.regions import ORDEM_REGIOES


def normalizar(chaves: Iterable[str] | None) -> set[str]:
    """Descarta o que nao e regiao conhecida (save velho, chave renomeada)."""
    if not chaves:
        return set()
    return {k for k in chaves if k in ORDEM_REGIOES}


def registrar_vitoria(conquistas: Iterable[str] | None, regiao: str) -> set[str]:
    """Marca a regiao como vencida. Nao muda o conjunto que entrou."""
    novas = normalizar(conquistas)
    if regiao in ORDEM_REGIOES:
        novas.add(regiao)
    return novas


def venceu_regiao(conquistas: Iterable[str] | None, regiao: str) -> bool:
    return regiao in normalizar(conquistas)


def total() -> int:
    return len(ORDEM_REGIOES)


def quantas(conquistas: Iterable[str] | None) -> int:
    return len(normalizar(conquistas))


def zerou_tudo(conquistas: Iterable[str] | None) -> bool:
    return quantas(conquistas) == total()


def pendentes(conquistas: Iterable[str] | None) -> list[str]:
    """Regioes que faltam, na ordem do jogo."""
    feitas = normalizar(conquistas)
    return [k for k in ORDEM_REGIOES if k not in feitas]
