"""Harness de balanceamento: roda politicas automaticas em varias sementes.

Uso: uv run python tools/balance_sim.py [n_sementes]
"""

import statistics
import sys

from dindin.content.flavors import SABORES, sabores_disponiveis
from dindin.content.locations import LOCAIS, ORDEM_LOCAIS
from dindin.content.regions import ORDEM_REGIOES
from dindin.sim import economy, progression
from dindin.sim.demand import tolerancia_efetiva
from dindin.sim.engine import advance_day, clima_do_dia
from dindin.sim.state import DayPlan, GameState
from dindin.content.regions import REGIOES
from dindin.sim.freezer import capacidade_dia, capacidade_total
from dindin.sim.types import Tier

MAX_DIAS = 200


def _melhores_sabores(state: GameState, n: int = 2) -> list[str]:
    regiao = REGIOES[state.regiao]
    local = LOCAIS[state.local_atual]
    cands = sabores_disponiveis(state.locais_desbloqueados)
    def score(f):
        margem = f.preco_ref - economy.custo_unitario(f.key, state.regiao)
        afin = local.gourmet_afinidade if f.tier is Tier.GOURMET else 1.0
        return margem * regiao.pref(f.key) * afin * f.apelo_base
    return [f.key for f in sorted(cands, key=score, reverse=True)[:n]]


def _preco_otimo(flavor: str, regiao: str, tol: float, ratio: float) -> int:
    """Preco que maximiza LUCRO (nao receita): margem x resposta de demanda."""
    from dindin.sim.demand import f_preco

    ref = SABORES[flavor].preco_ref
    custo = economy.custo_unitario(flavor, regiao)
    melhor, melhor_lucro = ref, -1.0
    for p in range(int(ref * 0.5), int(ref * 2.2), 5):
        lucro = (p - custo) * f_preco(p, ref, tol)
        if lucro > melhor_lucro:
            melhor, melhor_lucro = p, lucro
    return max(custo + 10, round(melhor * ratio))


def politica_competente(state: GameState, ratio: float = 1.0) -> DayPlan:
    """Le a previsao, produz ate a capacidade e precifica perto do otimo."""
    local = LOCAIS[state.local_atual]
    clima = clima_do_dia(state, state.dia)
    tol = tolerancia_efetiva(REGIOES[state.regiao], local, clima.heat_index)

    escolhidos = _melhores_sabores(state, 2)
    alvo = capacidade_dia(state, state.local_atual)
    if clima.kind.value in ("chuva", "temporal"):
        alvo = int(alvo * 0.55)
    elif clima.kind.value == "frio":
        alvo = int(alvo * 0.40)
    # Nunca estocar acima do que o freezer aguenta.
    alvo = min(alvo, capacidade_total(state))

    ja_pronto = state.inventario.total_prontos()
    falta = max(0, alvo - ja_pronto)
    por_sabor = {k: max(0, falta // len(escolhidos)) for k in escolhidos}

    # Compra insumos do que falta, com folga.
    compras: dict[str, int] = {}
    for k, qtd in por_sabor.items():
        for ing, precisa in SABORES[k].consumo(qtd).items():
            tem = state.inventario.total(ing)
            if tem < precisa:
                compras[ing] = compras.get(ing, 0) + max(1, int(precisa - tem + 0.999))

    custo = economy.custo_compras(compras, state.regiao)
    while custo > state.caixa and compras:
        maior = max(compras, key=lambda k: compras[k])
        compras[maior] -= 1
        if compras[maior] <= 0:
            del compras[maior]
        por_sabor = {k: int(v * 0.8) for k, v in por_sabor.items()}
        custo = economy.custo_compras(compras, state.regiao)

    gelo = 0 if state.local_atual == "casa" else max(1, (alvo + 49) // 50)
    precos = {k: _preco_otimo(k, state.regiao, tol, ratio) for k in escolhidos}
    return DayPlan(producao=por_sabor, precos=precos, local=state.local_atual,
                   compras=compras, gelo=gelo)


def politica_ingenua(state: GameState) -> DayPlan:
    """Produz sempre o mesmo, ignora clima, cobra o preco de referencia."""
    escolhidos = _melhores_sabores(state, 1)
    k = escolhidos[0]
    compras: dict[str, int] = {}
    for ing, precisa in SABORES[k].consumo(40).items():
        tem = state.inventario.total(ing)
        if tem < precisa:
            compras[ing] = max(1, int(precisa - tem + 0.999))
    custo = economy.custo_compras(compras, state.regiao)
    if custo > state.caixa:
        compras = {}
    return DayPlan(producao={k: 40}, precos={k: SABORES[k].preco_ref},
                   local=state.local_atual, compras=compras,
                   gelo=0 if state.local_atual == "casa" else 1)


def _cuidar_do_isopor(s: GameState) -> None:
    """Compra a melhor caixa que couber no bolso quando precisa."""
    from dindin.content.coolers import ISOPORES, ORDEM_ISOPORES

    if s.local_atual == "casa":
        return
    if not (progression.precisa_de_isopor(s) or progression.isopor_acabando(s)):
        return
    # Guarda uma folga pra insumos: nao gasta tudo na caixa.
    folga = s.caixa * 0.40
    for key in reversed(ORDEM_ISOPORES):
        if ISOPORES[key].custo <= folga:
            progression.comprar_isopor(s, key)
            return
    if progression.precisa_de_isopor(s):
        mais_barato = ORDEM_ISOPORES[0]
        if s.caixa >= ISOPORES[mais_barato].custo:
            progression.comprar_isopor(s, mais_barato)


def rodar(regiao: str, seed: int, politica) -> tuple[str, int, int]:
    s = GameState(seed=seed, regiao=regiao, local_atual="casa")
    for _ in range(MAX_DIAS):
        if s.encerrado:
            break
        s.local_atual = progression.melhor_local(s)  # volta de graca ao ponto
        _cuidar_do_isopor(s)
        if progression.precisa_de_isopor(s):
            s.local_atual = "casa"   # sem caixa, vende de casa hoje
        advance_day(s, politica(s))
        # Sobe de ponto sempre que da. `pode_desbloquear` so responde pro
        # ponto ainda trancado -- se ele ja foi liberado antes e o jogador
        # nao mudou, e preciso olhar o proximo da lista direto.
        prox = progression.pode_desbloquear(s) or progression.proximo_local(s)
        if (prox and prox != s.local_atual
                and s.caixa >= LOCAIS[s.local_atual].meta_caixa
                and s.caixa >= LOCAIS[prox].custo_entrada + 4000):
            progression.desbloquear(s, prox)
            _cuidar_do_isopor(s)
    return (s.encerrado or "inacabado", s.dia, s.caixa)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(f"{'regiao':8} {'politica':12} {'vitorias':>9} {'falencias':>10} "
          f"{'dias p50':>9} {'dias p90':>9}")
    print("-" * 62)
    for regiao in ORDEM_REGIOES:
        for nome, pol in (("competente", politica_competente),
                          ("ingenua", politica_ingenua)):
            resultados = [rodar(regiao, s, pol) for s in range(n)]
            vit = [d for st, d, _ in resultados if st == "vitoria"]
            fal = sum(1 for st, _, _ in resultados if st == "falencia")
            p50 = f"{statistics.median(vit):.0f}" if vit else "-"
            p90 = (f"{sorted(vit)[int(len(vit) * 0.9) - 1]:.0f}"
                   if len(vit) >= 2 else "-")
            print(f"{regiao:8} {nome:12} {len(vit):>4}/{n:<4} {fal:>10} "
                  f"{p50:>9} {p90:>9}")


if __name__ == "__main__":
    main()
