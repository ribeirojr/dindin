"""Os 5 capitulos da campanha. Cada um e um problema diferente."""

from ..sim.models import Location, Upgrade

_L = (
    Location("casa", "Freezer de casa", 1, meta_caixa=15000, custo_entrada=0,
             trafego_base=45, tolerancia_mod=0.90, sensibilidade_clima=0.55,
             chuva_mod=0.85, capacidade=60, custo_fixo_dia=0, gourmet_afinidade=0.70),
    Location("isopor", "Isopor na rua", 2, meta_caixa=40000, custo_entrada=2000,
             trafego_base=110, tolerancia_mod=1.00, sensibilidade_clima=1.00,
             chuva_mod=0.40, capacidade=100, custo_fixo_dia=300, gourmet_afinidade=0.85),
    Location("praia", "Praia / orla", 3, meta_caixa=100000, custo_entrada=10000,
             trafego_base=260, tolerancia_mod=1.20, sensibilidade_clima=1.25,
             chuva_mod=0.15, capacidade=150, custo_fixo_dia=1200, gourmet_afinidade=1.35),
    Location("escola", "Portão da escola", 4, meta_caixa=200000, custo_entrada=10000,
             trafego_base=190, tolerancia_mod=0.80, sensibilidade_clima=0.70,
             chuva_mod=0.60, capacidade=130, custo_fixo_dia=800, gourmet_afinidade=0.55,
             escala_semana_escolar=True),
    Location("carrinho", "Carrinho próprio", 5, meta_caixa=500000, custo_entrada=120000,
             trafego_base=340, tolerancia_mod=1.10, sensibilidade_clima=1.05,
             chuva_mod=0.45, capacidade=260, custo_fixo_dia=2500, gourmet_afinidade=1.20),
)

LOCAIS: dict[str, Location] = {l.key: l for l in _L}
ORDEM_LOCAIS = tuple(l.key for l in _L)

_U = (
    Upgrade("freezer_maior", "Freezer maior", 45000, "praia",
            "+120 de capacidade de estoque congelado"),
    Upgrade("gerador", "Gerador", 70000, "praia",
            "Imune a queda de energia"),
    Upgrade("isopor_termico", "Isopor térmico bom", 18000, "isopor",
            "Reduz pela metade o derretimento"),
    Upgrade("banner", "Placa / banner", 12000, "isopor",
            "+8% de movimento"),
    Upgrade("ajudante", "Ajudante", 0, "praia",
            "+40 de capacidade por dia (custa R$15/dia)"),
)

UPGRADES: dict[str, Upgrade] = {u.key: u for u in _U}
CUSTO_AJUDANTE_DIA = 1500
BONUS_FREEZER_MAIOR = 120
BONUS_AJUDANTE_CAPACIDADE = 40
