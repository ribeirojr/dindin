"""A formula de demanda: valores fixos e propriedades."""

import math

import pytest

from dindin.content.flavors import SABORES
from dindin.content.locations import LOCAIS
from dindin.content.regions import REGIOES
from dindin.sim.demand import (
    CURVA_K,
    CURVA_MID,
    apelo,
    f_clima,
    f_preco,
    f_reputacao,
    tolerancia_efetiva,
)
from dindin.sim.models import Weather
from dindin.sim.types import WeatherKind


def test_exemplo_dourado_praia_para():
    """PA, praia, sabado escaldante hi=37, rep 62. Numeros fixados no plano."""
    pa, praia = REGIOES["pa"], LOCAIS["praia"]

    fc = f_clima(37.0, WeatherKind.ESCALDANTE, praia.sensibilidade_clima)
    assert fc == pytest.approx(2.0572, abs=1e-4)

    trafego = 260 * fc * 1.30 * 1.00 * f_reputacao(62) * 1.03
    assert trafego == pytest.approx(759.2, abs=0.5)

    a_acai = apelo(SABORES["acai"], pa, praia, 37.0, 0)
    a_coco = apelo(SABORES["coco"], pa, praia, 37.0, 0)
    total = a_acai + a_coco
    assert a_acai / total == pytest.approx(0.686, abs=1e-3)
    assert a_coco / total == pytest.approx(0.314, abs=1e-3)

    tol = tolerancia_efetiva(pa, praia, 37.0)
    assert tol == pytest.approx(1.2350, abs=1e-4)

    assert trafego * (a_acai / total) * f_preco(450, 400, tol) == pytest.approx(475, abs=2)
    assert trafego * (a_coco / total) * f_preco(200, 200, tol) == pytest.approx(226, abs=2)


def test_otimo_de_receita_fica_acima_do_preco_de_referencia():
    """O otimo tem que ficar em r~1.02-1.08: furar preco NAO pode ser dominante."""
    melhor_r, melhor_receita = 0.0, 0.0
    r = 0.50
    while r <= 1.80:
        receita = r * (1.0 / (1.0 + math.exp(CURVA_K * (r - CURVA_MID))))
        if receita > melhor_receita:
            melhor_r, melhor_receita = r, receita
        r += 0.001
    assert 1.02 <= melhor_r <= 1.08, f"otimo em r={melhor_r:.3f}"


def test_preco_maior_nunca_vende_mais():
    anterior = 2.0
    for preco in range(100, 900, 25):
        atual = f_preco(preco, 400, 1.0)
        assert atual <= anterior + 1e-9
        anterior = atual


def test_mais_calor_nunca_diminui_trafego():
    anterior = 0.0
    for hi in range(20, 45):
        atual = f_clima(float(hi), WeatherKind.QUENTE, 1.0)
        assert atual >= anterior - 1e-9
        anterior = atual


def test_calor_permite_cobrar_mais_caro():
    pa, praia = REGIOES["pa"], LOCAIS["praia"]
    ameno = tolerancia_efetiva(pa, praia, 28.0)
    escaldante = tolerancia_efetiva(pa, praia, 37.0)
    assert escaldante > ameno

    def melhor_preco(tol: float) -> int:
        return max(range(200, 900), key=lambda p: p * f_preco(p, 400, tol))

    assert melhor_preco(escaldante) > melhor_preco(ameno)


def test_chuva_e_frio_derrubam_o_movimento():
    for ruim in (WeatherKind.CHUVA, WeatherKind.TEMPORAL, WeatherKind.FRIO):
        assert f_clima(30.0, ruim, 1.0) < f_clima(30.0, WeatherKind.QUENTE, 1.0)


def test_preferencia_regional_muda_o_apelo():
    """Acai no PA tem que ter muito mais apelo do que acai no RS."""
    praia = LOCAIS["praia"]
    no_para = apelo(SABORES["acai"], REGIOES["pa"], praia, 32.0, 0)
    no_sul = apelo(SABORES["acai"], REGIOES["rs"], praia, 32.0, 0)
    assert no_para > no_sul * 2


def test_enjoo_reduz_apelo():
    praia = LOCAIS["praia"]
    novo = apelo(SABORES["coco"], REGIOES["ce"], praia, 32.0, 0)
    repetido = apelo(SABORES["coco"], REGIOES["ce"], praia, 32.0, 6)
    assert repetido < novo


def test_escola_desfavorece_gourmet():
    """Capitulo 4 e de proposito ruim pra gourmet: obriga a mudar de estrategia."""
    escola, praia = LOCAIS["escola"], LOCAIS["praia"]
    ce = REGIOES["ce"]
    g_escola = apelo(SABORES["acai"], ce, escola, 32.0, 0)
    g_praia = apelo(SABORES["acai"], ce, praia, 32.0, 0)
    assert g_escola < g_praia
