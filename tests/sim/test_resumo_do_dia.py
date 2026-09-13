"""O veredito de uma linha no fim do relatorio: qual chave bate primeiro."""

from dindin.sim.engine import resumo_do_dia
from dindin.sim.models import Weather
from dindin.sim.state import DayResult, FlavorOutcome
from dindin.sim.types import WeatherKind

_CLIMA = Weather(WeatherKind.QUENTE, 30.0, 0.5, 31.0)


def _dia(por_sabor, receita=0, custo_insumos=0, custo_fixo=0) -> DayResult:
    lucro = receita - custo_insumos - custo_fixo
    return DayResult(
        dia=1, clima=_CLIMA, local="isopor", eventos=(), por_sabor=por_sabor,
        receita=receita, custo_insumos=custo_insumos, custo_fixo=custo_fixo,
        lucro=lucro, caixa_final=10000, reputacao_delta=0.0,
    )


def _sabor(ofertados, vendidos, preco=200, receita=None,
           perdidos_derretimento=0, demanda_potencial=None):
    return FlavorOutcome(
        flavor="coco", ofertados=ofertados, vendidos=vendidos, preco=preco,
        receita=receita if receita is not None else vendidos * preco,
        perdidos_derretimento=perdidos_derretimento,
        demanda_potencial=demanda_potencial if demanda_potencial is not None
        else vendidos,
    )


def test_nada_foi_produzido():
    assert resumo_do_dia(_dia(())) == "resumo.nada_pra_vender"


def test_teve_estoque_mas_nao_vendeu_nada():
    r = _dia((_sabor(40, 0, demanda_potencial=0),))
    assert resumo_do_dia(r) == "resumo.zero_venda"


def test_derreteu_mais_do_que_vendeu():
    r = _dia((_sabor(40, 10, perdidos_derretimento=15, demanda_potencial=10),),
             receita=2000, custo_insumos=500)
    assert resumo_do_dia(r) == "resumo.derreteu_muito"


def test_vendeu_tudo_e_ainda_faltou_gente():
    """demanda_nao_atendida (faltou) e o que sobrou de demanda, nao o total
    que queria comprar -- por isso o teste pede bem mais do que vendeu."""
    r = _dia((_sabor(30, 30, demanda_potencial=90),),
             receita=6000, custo_insumos=1000)
    assert resumo_do_dia(r) == "resumo.faltou_estoque"


def test_prejuizo_no_dia():
    r = _dia((_sabor(20, 15, demanda_potencial=15),),
             receita=3000, custo_insumos=2000, custo_fixo=1500)
    assert resumo_do_dia(r) == "resumo.prejuizo"


def test_sellout_limpo_sem_faltar_ninguem():
    r = _dia((_sabor(30, 30, demanda_potencial=30),),
             receita=6000, custo_insumos=1000)
    assert resumo_do_dia(r) == "resumo.sellout_limpo"


def test_lucro_bem_forte():
    r = _dia((_sabor(20, 15, demanda_potencial=15),),
             receita=3000, custo_insumos=200, custo_fixo=100)
    assert resumo_do_dia(r) == "resumo.lucro_forte"


def test_dia_comum_cai_no_normal():
    r = _dia((_sabor(30, 20, demanda_potencial=25),),
             receita=4000, custo_insumos=2500, custo_fixo=800)
    assert resumo_do_dia(r) == "resumo.dia_normal"


def test_zero_venda_tem_prioridade_sobre_derretimento():
    """Nao vender nada e pior do que derreter -- a chave mais grave ganha."""
    r = _dia((_sabor(40, 0, perdidos_derretimento=40, demanda_potencial=0),))
    assert resumo_do_dia(r) == "resumo.zero_venda"
