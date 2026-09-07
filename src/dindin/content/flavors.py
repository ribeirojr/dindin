"""Catalogo de sabores. Receitas expressas por 10 unidades."""

from ..sim.models import Flavor
from ..sim.types import Tier

_F = (
    # --- SIMPLES ---
    Flavor("coco", "Coco", Tier.SIMPLES,
           {"polpa_comum": 0.40, "acucar": 0.22, "saquinho": 0.10}, 1.00, 200),
    Flavor("limao", "Limão", Tier.SIMPLES,
           {"polpa_comum": 0.34, "acucar": 0.24, "saquinho": 0.10}, 0.95, 200),
    Flavor("maracuja", "Maracujá", Tier.SIMPLES,
           {"polpa_comum": 0.42, "acucar": 0.26, "saquinho": 0.10}, 1.05, 200),
    Flavor("manga", "Manga", Tier.SIMPLES,
           {"polpa_comum": 0.44, "acucar": 0.20, "saquinho": 0.10}, 1.00, 200,
           desbloqueio="isopor"),
    Flavor("uva", "Uva", Tier.SIMPLES,
           {"polpa_comum": 0.40, "acucar": 0.24, "saquinho": 0.10}, 0.95, 200,
           desbloqueio="isopor"),
    Flavor("milho_verde", "Milho verde", Tier.SIMPLES,
           {"milho": 1.10, "acucar": 0.20, "leite_cond": 0.30, "saquinho": 0.10},
           1.00, 250, desbloqueio="isopor"),
    Flavor("caja", "Cajá", Tier.SIMPLES,
           {"polpa_comum": 0.42, "acucar": 0.26, "saquinho": 0.10}, 1.00, 220,
           desbloqueio="praia"),
    Flavor("pessego", "Pêssego", Tier.SIMPLES,
           {"polpa_comum": 0.42, "acucar": 0.22, "saquinho": 0.10}, 0.98, 220,
           desbloqueio="praia"),
    Flavor("jabuticaba", "Jabuticaba", Tier.SIMPLES,
           {"polpa_comum": 0.44, "acucar": 0.24, "saquinho": 0.10}, 1.00, 240,
           desbloqueio="escola"),
    # --- GOURMET (desbloqueiam mais tarde) ---
    Flavor("acai", "Açaí com leite condensado", Tier.GOURMET,
           {"polpa_premium": 0.50, "leite_cond": 0.55, "saquinho": 0.10},
           1.10, 400, desbloqueio="isopor"),
    Flavor("cupuacu", "Cupuaçu cremoso", Tier.GOURMET,
           {"polpa_premium": 0.48, "leite_cond": 0.50, "saquinho": 0.10},
           1.08, 450, desbloqueio="isopor"),
    Flavor("morango", "Morango cremoso", Tier.GOURMET,
           {"polpa_comum": 0.45, "leite_cond": 0.55, "leite_po": 0.10, "saquinho": 0.10},
           1.05, 450, desbloqueio="isopor"),
    Flavor("doce_leite", "Doce de leite", Tier.GOURMET,
           {"leite_cond": 0.90, "leite_po": 0.10, "saquinho": 0.10},
           1.05, 450, desbloqueio="praia"),
    Flavor("tapioca", "Tapioca cremosa", Tier.GOURMET,
           {"polpa_comum": 0.30, "leite_cond": 0.55, "leite_po": 0.12, "saquinho": 0.10},
           1.05, 450, desbloqueio="praia"),
    Flavor("bacuri", "Bacuri", Tier.GOURMET,
           {"polpa_premium": 0.52, "leite_cond": 0.50, "saquinho": 0.10},
           1.10, 480, desbloqueio="praia"),
    Flavor("taperreba", "Taperebá", Tier.GOURMET,
           {"polpa_premium": 0.48, "leite_cond": 0.45, "saquinho": 0.10},
           1.05, 450, desbloqueio="praia"),
    Flavor("ninho_nutella", "Ninho com Nutella", Tier.GOURMET,
           {"leite_po": 0.22, "creme_avela": 0.30, "leite_cond": 0.40, "saquinho": 0.10},
           1.20, 550, desbloqueio="escola"),
)

SABORES: dict[str, Flavor] = {f.key: f for f in _F}


def sabores_disponiveis(desbloqueados: list[str]) -> list[Flavor]:
    liberados = set(desbloqueados)
    return [f for f in _F if f.desbloqueio is None or f.desbloqueio in liberados]
