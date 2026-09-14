"""As 6 regioes jogaveis. Cada uma muda vocabulario E economia."""

from ..sim.models import Region
from ..sim.types import Season, WeatherKind as W

_VERAO_NORDESTE = {W.ESCALDANTE: 0.30, W.QUENTE: 0.38, W.ABAFADO: 0.18,
                   W.NUBLADO: 0.08, W.CHUVA: 0.05, W.TEMPORAL: 0.01, W.FRIO: 0.00}
_INVERNO_NORDESTE = {W.ESCALDANTE: 0.10, W.QUENTE: 0.34, W.ABAFADO: 0.20,
                     W.NUBLADO: 0.20, W.CHUVA: 0.14, W.TEMPORAL: 0.02, W.FRIO: 0.00}

CEARA = Region(
    key="ce", nome="Ceará", gentilico="cearense", capital="Fortaleza",
    clima={Season.VERAO: _VERAO_NORDESTE, Season.OUTONO: _VERAO_NORDESTE,
           Season.INVERNO: _INVERNO_NORDESTE, Season.PRIMAVERA: _VERAO_NORDESTE},
    base_temp_c=(29.0, 35.0),
    preferencia={"coco": 1.45, "caja": 1.35, "tapioca": 1.30, "manga": 1.15,
                 "ninho_nutella": 0.80, "uva": 0.85},
    tolerancia_preco=0.94, custo_insumo_mod=0.95,
    eventos_exclusivos=("seca_forte", "festa_padroeira"),
)

RIO = Region(
    key="rj", nome="Rio de Janeiro", gentilico="carioca", capital="Rio de Janeiro",
    clima={Season.VERAO: {W.ESCALDANTE: 0.26, W.QUENTE: 0.32, W.ABAFADO: 0.20,
                          W.NUBLADO: 0.09, W.CHUVA: 0.08, W.TEMPORAL: 0.05, W.FRIO: 0.00},
           Season.OUTONO: {W.ESCALDANTE: 0.12, W.QUENTE: 0.30, W.ABAFADO: 0.20,
                           W.NUBLADO: 0.20, W.CHUVA: 0.13, W.TEMPORAL: 0.04, W.FRIO: 0.01},
           Season.INVERNO: {W.ESCALDANTE: 0.04, W.QUENTE: 0.22, W.ABAFADO: 0.14,
                            W.NUBLADO: 0.28, W.CHUVA: 0.20, W.TEMPORAL: 0.04, W.FRIO: 0.08},
           Season.PRIMAVERA: {W.ESCALDANTE: 0.16, W.QUENTE: 0.32, W.ABAFADO: 0.18,
                              W.NUBLADO: 0.16, W.CHUVA: 0.12, W.TEMPORAL: 0.05, W.FRIO: 0.01}},
    base_temp_c=(26.0, 34.0),
    preferencia={"coco": 1.40, "limao": 1.25, "maracuja": 1.20, "acai": 1.10,
                 "milho_verde": 0.80},
    tolerancia_preco=1.12, custo_insumo_mod=1.10,
    eventos_exclusivos=("carnaval_bloco", "temporal_carioca"),
)

MINAS = Region(
    key="mg", nome="Minas Gerais", gentilico="mineiro", capital="Belo Horizonte",
    clima={Season.VERAO: {W.ESCALDANTE: 0.12, W.QUENTE: 0.34, W.ABAFADO: 0.16,
                          W.NUBLADO: 0.20, W.CHUVA: 0.14, W.TEMPORAL: 0.04, W.FRIO: 0.00},
           Season.OUTONO: {W.ESCALDANTE: 0.05, W.QUENTE: 0.26, W.ABAFADO: 0.12,
                           W.NUBLADO: 0.30, W.CHUVA: 0.16, W.TEMPORAL: 0.03, W.FRIO: 0.08},
           Season.INVERNO: {W.ESCALDANTE: 0.01, W.QUENTE: 0.14, W.ABAFADO: 0.08,
                            W.NUBLADO: 0.30, W.CHUVA: 0.12, W.TEMPORAL: 0.02, W.FRIO: 0.33},
           Season.PRIMAVERA: {W.ESCALDANTE: 0.08, W.QUENTE: 0.30, W.ABAFADO: 0.14,
                              W.NUBLADO: 0.24, W.CHUVA: 0.16, W.TEMPORAL: 0.04, W.FRIO: 0.04}},
    base_temp_c=(22.0, 30.0),
    preferencia={"milho_verde": 1.55, "doce_leite": 1.35, "jabuticaba": 1.30,
                 "morango": 1.15, "coco": 0.90, "acai": 0.80},
    tolerancia_preco=0.97, custo_insumo_mod=0.90,
    eventos_exclusivos=("festa_junina_mg", "quermesse"),
)

SAO_PAULO = Region(
    key="sp", nome="São Paulo", gentilico="paulista", capital="São Paulo",
    clima={Season.VERAO: {W.ESCALDANTE: 0.16, W.QUENTE: 0.30, W.ABAFADO: 0.18,
                          W.NUBLADO: 0.16, W.CHUVA: 0.14, W.TEMPORAL: 0.06, W.FRIO: 0.00},
           Season.OUTONO: {W.ESCALDANTE: 0.06, W.QUENTE: 0.24, W.ABAFADO: 0.14,
                           W.NUBLADO: 0.28, W.CHUVA: 0.18, W.TEMPORAL: 0.04, W.FRIO: 0.06},
           Season.INVERNO: {W.ESCALDANTE: 0.02, W.QUENTE: 0.16, W.ABAFADO: 0.10,
                            W.NUBLADO: 0.32, W.CHUVA: 0.14, W.TEMPORAL: 0.02, W.FRIO: 0.24},
           Season.PRIMAVERA: {W.ESCALDANTE: 0.10, W.QUENTE: 0.28, W.ABAFADO: 0.16,
                              W.NUBLADO: 0.22, W.CHUVA: 0.16, W.TEMPORAL: 0.05, W.FRIO: 0.03}},
    base_temp_c=(20.0, 31.0),
    preferencia={"ninho_nutella": 1.45, "morango": 1.25, "acai": 1.15,
                 "doce_leite": 1.10, "milho_verde": 0.85},
    tolerancia_preco=1.20, custo_insumo_mod=1.15,
    eventos_exclusivos=("onda_calor_sp", "greve_transporte"),
)

RIO_GRANDE = Region(
    key="rs", nome="Rio Grande do Sul", gentilico="gaúcho", capital="Porto Alegre",
    clima={Season.VERAO: {W.ESCALDANTE: 0.22, W.QUENTE: 0.34, W.ABAFADO: 0.16,
                          W.NUBLADO: 0.14, W.CHUVA: 0.10, W.TEMPORAL: 0.04, W.FRIO: 0.00},
           Season.OUTONO: {W.ESCALDANTE: 0.04, W.QUENTE: 0.20, W.ABAFADO: 0.10,
                           W.NUBLADO: 0.28, W.CHUVA: 0.18, W.TEMPORAL: 0.04, W.FRIO: 0.16},
           Season.INVERNO: {W.ESCALDANTE: 0.00, W.QUENTE: 0.06, W.ABAFADO: 0.04,
                            W.NUBLADO: 0.24, W.CHUVA: 0.16, W.TEMPORAL: 0.04, W.FRIO: 0.46},
           Season.PRIMAVERA: {W.ESCALDANTE: 0.08, W.QUENTE: 0.26, W.ABAFADO: 0.12,
                              W.NUBLADO: 0.24, W.CHUVA: 0.16, W.TEMPORAL: 0.06, W.FRIO: 0.08}},
    base_temp_c=(17.0, 32.0),
    preferencia={"uva": 1.35, "pessego": 1.30, "doce_leite": 1.20,
                 "morango": 1.10, "acai": 0.75, "coco": 0.85},
    tolerancia_preco=1.04, custo_insumo_mod=1.00,
    eventos_exclusivos=("minuano", "semana_farroupilha"),
)

PARA = Region(
    key="pa", nome="Pará", gentilico="paraense", capital="Belém",
    clima={Season.VERAO: {W.ESCALDANTE: 0.24, W.QUENTE: 0.30, W.ABAFADO: 0.22,
                          W.NUBLADO: 0.08, W.CHUVA: 0.14, W.TEMPORAL: 0.02, W.FRIO: 0.00},
           Season.OUTONO: {W.ESCALDANTE: 0.18, W.QUENTE: 0.26, W.ABAFADO: 0.22,
                           W.NUBLADO: 0.10, W.CHUVA: 0.20, W.TEMPORAL: 0.04, W.FRIO: 0.00},
           Season.INVERNO: {W.ESCALDANTE: 0.14, W.QUENTE: 0.24, W.ABAFADO: 0.22,
                            W.NUBLADO: 0.12, W.CHUVA: 0.24, W.TEMPORAL: 0.04, W.FRIO: 0.00},
           Season.PRIMAVERA: {W.ESCALDANTE: 0.20, W.QUENTE: 0.28, W.ABAFADO: 0.22,
                              W.NUBLADO: 0.10, W.CHUVA: 0.18, W.TEMPORAL: 0.02, W.FRIO: 0.00}},
    base_temp_c=(28.0, 34.0),
    preferencia={"acai": 1.70, "cupuacu": 1.55, "bacuri": 1.40, "taperreba": 1.30,
                 "coco": 1.05, "uva": 0.80, "morango": 0.85},
    tolerancia_preco=0.95, custo_insumo_mod=0.85,
    eventos_exclusivos=("cirio_nazare", "chuva_das_duas"),
)

BRASILIA = Region(
    key="df", nome="Distrito Federal", gentilico="brasiliense", capital="Brasília",
    # Cerrado: verao chuvoso (out-abr) e um inverno seco de rachar --
    # meses a fio sem chuva, umidade baixissima, calor seco o dia inteiro.
    clima={Season.VERAO: {W.ESCALDANTE: 0.14, W.QUENTE: 0.32, W.ABAFADO: 0.16,
                          W.NUBLADO: 0.14, W.CHUVA: 0.18, W.TEMPORAL: 0.06, W.FRIO: 0.00},
           Season.OUTONO: {W.ESCALDANTE: 0.18, W.QUENTE: 0.34, W.ABAFADO: 0.10,
                           W.NUBLADO: 0.16, W.CHUVA: 0.14, W.TEMPORAL: 0.04, W.FRIO: 0.04},
           Season.INVERNO: {W.ESCALDANTE: 0.30, W.QUENTE: 0.38, W.ABAFADO: 0.04,
                            W.NUBLADO: 0.16, W.CHUVA: 0.01, W.TEMPORAL: 0.00, W.FRIO: 0.11},
           Season.PRIMAVERA: {W.ESCALDANTE: 0.20, W.QUENTE: 0.32, W.ABAFADO: 0.12,
                              W.NUBLADO: 0.14, W.CHUVA: 0.16, W.TEMPORAL: 0.06, W.FRIO: 0.00}},
    base_temp_c=(24.0, 32.0),
    preferencia={"manga": 1.40, "milho_verde": 1.30, "caja": 1.20, "coco": 1.05,
                 "acai": 0.90, "bacuri": 0.75},
    tolerancia_preco=1.08, custo_insumo_mod=1.05,
    eventos_exclusivos=("seca_do_cerrado", "greve_servidor"),
)

REGIOES: dict[str, Region] = {r.key: r for r in
                              (CEARA, RIO, MINAS, SAO_PAULO, RIO_GRANDE, PARA, BRASILIA)}
ORDEM_REGIOES = ("ce", "rj", "mg", "sp", "rs", "pa", "df")
