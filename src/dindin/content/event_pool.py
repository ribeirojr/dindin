"""Eventos aleatorios: globais e exclusivos de cada regiao."""

from ..sim.models import GameEvent
from ..sim.types import EventKind as EK

_E = (
    # --- Globais ---
    GameEvent("queda_energia", EK.PROBLEMA, 0.030, derrete_frac=0.55),
    GameEvent("freezer_pifou", EK.PROBLEMA, 0.012, derrete_frac=0.35, custo_extra=8000),
    GameEvent("fiscal", EK.PROBLEMA, 0.020, custo_extra=5000, locais=("praia", "carrinho")),
    GameEvent("saquinho_furado", EK.PROBLEMA, 0.025, derrete_frac=0.10),
    GameEvent("jogo_do_brasil", EK.SOCIAL, 0.030, trafego_mod=1.45),
    GameEvent("obra_na_rua", EK.PROBLEMA, 0.025, trafego_mod=0.55,
              locais=("isopor", "escola", "carrinho")),
    GameEvent("excursao", EK.SORTE, 0.030, trafego_mod=1.60, locais=("praia", "carrinho")),
    GameEvent("concorrente", EK.PROBLEMA, 0.040, trafego_mod=0.70),
    GameEvent("elogio_bairro", EK.SORTE, 0.035, trafego_mod=1.25),
    GameEvent("feira_promocao", EK.SORTE, 0.030, custo_extra=-2000),
    # --- Regionais ---
    GameEvent("seca_forte", EK.CLIMA, 0.045, trafego_mod=1.30, regioes=("ce",)),
    GameEvent("festa_padroeira", EK.SOCIAL, 0.035, trafego_mod=1.50, regioes=("ce",)),
    GameEvent("carnaval_bloco", EK.SOCIAL, 0.045, trafego_mod=1.65, regioes=("rj",)),
    GameEvent("temporal_carioca", EK.CLIMA, 0.040, trafego_mod=0.35, regioes=("rj",)),
    GameEvent("festa_junina_mg", EK.SOCIAL, 0.045, trafego_mod=1.45, regioes=("mg",)),
    GameEvent("quermesse", EK.SOCIAL, 0.035, trafego_mod=1.30, regioes=("mg",)),
    GameEvent("onda_calor_sp", EK.CLIMA, 0.040, trafego_mod=1.55, regioes=("sp",)),
    GameEvent("greve_transporte", EK.PROBLEMA, 0.035, trafego_mod=0.50, regioes=("sp",)),
    GameEvent("minuano", EK.CLIMA, 0.045, trafego_mod=0.45, regioes=("rs",)),
    GameEvent("semana_farroupilha", EK.SOCIAL, 0.035, trafego_mod=1.40, regioes=("rs",)),
    GameEvent("cirio_nazare", EK.SOCIAL, 0.040, trafego_mod=1.75, regioes=("pa",)),
    GameEvent("chuva_das_duas", EK.CLIMA, 0.055, trafego_mod=0.70, regioes=("pa",)),
    GameEvent("seca_do_cerrado", EK.CLIMA, 0.045, trafego_mod=1.35, regioes=("df",)),
    GameEvent("greve_servidor", EK.SOCIAL, 0.035, trafego_mod=1.20, regioes=("df",)),
)

EVENTOS: dict[str, GameEvent] = {e.key: e for e in _E}


def elegiveis(regiao: str, local: str) -> list[GameEvent]:
    return [e for e in _E
            if (not e.regioes or regiao in e.regioes)
            and (not e.locais or local in e.locais)]
