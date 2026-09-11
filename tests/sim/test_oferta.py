"""O que vai pro ponto quando o estoque passa da capacidade do dia."""

from dindin.sim.engine import simulate_day
from dindin.sim.state import DayPlan, GameState


def _estado_na_rua(prontos: dict[str, int]) -> GameState:
    s = GameState(seed=1, regiao="ce", local_atual="isopor", caixa=50000,
                  locais_desbloqueados=["casa", "isopor"],
                  isopor="simples", isopor_dias=10,
                  capacidade_freezer=400)  # freezer folgado: nada derrete em casa
    s.inventario.prontos = dict(prontos)
    return s


def test_oferta_usa_a_capacidade_inteira_do_isopor():
    """O piso do rateio (int) deixava vagas: 3 sabores de 67 num isopor de
    100 ofereciam 99. A vaga que sobra vai pra quem tem estoque parado."""
    s = _estado_na_rua({"coco": 67, "limao": 67, "maracuja": 67})
    precos = {"coco": 200, "limao": 200, "maracuja": 200}
    r = simulate_day(s, DayPlan({}, precos, "isopor", {}, gelo=5))
    assert sum(f.ofertados for f in r.por_sabor) == 100


def test_oferta_nao_passa_da_capacidade():
    s = _estado_na_rua({"coco": 300})
    r = simulate_day(s, DayPlan({}, {"coco": 200}, "isopor", {}, gelo=5))
    assert sum(f.ofertados for f in r.por_sabor) <= 100


def test_com_estoque_menor_que_a_capacidade_vai_tudo():
    s = _estado_na_rua({"coco": 30, "limao": 20})
    r = simulate_day(s, DayPlan({}, {"coco": 200, "limao": 200}, "isopor", {},
                                gelo=2))
    assert sum(f.ofertados for f in r.por_sabor) == 50
