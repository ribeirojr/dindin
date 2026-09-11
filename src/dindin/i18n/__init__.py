"""Tradutor regional. A camada sim/ nunca chama t(): ela devolve chaves."""

import importlib
from random import Random

from .barks import pool
from .base_en import BASE_EN, OVERRIDES_EN
from .base_ptbr import BASE

REGIOES_I18N = ("ce", "rj", "mg", "sp", "rs", "pa")
IDIOMAS = ("pt", "en")


def carregar_override(regiao: str) -> dict[str, str]:
    try:
        mod = importlib.import_module(f".overrides.{regiao}", __package__)
    except ModuleNotFoundError:
        return {}
    return dict(getattr(mod, "OVERRIDE", {}))


class Translator:
    """Resolve override regional -> base do idioma -> base pt -> marcador.

    Em ingles so a interface muda: nome do produto (dindin, sacole...) e
    girias sao fala de rua/nome proprio e continuam em portugues.
    """

    def __init__(self, regiao: str, lang: str = "pt") -> None:
        self.regiao = regiao
        self.lang = lang if lang in IDIOMAS else "pt"
        self._base = BASE
        if self.lang == "en":
            self._cadeia = (OVERRIDES_EN.get(regiao, {}), BASE_EN, BASE)
        else:
            self._cadeia = (carregar_override(regiao), BASE)

    def t(self, key: str, /, **kw: object) -> str:
        tpl = None
        for camada in self._cadeia:
            tpl = camada.get(key)
            if tpl:
                break
        if tpl is None:
            return f"⟨missing:{key}⟩"
        if not kw:
            return tpl
        try:
            return tpl.format(**kw)
        except (KeyError, IndexError):
            return tpl

    def bark(self, tag: str, rng: Random) -> str:
        opcoes = pool(self.regiao, tag, self.lang)
        return rng.choice(opcoes) if opcoes else ""

    @property
    def produto(self) -> str:
        return self.t("produto.sing")

    @property
    def produtos(self) -> str:
        return self.t("produto.plur")


def money(centavos: int) -> str:
    """Formata em real, com separadores brasileiros."""
    sinal = "-" if centavos < 0 else ""
    v = abs(centavos)
    inteiro, cent = divmod(v, 100)
    milhar = f"{inteiro:,}".replace(",", ".")
    return f"{sinal}R$ {milhar},{cent:02d}"
