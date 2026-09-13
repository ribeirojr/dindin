"""Base pt-BR neutra. Cada regiao sobrescreve o que muda."""

BASE: dict[str, str] = {
    # --- produto ---
    "produto.sing": "picolé de saquinho",
    "produto.plur": "picolés de saquinho",
    "produto.artigo": "o",

    # --- interjeicoes e vocativo ---
    "interj.surpresa": "Nossa",
    "interj.positivo": "Muito bom",
    "interj.negativo": "Que pena",
    "vocativo": "amigo",
    "gente": "o pessoal",

    # --- navegacao ---
    "ui.titulo": "DINDIN",
    "ui.subtitulo": "a vida de quem vende gelado no Brasil",
    "ui.novo_jogo": "Jogo novo",
    "ui.continuar": "Continuar",
    "ui.ajuda": "Como se joga",
    "ui.sair": "Sair",
    "ui.voltar": "Voltar",
    "ui.confirmar": "Confirmar",
    "ui.bora": "Bora!",
    "ui.proximo_dia": "Próximo dia",
    "ui.modo_bandeira": "Modo bandeira",
    "ui.modo_noite": "Modo noite",
    "ui.escolha_regiao": "De onde você é?",
    "ui.dia": "Dia",
    "ui.caixa": "Caixa",
    "ui.reputacao": "Reputação",
    "ui.meta": "Meta do capítulo",
    "ui.ponto": "Ponto de venda",
    "ui.clima_amanha": "Previsão de hoje",
    "ui.menu": "Mais opções",
    "ui.trocar_regiao": "Trocar de região",

    # --- repl de python ---
    "repl.menu_link": "🐍 Aprenda Python",
    "repl.titulo": "Python no navegador",
    "repl.subtitulo": "Digite um comando Python e aperte Enter para rodar. "
                       "É o mesmo Python que roda o jogo — de verdade, sem servidor.",
    "repl.placeholder": "digite aqui e aperte Enter...",
    "repl.rodar": "Rodar",
    "repl.limpar": "Limpar",
    "repl.reiniciar": "Reiniciar",
    "repl.reiniciado": "Python reiniciado. Todas as variáveis foram apagadas.",
    "repl.bem_vindo": "Python {versao} pronto. Digite algo como {exemplo} e aperte Enter.",
    "repl.dica_setas": "Dica: use ↑ e ↓ para repetir comandos anteriores.",
    "repl.exemplos_titulo": "Exemplos pra começar",

    # --- feira ---
    "feira.titulo": "Feira",
    "feira.subtitulo": "Compre os insumos do dia",
    "feira.insumo": "Insumo",
    "feira.unidade": "Unidade",
    "feira.preco": "Preço",
    "feira.validade": "Validade",
    "feira.estoque": "Tem em casa",
    "feira.carrinho": "No carrinho",
    "feira.total": "Total da compra",
    "feira.desconto": "Comprando mais, sai mais barato.",
    "feira.sem_dinheiro": "Não tem caixa pra essa compra.",

    # --- cozinha ---
    "cozinha.titulo": "Cozinha",
    "cozinha.subtitulo": "Quantos você vai fazer hoje?",
    "cozinha.sabor": "Sabor",
    "cozinha.custo": "Custo por unidade",
    "cozinha.maximo": "Dá pra fazer",
    "cozinha.produzir": "Fazer",
    "cozinha.freezer": "Freezer",
    "cozinha.freezer_cheio": "Passou da capacidade! O que sobrar vai derreter.",
    "cozinha.pronto": "Já congelado",

    # --- preco ---
    "preco.titulo": "Preço",
    "preco.subtitulo": "Por quanto você vai vender?",
    "preco.sabor": "Sabor",
    "preco.custo": "Custo",
    "preco.preco": "Preço",
    "preco.margem": "Margem",
    "preco.termometro": "Como o povo vê o preço",
    "preco.barato": "de graça",
    "preco.justo": "tá justo",
    "preco.salgado": "tá salgado",
    "preco.caro": "tá caro demais",
    "preco.absurdo": "ninguém paga isso",

    # --- dia / relatorio ---
    "dia.vendendo": "Vendendo...",
    "dia.fim": "Fim do dia",
    "rel.titulo": "Como foi o dia",
    "rel.sabor": "Sabor",
    "rel.levou": "Levou",
    "rel.vendeu": "Vendeu",
    "rel.queria": "Queriam comprar",
    "rel.receita": "Receita",
    "rel.custos": "Custos",
    "rel.lucro": "Lucro",
    "rel.prejuizo": "Prejuízo",
    "rel.derreteu": "Derreteu",
    "rel.sellout": "Vendeu tudo! {perdidos} pessoas ficaram na vontade.",
    "rel.sobrou": "Sobraram {sobra} unidades no isopor.",
    "rel.chuva": "Choveu e a rua ficou vazia.",
    "rel.nada_vendido": "Não vendeu nada hoje.",

    # --- resumo do dia: um veredito curto, o fecho do relatorio ---
    "resumo.nada_pra_vender": "Hoje ninguém levou nada pro ponto — dia perdido antes de começar.",
    "resumo.zero_venda": "Ficou parado o dia inteiro. Amanhã é outro dia.",
    "resumo.derreteu_muito": "O calor venceu: mais derreteu do que vendeu. Faltou gelo.",
    "resumo.faltou_estoque": "Vendeu tudo rapidinho e sobrou gente querendo. Bora fazer mais.",
    "resumo.prejuizo": "No vermelho hoje — o caixa encolheu, mas a praça continua.",
    "resumo.sellout_limpo": "Levou certinho, vendeu tudo, ninguém ficou na mão. Redondo.",
    "resumo.lucro_forte": "Dia gordo! O lucro comeu boa parte da receita.",
    "resumo.dia_normal": "Um dia como outro qualquer: vendeu, pagou as contas, seguiu.",

    # --- capitulos ---
    "local.casa": "Freezer de casa",
    "local.isopor": "Isopor na rua",
    "local.praia": "Praia",
    "local.escola": "Portão da escola",
    "local.carrinho": "Carrinho próprio",
    "cap.desbloqueou": "Novo ponto liberado!",
    "cap.entrada": "Custo pra começar lá",
    "cap.vitoria": "Você conseguiu!",
    "cap.falencia": "Acabou o dinheiro.",

    # --- eventos ---
    "evento.isopor_acabou": "Seu {nome} rachou de vez. Precisa comprar outro.",
    "evento.isopor_acabando": "O {nome} tá nas últimas ({dias} dias).",
    "evento.queda_energia": "Faltou luz! Derreteu {perdidos} unidades.",
    "evento.queda_energia_gerador": "Faltou luz, mas o gerador segurou.",
    "evento.freezer_pifou": "O freezer pifou. Conserto: R$ {valor}.",
    "evento.fiscal": "Passou o fiscal. Multa de R$ {valor}.",
    "evento.saquinho_furado": "Saquinho furado, perdeu {perdidos} unidades.",
    "evento.jogo_do_brasil": "Jogo do Brasil! A rua encheu.",
    "evento.obra_na_rua": "Obra na rua espantou a freguesia.",
    "evento.excursao": "Chegou excursão! Movimento dobrado.",
    "evento.concorrente": "Apareceu outro vendedor no mesmo ponto.",
    "evento.elogio_bairro": "Falaram bem de você no bairro.",
    "evento.feira_promocao": "Promoção na feira! Economizou R$ {valor}.",
    "evento.seca_forte": "Seca braba, calor de rachar.",
    "evento.festa_padroeira": "Festa da padroeira, cidade cheia.",
    "evento.carnaval_bloco": "Bloco passou na sua rua!",
    "evento.temporal_carioca": "Temporal! Todo mundo correu.",
    "evento.festa_junina_mg": "Festa junina na praça.",
    "evento.quermesse": "Quermesse na igreja.",
    "evento.onda_calor_sp": "Onda de calor na cidade.",
    "evento.greve_transporte": "Greve de ônibus, ninguém saiu de casa.",
    "evento.minuano": "Minuano gelado, ninguém quer gelado.",
    "evento.semana_farroupilha": "Semana Farroupilha, movimento bom.",
    "evento.cirio_nazare": "Círio! A cidade inteira na rua.",
    "evento.chuva_das_duas": "Chuva das duas, na hora certa.",
    "evento.seca_do_cerrado": "Seca do cerrado: meses sem chuva, ar seco de rachar.",
    "evento.greve_servidor": "Greve de servidor público — meio-dia e a cidade tá na rua.",
    "evento.carnaval": "Carnaval!",
    "evento.sao_joao": "São João!",
    "evento.sao_pedro": "São Pedro!",
    "evento.mes_junino": "Mês de festa junina.",
    "evento.ferias": "Férias escolares.",
    "evento.dia_criancas": "Dia das Crianças!",
    "evento.dia_namorados": "Dia dos Namorados.",
    "evento.independencia": "Feriado da Independência.",
    "evento.natal": "Natal, todo mundo em casa.",
    "evento.ano_novo": "Ano novo, cidade parada.",

    # --- clima ---
    "clima.escaldante": "sol de rachar",
    "clima.quente": "quente",
    "clima.abafado": "abafado",
    "clima.nublado": "nublado",
    "clima.chuva": "chuva",
    "clima.temporal": "temporal",
    "clima.frio": "frio",
    "clima.sensacao": "sensação",
    "clima.dica.temporal": "Temporal. Quase ninguém na rua.",
    "clima.dica.chuva": "Chuva. Movimento fraco.",
    "clima.dica.frio": "Frio. Ninguém quer gelado.",
    "clima.dica.calorao": "Calor forte! Vai vender muito — e dá pra cobrar mais.",
    "clima.dica.bom": "Movimento bom.",
    "clima.dica.normal": "Movimento normal.",

    # --- web: telas ---
    "regiao.subtitulo": "O doce muda de nome em cada estado — e o clima, "
                        "o gosto e o preço mudam junto.",
    "regiao.sai_muito": "Sai muito",
    "ui.escolha_regiao": "Escolha uma cidade para jogar!",
    "ui.fama": "Fama",
    "ui.no_caixa": "No caixa",
    "ui.meta_curta": "Meta",
    "ui.faltam": "faltam {v}",
    "ui.meta_batida": "batida!",
    "ui.sabores": "Sabores",
    "ui.congelado": "Congelado",
    "ui.antes": "Antes de começar: veja como está o dia.",
    "ui.vender": "Vender! →",
    "ui.denovo": "Jogar de novo",
    "ui.comprar": "Comprar",
    "ui.falta_dinheiro": "Falta dinheiro",
    "ui.gelo": "Gelo",
    "ui.isopor": "Isopor",
    "dica.casa": "Comece pequeno: faça poucos e veja quantos a vizinhança quer.",
    "dica.isopor": "Na rua o movimento é bem maior — mas chuva esvazia a calçada.",
    "dica.praia": "Praia paga mais caro e adora cremoso. Só que chuva aqui é fatal.",
    "dica.escola": "Criança tem pouco dinheiro: aqui o barato vende, o gourmet encalha.",
    "dica.carrinho": "Seu ponto, suas regras. Olhe a previsão e escolha o dia certo.",

    # --- web: isopor ---
    "isopor.em_uso": "Em uso",
    "isopor.dura_mais": "Dura mais",
    "isopor.capacidade": "Capacidade",
    "isopor.dias_valor": "{n} dia(s)",
    "isopor.acabando": "O isopor tá no fim. Vale já comprar outro.",
    "isopor.precisa": "Sem isopor não dá pra vender na rua. Ele dura vários dias.",
    "isopor.det1": "{dias} dias · cabe {cap}",
    "isopor.det2": "{custo}/dia · derrete {pct}%",

    # --- web: feira e cozinha ---
    "feira.tem": "Tem",
    "feira.levar": "Levar",
    "feira.falta": "Falta {v} — tire alguma coisa do carrinho.",
    "feira.resumo": "Compra: {c} · sobra {s}",
    "cozinha.pronto_curto": "Pronto",
    "cozinha.maximo_curto": "Máx.",
    "cozinha.pra10": "Pra fazer 10 {plur}:",
    "cozinha.tem": "(tem {n})",
    "cozinha.falta": "Falta comprar: {lista}",
    "cozinha.tem_tudo": "Tem tudo que precisa.",
    "cozinha.cabe": "Cabe {n} no freezer. O que passar disso derrete.",

    # --- web: preco e gelo ---
    "preco.curva": "A curva mostra quantos compram em cada preço. "
                   "O losango é o preço de maior lucro.",
    "preco.melhor": "melhor preço",
    "preco.compram": "{pct}% compram · margem",
    "preco.vazio": "Faça alguma coisa na cozinha primeiro.",
    "gelo.vai": "Vai pro isopor",
    "gelo.cobre": "Um saco cobre",
    "gelo.calor": "calor: era {n}",
    "gelo.saco": "Saco",
    "gelo.sacos": "{n} saco(s)",
    "gelo.derrete": "Derrete {n} unidade(s) — gelo de menos.",
    "gelo.tudo": "Dá pra tudo. Nada derrete.",
    "gelo.nada": "Nada pra gelar ainda.",
    "gelo.atalho": "Levar {n} e não perder nada",

    # --- web: barra lateral do dia ---
    "dia.resumo_titulo": "O dia até agora",
    "dia.resumo_feira": "Compra na feira",
    "dia.resumo_gelo": "Gelo",
    "dia.resumo_vai": "Vai pro isopor",
    "dia.resumo_sobra": "Sobra no caixa",

    # --- web: relatorio e fim ---
    "rel.na_fila": "Na fila",
    "rel.queria_curto": "Queriam",
    "rel.derreteu_aviso": "Derreteu {n} unidade(s). Mais gelo "
                          "(ou um isopor melhor) segura o estoque.",
    "rel.nada_casa": "Nada foi pro ponto hoje — faltou sabor pronto e com preço.",
    "rel.nada_rua": "Nada chegou ao ponto: sem isopor vivo "
                    "(ou tudo derreteu antes).",
    "cap.det": "entrada {v}, movimento {n}/dia.",
    "cap.mudar": "Mudar pra {nome}",
    "fim.resumo": "{d} dias · caixa {c} · fama {f}",

    # --- jornada / backup (salva a viagem do isopor) ---
    "jornada.salvar": "Bora salvar essa jornada arretada, ma broca? Isopor cheio de dindin bom, égua!",
    "jornada.baixar": "Baixar o save do dia",
    "jornada.carregar": "Carregar jornada salva",
    "jornada.instrucao": "Arraste o dindin-diaXX-ABCDEF.json aqui (ou clique). Salva no fim de cada dia após vender — continua de onde parou sem derreter o lucro.",
    "jornada.toast_salvo": "Jornada guardada! O isopor tá seguro na memória, vixe.",
    "jornada.toast_carregado": "Jornada restaurada. Bora pro próximo dia, meu consagrado!",
    "jornada.erro": "Arquivo inválido. Só saves do Dindin (dindin-dia*.json).",
    "jornada.ajuda": "Salva a viagem do seu isopor pelo Brasil, parça.",

    # --- campanha: cada regiao e um cenario pra vencer ---
    "campanha.vencida": "vencida",
    "campanha.placar": "{n} de {total} regiões vencidas",
    "campanha.conquistou": "Você dominou o {nome}! {n} de {total} regiões vencidas.",
    "campanha.zerou": "Você venceu o Brasil inteiro!",
    "campanha.escolher_outra": "Escolher outra região",
}


def _nomes_do_conteudo() -> dict[str, str]:
    """Nomes de sabores, insumos e isopores viram chaves i18n.

    Em pt eles JA vivem em content/ (fonte da verdade); aqui viram chave pra
    ingles poder traduzir sem duplicar nada no lado portugues.
    """
    from ..content.coolers import ISOPORES
    from ..content.flavors import SABORES
    from ..content.ingredients import INSUMOS

    nomes: dict[str, str] = {}
    for k, f in SABORES.items():
        nomes[f"sabor.{k}"] = f.nome
    for k, i in INSUMOS.items():
        nomes[f"insumo.{k}"] = i.nome
        nomes[f"insumo.unidade.{k}"] = i.unidade
    for k, c in ISOPORES.items():
        nomes[f"isopor.nome.{k}"] = c.nome
        nomes[f"isopor.desc.{k}"] = c.descricao
    return nomes


BASE.update(_nomes_do_conteudo())
