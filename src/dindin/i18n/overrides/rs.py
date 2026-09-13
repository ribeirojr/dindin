"""Rio Grande do Sul: gelinho, 'bah', 'tchê', 'guria', 'capaz'."""

OVERRIDE: dict[str, str] = {
    "evento.isopor_acabou": "Bah, o {nome} rachou de vez, tchê. Tem que comprar outro.",
    "produto.sing": "gelinho",
    "produto.plur": "gelinhos",
    "interj.surpresa": "Bah",
    "interj.positivo": "Tri bom",
    "interj.negativo": "Bah, que trágico",
    "vocativo": "tchê",
    "gente": "a gurizada",
    "ui.subtitulo": "a vida de quem vende gelinho no Rio Grande",
    "ui.escolha_regiao": "Escolhe o lugar pra jogar, tchê?",
    "ui.bora": "Bora, tchê!",
    "cozinha.subtitulo": "Quantos gelinhos tu vai fazer hoje?",
    "preco.subtitulo": "Por quanto tu vai vender, tchê?",
    "preco.barato": "tá de graça",
    "preco.justo": "tá tri",
    "preco.salgado": "tá salgado, tchê",
    "preco.caro": "bah, tá caro",
    "preco.absurdo": "capaz que alguém paga isso",
    "rel.sellout": "Bah, tri! Vendeu tudo — {perdidos} ficaram na vontade.",
    "rel.chuva": "Bah, choveu. Não veio ninguém.",
    "rel.nada_vendido": "Não vendeu nada hoje, tchê.",
    "cap.desbloqueou": "Bah! Ponto novo liberado, tchê!",
    "cap.vitoria": "Tu conseguiu, tchê! Tri demais!",
    "evento.minuano": "Bah, o minuano baixou. Ninguém quer gelado.",
    "evento.semana_farroupilha": "Semana Farroupilha, tchê. Movimento tri bom.",
    # Porto Alegre fica no Guaiba (rio/lago), nao no litoral. Capitulo 3
    # vira a Orla do Guaiba em vez de uma praia de mar.
    "local.praia": "Orla do Guaíba",
    "dica.praia": "O gaúcho vem ver o pôr do sol e tomar chimarrão na Orla "
                  "— mas sol forte de tarde esvazia tudo, ninguém troca a "
                  "sombra por sorvete.",
}
