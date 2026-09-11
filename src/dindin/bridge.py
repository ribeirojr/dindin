"""Ponte entre a simulacao e o mundo JS (Pyodide).

Regra: so entra e sai JSON puro (dict/list/str/int/float/bool/None).
Nada de dataclass, enum ou objeto Python atravessa a fronteira -- assim o
mesmo modulo serve pro navegador, pra um servidor HTTP ou pra teste.

A camada sim/ continua sem saber que isso existe.
"""

from dataclasses import asdict, is_dataclass
from typing import Any

from .content.flavors import SABORES, sabores_disponiveis
from .content.ingredients import INSUMOS, insumos_disponiveis
from .content.locations import LOCAIS, ORDEM_LOCAIS, UPGRADES
from .content.regions import ORDEM_REGIOES, REGIOES
from .i18n import REGIOES_I18N, Translator, money
from .i18n.barks import pool
from .i18n.base_ptbr import BASE
from .sim.types import BarkTag
from .sim import economy, progression
from .sim.demand import f_preco, tolerancia_efetiva
from .sim.engine import advance_day, clima_do_dia, tolerancia_efetiva_do_dia
from .sim.freezer import capacidade_dia, capacidade_total
from .sim.state import DayPlan, GameState, Inventory, Lote


# ---------------------------------------------------------------- serializacao

def _jsonify(obj: Any) -> Any:
    """Converte qualquer coisa da simulacao em JSON puro."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _jsonify(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {str(k): _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_jsonify(v) for v in obj]
    if hasattr(obj, "value") and hasattr(obj, "name"):  # StrEnum
        return obj.value
    return obj


def estado_para_json(state: GameState) -> dict:
    return {
        "seed": state.seed,
        "regiao": state.regiao,
        "dia": state.dia,
        "caixa": state.caixa,
        "reputacao": round(state.reputacao, 1),
        "local_atual": state.local_atual,
        "locais_desbloqueados": list(state.locais_desbloqueados),
        "capacidade_freezer": capacidade_total(state),
        "capacidade_freezer_base": state.capacidade_freezer,
        "capacidade_dia": capacidade_dia(state, state.local_atual),
        "upgrades": sorted(state.upgrades),
        "encerrado": state.encerrado,
        "inventario": {
            "ingredientes": {
                k: round(state.inventario.total(k), 3)
                for k in state.inventario.ingredientes
                if state.inventario.total(k) > 0
            },
            # Lotes com validade: sem eles, insumo nunca venceria no navegador.
            "lotes": {
                k: [[round(l.qtd, 3), l.dia_validade] for l in lotes if l.qtd > 0]
                for k, lotes in state.inventario.ingredientes.items()
                if any(l.qtd > 0 for l in lotes)
            },
            "prontos": dict(state.inventario.prontos),
        },
        "vendas_recentes": dict(state.vendas_recentes),
        "socorro_usado": state.socorro_usado,
        "isopor": state.isopor,
        "isopor_dias": state.isopor_dias,
    }


def estado_de_json(d: dict) -> GameState:
    inv_json = d.get("inventario", {})
    lotes = inv_json.get("lotes")
    if lotes:
        ingredientes = {
            k: [Lote(float(qtd), val) for qtd, val in ls]
            for k, ls in lotes.items() if ls
        }
    else:
        # Estado antigo (sem lotes): totais viram lote unico sem validade.
        ingredientes = {
            k: [Lote(float(v), None)]
            for k, v in inv_json.get("ingredientes", {}).items()
        }
    inv = Inventory(
        ingredientes=ingredientes,
        prontos=dict(inv_json.get("prontos", {})),
    )
    return GameState(
        seed=d["seed"], regiao=d["regiao"], dia=d["dia"], caixa=d["caixa"],
        reputacao=d["reputacao"], local_atual=d["local_atual"],
        locais_desbloqueados=list(d["locais_desbloqueados"]),
        inventario=inv,
        capacidade_freezer=d.get("capacidade_freezer_base", 60),
        upgrades=set(d.get("upgrades", [])),
        vendas_recentes=dict(d.get("vendas_recentes", {})),
        socorro_usado=bool(d.get("socorro_usado", False)),
        isopor=d.get("isopor"),
        isopor_dias=d.get("isopor_dias", 0),
        encerrado=d.get("encerrado"),
    )


# ---------------------------------------------------------------- conteudo

def catalogo(regiao: str, desbloqueados: list | None = None) -> dict:
    """Tudo que a UI precisa saber de uma vez: textos, sabores, insumos, pontos.

    `desbloqueados` filtra pro que o jogador ja pode usar -- no dia 1 sao
    3 sabores e 4 insumos, nao os 17 e 8 do jogo inteiro.
    """
    tr = Translator(regiao)
    liberados = list(desbloqueados) if desbloqueados else None
    return {
        "regiao": regiao,
        "textos": {k: tr.t(k) for k in BASE},
        # Falas regionais: sem elas o navegador falaria pt-BR neutro.
        "barks": {tag.value: pool(regiao, tag) for tag in BarkTag},
        "produto": {"sing": tr.produto, "plur": tr.t("produto.plur")},
        "insumos": [
            {
                "key": i.key, "nome": i.nome, "unidade": i.unidade,
                "preco": i.preco_unitario(1, REGIOES[regiao].custo_insumo_mod),
                "validade": i.validade_dias,
                "bulk": [{"min": m, "fator": f} for m, f in i.bulk],
            }
            for i in (insumos_disponiveis(liberados) if liberados
                      else [x for x in INSUMOS.values() if x.key != "gelo"])
        ],
        "sabores": [
            {
                "key": f.key, "nome": f.nome, "tier": f.tier.value,
                "preco_ref": f.preco_ref, "apelo": f.apelo_base,
                "desbloqueio": f.desbloqueio,
                "custo": economy.custo_unitario(f.key, regiao),
                "preferencia": REGIOES[regiao].pref(f.key),
                "receita": dict(f.receita),
            }
            for f in (sabores_disponiveis(liberados) if liberados
                      else list(SABORES.values()))
        ],
        "locais": [
            {
                "key": l.key, "nome": l.nome, "ordem": l.ordem,
                "meta": l.meta_caixa, "entrada": l.custo_entrada,
                "trafego": l.trafego_base, "capacidade": l.capacidade,
                "custo_fixo": l.custo_fixo_dia,
                "gourmet": l.gourmet_afinidade,
                "chuva": l.chuva_mod,
            }
            for l in LOCAIS.values()
        ],
        "upgrades": [
            {"key": u.key, "nome": u.nome, "custo": u.custo,
             "desbloqueio": u.desbloqueio, "descricao": u.descricao}
            for u in UPGRADES.values()
        ],
    }


def regioes() -> list[dict]:
    """Lista pra tela de escolha, ja com o nome do produto em cada estado."""
    saida = []
    for key in ORDEM_REGIOES:
        r = REGIOES[key]
        tr = Translator(key)
        favoritos = sorted(r.preferencia.items(), key=lambda kv: -kv[1])[:3]
        saida.append({
            "key": key, "nome": r.nome, "gentilico": r.gentilico,
            "produto": tr.produto,
            "giria": [tr.t("interj.surpresa"), tr.t("interj.positivo"),
                      tr.t("vocativo")],
            "tolerancia": r.tolerancia_preco,
            "custo_mod": r.custo_insumo_mod,
            "favoritos": [
                {"key": k, "nome": SABORES[k].nome, "mult": m}
                for k, m in favoritos if k in SABORES
            ],
        })
    return saida


# ---------------------------------------------------------------- jogo

def novo_jogo(regiao: str, seed: int) -> dict:
    state = GameState(seed=seed, regiao=regiao, local_atual="casa")
    return estado_para_json(state)


def previsao(estado: dict) -> dict:
    state = estado_de_json(estado)
    return _jsonify(clima_do_dia(state, state.dia))


def isopores(estado: dict) -> dict:
    """Caixas a venda + o estado da que esta em uso."""
    from .content.coolers import ISOPORES, ORDEM_ISOPORES

    state = estado_de_json(estado)
    return {
        "atual": state.isopor,
        "dias_restantes": state.isopor_dias,
        "precisa": progression.precisa_de_isopor(state),
        "acabando": progression.isopor_acabando(state),
        "opcoes": [
            {
                "key": k, "nome": ISOPORES[k].nome,
                "custo": ISOPORES[k].custo, "dias": ISOPORES[k].dias,
                "capacidade": ISOPORES[k].capacidade,
                "derretimento": ISOPORES[k].derretimento,
                "custo_por_dia": ISOPORES[k].custo_por_dia,
                "descricao": ISOPORES[k].descricao,
                "pode": state.caixa >= ISOPORES[k].custo,
            }
            for k in ORDEM_ISOPORES
        ],
    }


def comprar_isopor(estado: dict, key: str) -> dict:
    state = estado_de_json(estado)
    ok = progression.comprar_isopor(state, key)
    return {"ok": ok, "estado": estado_para_json(state)}


def info_do_gelo(estado: dict, unidades: int) -> dict:
    """Quanto um saco rende hoje e quanto derrete pra cada quantidade."""
    from .sim.freezer import cobertura_do_saco

    state = estado_de_json(estado)
    # O que passa da capacidade do dia nem chega ao ponto -- gelo pra isso
    # seria dinheiro jogado fora. Mesma conta do engine (disponivel_hoje).
    unidades = min(int(unidades), capacidade_dia(state, state.local_atual))
    clima = clima_do_dia(state, state.dia)
    cobertura = cobertura_do_saco(clima.heat_index)
    preco = INSUMOS["gelo"].preco_unitario(
        1, REGIOES[state.regiao].custo_insumo_mod)
    opcoes = []
    for sacos in range(0, 9):
        coberto = sacos * cobertura
        opcoes.append({
            "sacos": sacos,
            "custo": sacos * preco,
            "derrete": max(0, unidades - coberto),
        })
    return {
        "cobertura": cobertura,
        "cobertura_normal": 50,
        "preco_saco": preco,
        "unidades": unidades,
        "sugestao": max(1, -(-unidades // cobertura)) if unidades else 0,
        "opcoes": opcoes,
    }


def sabores_do_jogador(estado: dict, carrinho: dict | None = None,
                       producao: dict | None = None) -> list[dict]:
    """Sabores disponiveis e quanto da pra fazer de cada um.

    `carrinho` e o que o jogador acabou de por na feira mas ainda nao
    comprou. Entra na conta pra tela da cozinha responder na hora --
    sem isso "Da pra fazer" ficaria congelado no que tinha antes da feira.

    `producao` e o que ele ja mandou fazer nesta tela. Insumo e compartilhado
    (coco e maracuja saem da MESMA polpa), entao reservar 40 de coco tem que
    derrubar o maximo do maracuja -- senao o jogador planeja mais do que cabe.
    """
    state = estado_de_json(estado)
    if carrinho:
        for key, qtd in carrinho.items():
            if qtd and key in INSUMOS:
                state.inventario.adicionar(key, float(qtd), None)

    pedido = {k: int(v) for k, v in (producao or {}).items()
              if v and k in SABORES}

    saida = []
    for f in sabores_disponiveis(state.locais_desbloqueados):
        faltando = {}
        for ing_key, por_dez in f.receita.items():
            precisa = por_dez / 10.0
            tem = state.inventario.total(ing_key)
            if tem < precisa:
                faltando[ing_key] = INSUMOS[ing_key].nome
        saida.append({
            "key": f.key, "nome": f.nome, "tier": f.tier.value,
            "custo": economy.custo_unitario(f.key, state.regiao),
            "preco_ref": f.preco_ref,
            "pode_produzir": economy.pode_produzir_com_reserva(
                state, f.key, pedido),
            "pronto": state.inventario.prontos.get(f.key, 0),
            "receita": [
                {
                    "key": k,
                    "nome": INSUMOS[k].nome,
                    "unidade": INSUMOS[k].unidade,
                    "por_dez": v,
                    "tem": round(state.inventario.total(k), 2),
                }
                for k, v in f.receita.items()
            ],
            "faltando": sorted(faltando.values()),
        })
    return saida


def curva_de_preco(estado: dict, flavor: str, minimo: int = 50,
                   maximo: int = 900, passo: int = 10) -> dict:
    """Curva de demanda x preco pro grafico. E o termometro virando gráfico.

    Devolve tambem o preco que maximiza LUCRO -- o ponto que o jogador
    precisa aprender a achar.
    """
    state = estado_de_json(estado)
    clima = clima_do_dia(state, state.dia)
    tol = tolerancia_efetiva_do_dia(state, state.local_atual, clima)
    ref = SABORES[flavor].preco_ref
    custo = economy.custo_unitario(flavor, state.regiao)

    pontos = []
    melhor_lucro, melhor_preco = -1.0, ref
    for p in range(minimo, maximo + 1, passo):
        resp = f_preco(p, ref, tol)
        lucro_rel = (p - custo) * resp
        pontos.append({
            "preco": p,
            "resposta": round(resp, 4),
            "receita_rel": round(p * resp, 2),
            "lucro_rel": round(lucro_rel, 2),
        })
        if lucro_rel > melhor_lucro:
            melhor_lucro, melhor_preco = lucro_rel, p

    return {
        "flavor": flavor, "preco_ref": ref, "custo": custo,
        "tolerancia": round(tol, 4),
        "preco_justo": round(ref * tol),
        "melhor_preco": melhor_preco,
        "pontos": pontos,
    }


def jogar_dia(estado: dict, plano: dict) -> dict:
    """Roda um dia. Recebe e devolve JSON puro."""
    state = estado_de_json(estado)

    # Mesma regra da TUI: o dia acontece no ponto mais avancado que ja e do
    # jogador (voltar e de graca) -- senao quem cai pro socorro fica preso em
    # casa pra sempre. Sem isopor vivo o dia roda de casa, mas o ponto
    # continua sendo dele: e o que mantem a vitrine de isopor na tela.
    state.local_atual = progression.melhor_local(state)
    local_do_dia = state.local_atual
    if progression.precisa_de_isopor(state):
        local_do_dia = "casa"

    gasto = 0
    if plano.get("compras"):
        gasto = economy.comprar(state, plano["compras"])
    if plano.get("producao"):
        economy.produzir(state, plano["producao"])

    gelo = int(plano.get("gelo", 0))
    day_plan = DayPlan(
        producao={}, precos=plano.get("precos", {}),
        local=local_do_dia, compras={}, gelo=gelo,
    )
    resultado = advance_day(state, day_plan, gasto_previo=gasto)

    prox = progression.pode_desbloquear(state)
    return {
        "resultado": _jsonify(resultado),
        "estado": estado_para_json(state),
        "desbloqueou": prox,
    }


def mudar_de_ponto(estado: dict, local: str) -> dict:
    state = estado_de_json(estado)
    ok = progression.desbloquear(state, local)
    return {"ok": ok, "estado": estado_para_json(state)}


def formatar_dinheiro(centavos: int) -> str:
    return money(centavos)


def versao() -> dict:
    from . import __version__
    return {"versao": __version__, "regioes": list(REGIOES_I18N),
            "locais": list(ORDEM_LOCAIS)}
