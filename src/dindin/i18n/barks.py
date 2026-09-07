"""Falas da freguesia. Sao sabor E diagnostico: se o povo reclama do preco,
o jogador descobre o erro antes de ler os numeros."""

from ..sim.types import BarkTag as T

_BASE: dict[str, list[str]] = {
    T.COMPRA_SIMPLES: ["Me vê um aí!", "Vou levar dois.", "Tá geladinho?"],
    T.COMPRA_GOURMET: ["Esse cremoso é bom demais!", "Me vê um desse gourmet."],
    T.PRECO_ALTO: ["Tá caro isso aí...", "Por esse preço eu passo.",
                   "Nossa, subiu, hein?"],
    T.PRECO_BARATO: ["Tá barato! Me vê três.", "Por esse preço eu levo mais."],
    T.FILA: ["Tem fila, hein!", "Deixa eu furar a fila."],
    T.SELLOUT: ["Acabou já?", "Poxa, cheguei tarde."],
    T.CALOR: ["Que calor insuportável!", "Tô derretendo aqui."],
    T.CHUVA: ["Vou correr antes de molhar.", "Que chuva!"],
}

_REG: dict[str, dict[str, list[str]]] = {
    "ce": {
        T.COMPRA_SIMPLES: ["Me vê um dindin aí, ma broca!", "Bota dois pra mim!"],
        T.COMPRA_GOURMET: ["Esse dindin cremoso é arretado!",
                           "Ma broca, esse aí é bom demais!"],
        T.PRECO_ALTO: ["Vixe, tá caro, ma broca...", "Égua, subiu o preço?",
                       "Por esse dinheiro eu num levo não."],
        T.PRECO_BARATO: ["Arretado esse preço! Me vê três."],
        T.SELLOUT: ["Acabou, ma broca? Ê lasqueira."],
        T.CALOR: ["Tá um calor de rachar, me vê um gelado!"],
    },
    "rj": {
        T.COMPRA_SIMPLES: ["Me vê um sacolé aí, mermão!", "Manda dois!"],
        T.COMPRA_GOURMET: ["Caraca, esse cremoso é sinistro!"],
        T.PRECO_ALTO: ["Caraca, tá caro, mermão...", "Aí já é sacanagem.",
                       "Por esse preço, nem pensar."],
        T.PRECO_BARATO: ["Tá de graça isso! Me vê três."],
        T.SELLOUT: ["Acabou, mermão? Poxa."],
        T.CALOR: ["Tá um calor sinistro, me vê um!"],
    },
    "mg": {
        T.COMPRA_SIMPLES: ["Me vê uma laranjinha, sô!", "Ô, me vê duas."],
        T.COMPRA_GOURMET: ["Uai, esse cremoso é trem bão!"],
        T.PRECO_ALTO: ["Uai, tá caro, sô...", "Trem caro esse, viu.",
                       "Num vou levar não, tá salgado."],
        T.PRECO_BARATO: ["Uai, tá baratinho! Me vê três."],
        T.SELLOUT: ["Acabou, sô? Que dó."],
        T.CALOR: ["Uai, que calor, sô. Me vê um gelado."],
    },
    "sp": {
        T.COMPRA_SIMPLES: ["Me vê um geladinho, meu!", "Manda dois aí, mano."],
        T.COMPRA_GOURMET: ["Mano, esse gourmet é da hora!"],
        T.PRECO_ALTO: ["Tá caro, meu...", "Nossa, mano, salgou.",
                       "Por esse preço eu não levo."],
        T.PRECO_BARATO: ["Da hora esse preço! Me vê três."],
        T.SELLOUT: ["Acabou, meu? Que zica."],
        T.CALOR: ["Que calor, meu. Me vê um gelado."],
    },
    "rs": {
        T.COMPRA_SIMPLES: ["Me vê um gelinho, tchê!", "Bah, manda dois, guria."],
        T.COMPRA_GOURMET: ["Bah, tchê, esse cremoso tá tri!"],
        T.PRECO_ALTO: ["Bah, tá caro, tchê...", "Capaz que eu pago isso.",
                       "Tá salgado demais, guria."],
        T.PRECO_BARATO: ["Bah, tá tri barato! Me vê três."],
        T.SELLOUT: ["Bah, acabou, tchê?"],
        T.CALOR: ["Bah, que calor, tchê! Me vê um."],
    },
    "pa": {
        T.COMPRA_SIMPLES: ["Me vê um chup-chup, maninho!", "Égua, manda dois!"],
        T.COMPRA_GOURMET: ["Égua, esse de açaí tá pai d'égua, maninho!",
                           "Me vê dois de cupuaçu aí, maninho!"],
        T.PRECO_ALTO: ["Égua, tá caro isso aí, maninho...",
                       "Rapaz, por esse preço eu passo.",
                       "Égua, subiu demais."],
        T.PRECO_BARATO: ["Pai d'égua esse preço! Me vê três."],
        T.SELLOUT: ["Acabou, maninho? Égua..."],
        T.CALOR: ["Tá um calor desgraçado, me vê um gelado!"],
    },
}


def pool(regiao: str, tag: str) -> list[str]:
    return _REG.get(regiao, {}).get(tag) or _BASE.get(tag, [])
