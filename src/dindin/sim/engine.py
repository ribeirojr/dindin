"""Orquestracao do dia: simulate_day e advance_day.

simulate_day e uma funcao pura o suficiente para rodar milhares de dias
sem terminal: nenhuma I/O, nenhum random global.
"""

from collections.abc import Mapping
from dataclasses import replace
from datetime import date, timedelta
from random import Random

from ..content.flavors import SABORES
from ..content.locations import CUSTO_AJUDANTE_DIA, LOCAIS
from . import economy, events, freezer, progression
from .calendar import mod_calendario, outcomes_calendario
from .demand import calcular_demanda, f_preco, tolerancia_efetiva
from .models import Weather
from .rng import stream
from .state import (
    DayPlan,
    DayResult,
    EventOutcome,
    FlavorOutcome,
    GameState,
)
from .types import BarkTag, Centavos, Tier
from .weather import sortear_clima

DATA_INICIAL = date(2026, 1, 5)  # uma segunda-feira

REP_SELLOUT_BOM = 0.8
REP_STOCKOUT = -2.5
REP_DERRETIDO = -1.5
REP_PRECO_ABUSIVO = -1.2
REP_DIA_NORMAL = 0.15


def data_do_dia(dia: int) -> date:
    return DATA_INICIAL + timedelta(days=dia - 1)


def clima_do_dia(state: GameState, dia: int) -> Weather:
    return sortear_clima(state.regiao, data_do_dia(dia), stream(state.seed, dia, "clima"))


def previsao_amanha(state: GameState) -> Weather:
    return clima_do_dia(state, state.dia + 1)


def _barks(
    resultados: list[FlavorOutcome],
    precos: Mapping[str, Centavos],
    tol: float,
    clima: Weather,
    rng: Random,
) -> tuple[tuple[BarkTag, str], ...]:
    """Gera falas do publico. Sao sabor E diagnostico: 'ta caro' avisa o jogador."""
    saida: list[tuple[BarkTag, str]] = []
    for r in resultados:
        sabor = SABORES[r.flavor]
        resposta = f_preco(r.preco, sabor.preco_ref, tol)
        if resposta < 0.35:
            saida.extend((BarkTag.PRECO_ALTO, r.flavor) for _ in range(3))
        elif resposta > 0.92:
            saida.append((BarkTag.PRECO_BARATO, r.flavor))
        if r.vendidos > 0:
            tag = (BarkTag.COMPRA_GOURMET if sabor.tier is Tier.GOURMET
                   else BarkTag.COMPRA_SIMPLES)
            saida.extend((tag, r.flavor) for _ in range(min(3, 1 + r.vendidos // 25)))
        if r.demanda_potencial > r.ofertados and r.ofertados > 0:
            saida.append((BarkTag.SELLOUT, r.flavor))
    if clima.heat_index > 34:
        saida.append((BarkTag.CALOR, ""))
    if clima.kind.value in ("chuva", "temporal"):
        saida.append((BarkTag.CHUVA, ""))
    rng.shuffle(saida)
    return tuple(saida[:14])


def simulate_day(state: GameState, plan: DayPlan, rng: Random | None = None,
                 gasto_previo: Centavos = 0) -> DayResult:
    """Roda um dia inteiro e devolve o resultado. NAO altera state.dia.

    gasto_previo: compras ja debitadas fora do plano (a UI compra na tela da
    feira). Entra no relatorio pra receita - custos == lucro continuar valendo.
    """
    dia = state.dia
    d = data_do_dia(dia)
    rng = rng or stream(state.seed, dia, "dia")
    local = LOCAIS[plan.local]

    caixa_inicial = state.caixa

    # 1. Insumos vencidos somem antes de qualquer coisa.
    state.inventario.expirar(dia)

    # 2. Compras e producao.
    custo_insumos = gasto_previo + economy.comprar(state, plan.compras)
    if plan.gelo:
        # So compra o gelo que cabe no caixa: sem isso o jogador fica devendo.
        preco_gelo = economy.custo_compras({"gelo": 1}, state.regiao)
        cabe = state.caixa // preco_gelo if preco_gelo else 0
        sacos = max(0, min(plan.gelo, cabe))
        if sacos:
            custo_insumos += economy.comprar(state, {"gelo": sacos})
        plan = replace(plan, gelo=sacos)
    economy.produzir(state, plan.producao)

    # 3. Clima e eventos.
    clima = clima_do_dia(state, dia)
    evs = events.sortear(state.regiao, plan.local, stream(state.seed, dia, "evento"))
    mod_ev, custo_ev, out_ev = events.aplicar(state, evs)
    out_cal = outcomes_calendario(d)
    mod_total = mod_ev * mod_calendario(d)

    # 4. Perdas de estoque: excesso de freezer e falta de gelo.
    perdas: dict[str, int] = {}
    for k, v in freezer.derretimento_por_excesso(state).items():
        perdas[k] = perdas.get(k, 0) + v
    disponivel_hoje = min(state.inventario.total_prontos(),
                          freezer.capacidade_dia(state, plan.local))
    for k, v in freezer.falta_de_gelo(state, plan.local, plan.gelo,
                                      disponivel_hoje,
                                      clima.heat_index).items():
        perdas[k] = perdas.get(k, 0) + v

    # 5. Quanto de cada sabor vai pro ponto (limitado pela capacidade do dia).
    prontos = dict(state.inventario.prontos)
    cap_dia = freezer.capacidade_dia(state, plan.local)
    total_prontos = sum(prontos.values())
    ofertados: dict[str, int] = {}
    if total_prontos > 0:
        if total_prontos <= cap_dia:
            ofertados = dict(prontos)
        else:
            for k, v in prontos.items():
                ofertados[k] = int(v * cap_dia / total_prontos)
            # O piso do int() deixa vagas no isopor: completa com quem
            # ainda tem estoque parado em casa.
            sobra_cap = cap_dia - sum(ofertados.values())
            for k in sorted(prontos, key=lambda x: -(prontos[x] - ofertados[x])):
                if sobra_cap <= 0:
                    break
                extra = min(sobra_cap, prontos[k] - ofertados[k])
                ofertados[k] += extra
                sobra_cap -= extra
    ofertados = {k: v for k, v in ofertados.items() if v > 0 and k in plan.precos}

    # 6. Vendas.
    demanda, vendidos, _ = calcular_demanda(
        ofertados, plan.precos, SABORES, state.regiao, plan.local, clima,
        d.weekday(), state.reputacao, rng, mod_total, state.vendas_recentes,
        1.08 if "banner" in state.upgrades else 1.0,
    )

    receita: Centavos = 0
    resultados: list[FlavorOutcome] = []
    for k in sorted(ofertados):
        v = vendidos.get(k, 0)
        r = v * plan.precos[k]
        receita += r
        state.inventario.prontos[k] = state.inventario.prontos.get(k, 0) - v
        if state.inventario.prontos.get(k, 0) <= 0:
            state.inventario.prontos.pop(k, None)
        resultados.append(FlavorOutcome(
            flavor=k, ofertados=ofertados[k], vendidos=v, preco=plan.precos[k],
            receita=r, perdidos_derretimento=perdas.get(k, 0),
            demanda_potencial=demanda.get(k, 0),
        ))

    # 7. Custos fixos e caixa. Nunca deixa o caixa ficar negativo: se nao da
    # pra pagar o ponto, cobra so o que tem (o jogador quebra, nao endivida).
    custo_fixo = local.custo_fixo_dia + custo_ev
    if "ajudante" in state.upgrades:
        custo_fixo += CUSTO_AJUDANTE_DIA
    custo_fixo = min(custo_fixo, max(0, state.caixa + receita))
    state.caixa += receita - custo_fixo

    # 8. Reputacao.
    tol = tolerancia_efetiva_do_dia(state, plan.local, clima)
    delta = REP_DIA_NORMAL
    # Vender tudo e bom. Faltar MUITO num dia cheio e que queima a fama:
    # so pesa quando a demanda perdida foi grande de verdade.
    perdida = sum(max(0, r.demanda_potencial - r.ofertados) for r in resultados)
    ofertado_total = sum(r.ofertados for r in resultados)
    faltou_feio = ofertado_total > 0 and perdida > ofertado_total
    if faltou_feio:
        delta += REP_STOCKOUT if mod_total > 1.2 else -1.0
    elif resultados and all(r.vendidos == r.ofertados for r in resultados):
        delta += REP_SELLOUT_BOM
    if perdas:
        delta += REP_DERRETIDO
    if any(f_preco(r.preco, SABORES[r.flavor].preco_ref, tol) < 0.20
           for r in resultados):
        delta += REP_PRECO_ABUSIVO
    state.reputacao = max(0.0, min(100.0, state.reputacao + delta))

    # 9. O isopor gasta um dia de vida quando sai pra rua.
    eventos_isopor: list[EventOutcome] = []
    if plan.local != "casa" and state.isopor:
        state.isopor_dias -= 1
        if state.isopor_dias <= 0:
            from ..content.coolers import ISOPORES
            nome = ISOPORES[state.isopor].nome
            eventos_isopor.append(EventOutcome(
                "isopor_acabou", "evento.isopor_acabou", {"nome": nome}))
            state.isopor = None
            state.isopor_dias = 0

    # 10. Contador de enjoo por sabor.
    for k in list(state.vendas_recentes):
        if k not in ofertados:
            state.vendas_recentes.pop(k)
    for k in ofertados:
        state.vendas_recentes[k] = state.vendas_recentes.get(k, 0) + 1

    lucro = receita - custo_insumos - custo_fixo
    return DayResult(
        dia=dia, clima=clima, local=plan.local,
        eventos=out_ev + out_cal + tuple(eventos_isopor),
        por_sabor=tuple(resultados),
        receita=receita, custo_insumos=custo_insumos, custo_fixo=custo_fixo,
        lucro=lucro, caixa_final=state.caixa,
        reputacao_delta=delta,
        barks=_barks(resultados, plan.precos, tol, clima,
                     stream(state.seed, dia, "bark")),
    )


def tolerancia_efetiva_do_dia(state: GameState, local_key: str,
                              clima: Weather) -> float:
    from ..content.regions import REGIOES
    return tolerancia_efetiva(REGIOES[state.regiao], LOCAIS[local_key],
                              clima.heat_index)


def advance_day(state: GameState, plan: DayPlan,
                gasto_previo: Centavos = 0) -> DayResult:
    """Roda o dia, guarda no historico e avanca o calendario."""
    resultado = simulate_day(state, plan, gasto_previo=gasto_previo)
    state.historico.append(resultado)
    state.dia += 1
    state.encerrado = progression.checar_fim(state)
    return resultado
