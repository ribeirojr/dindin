"""Catalogo de insumos da feira. Precos em centavos, antes do modificador regional."""

from ..sim.models import Ingredient

# Insumo so aparece na feira quando o ponto que o usa esta liberado.
# Sem isso o dia 1 joga 8 insumos na cara de quem ainda nao sabe jogar.
DESBLOQUEIO_INSUMO: dict[str, str | None] = {
    "polpa_comum": None,      # desde o comeco
    "acucar": None,
    "saquinho": None,
    "milho": None,
    "leite_cond": "isopor",   # abre junto com os cremosos
    "polpa_premium": "isopor",
    "leite_po": "isopor",   # morango cremoso abre no isopor e usa leite em po
    "creme_avela": "escola",
    "gelo": "isopor",
}

_ING = (
    Ingredient("polpa_comum", "Polpa de fruta comum", "kg", 1200, 30, True,
               ((5, 0.92), (20, 0.84))),
    Ingredient("polpa_premium", "Polpa premium (açaí, cupuaçu)", "kg", 2200, 30, True,
               ((5, 0.90), (20, 0.82))),
    Ingredient("acucar", "Açúcar", "kg", 450, 365, False, ((10, 0.88),)),
    Ingredient("leite_cond", "Leite condensado", "lata", 650, 180, False, ((12, 0.85),)),
    Ingredient("leite_po", "Leite em pó", "kg", 3800, 180, False, ((3, 0.90),)),
    Ingredient("creme_avela", "Creme de avelã", "pote", 2400, 180, False, ((3, 0.92),)),
    Ingredient("milho", "Milho verde", "lata", 500, 365, False, ((12, 0.86),)),
    Ingredient("saquinho", "Saquinhos", "cento", 800, None, False,
               ((5, 0.85), (20, 0.75))),
    Ingredient("gelo", "Gelo", "saco 5kg", 800, 1, False, ((4, 0.90),)),
)

INSUMOS: dict[str, Ingredient] = {i.key: i for i in _ING}


def insumos_disponiveis(desbloqueados: list[str]) -> list[Ingredient]:
    """So mostra o que o jogador tem como usar hoje."""
    liberados = set(desbloqueados)
    return [i for i in _ING
            if i.key != "gelo"
            and (DESBLOQUEIO_INSUMO.get(i.key) is None
                 or DESBLOQUEIO_INSUMO[i.key] in liberados)]

# Um saco de gelo conserva ate 50 unidades por dia no isopor.
UNIDADES_POR_SACO_GELO = 50
