/**
 * Vinhetas SVG do redesenho "Nocturne". Puro enfeite -- nenhum dado do
 * jogo mora aqui, so o key de regiao/local escolhe qual cena aparece.
 */

// Cena de abertura da tela de regioes.
export const CENA_HERO = `
<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Fim de tarde na rua, isopor no chao e duas criancas com dindin na mao">
  <rect width="400" height="300" fill="#1a1d2c"></rect>
  <circle cx="286" cy="106" r="48" fill="#e8c07a" opacity="0.9"></circle>
  <circle cx="286" cy="106" r="72" fill="#e8c07a" opacity="0.08"></circle>
  <path d="M0,198 V166 H28 V148 H60 V174 H94 V140 H122 V158 H152 V130 H188 V162 H216 V148 H252 V170 H288 V144 H324 V166 H358 V154 H400 V198 Z" fill="#232739"></path>
  <g fill="#e8c07a" opacity="0.45">
    <rect x="36" y="156" width="5" height="6"></rect>
    <rect x="68" y="182" width="5" height="6"></rect>
    <rect x="100" y="150" width="5" height="6"></rect>
    <rect x="160" y="140" width="5" height="6"></rect>
    <rect x="196" y="172" width="5" height="6"></rect>
    <rect x="296" y="154" width="5" height="6"></rect>
    <rect x="332" y="176" width="5" height="6"></rect>
  </g>
  <rect y="196" width="400" height="104" fill="#262a3b"></rect>
  <path d="M0,210 H400" stroke="#383e56" stroke-width="2"></path>
  <ellipse cx="120" cy="258" rx="86" ry="8" fill="#171a26"></ellipse>
  <rect x="52" y="214" width="104" height="44" rx="7" fill="#1b1f2c"></rect>
  <rect x="46" y="204" width="116" height="13" rx="5" fill="#333852"></rect>
  <rect x="94" y="198" width="20" height="8" rx="4" fill="#434a66"></rect>
  <g fill="#9184d9">
    <rect x="64" y="228" width="10" height="22" rx="5"></rect>
    <rect x="80" y="228" width="10" height="22" rx="5" opacity="0.6"></rect>
  </g>
  <g fill="#c98b8b"><rect x="96" y="228" width="10" height="22" rx="5" opacity="0.85"></rect></g>
  <g fill="#8fd3a6"><rect x="112" y="228" width="10" height="22" rx="5" opacity="0.7"></rect></g>
  <g fill="#0e1018">
    <circle cx="232" cy="150" r="21"></circle>
    <path d="M211,258 V200 a21,21 0 0 1 42,0 v58 Z"></path>
    <path d="M250,206 L266,166" stroke="#0e1018" stroke-width="11" stroke-linecap="round"></path>
    <circle cx="306" cy="166" r="17"></circle>
    <path d="M289,258 V210 a17,17 0 0 1 34,0 v48 Z"></path>
    <path d="M292,216 L278,186" stroke="#0e1018" stroke-width="9" stroke-linecap="round"></path>
  </g>
  <rect x="262" y="140" width="13" height="34" rx="6.5" fill="#9184d9" transform="rotate(14 268 157)"></rect>
  <rect x="272" y="160" width="13" height="30" rx="6.5" fill="#e8c07a" opacity="0.9" transform="rotate(-18 278 175)"></rect>
</svg>`;

// Uma vinheta de fundo por regiao, pro cartao de escolha.
export const CENA_REGIAO = {
  ce: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ceara: calcada de sol a pino, mandacaru">
  <rect width="320" height="112" fill="#1f2130"></rect>
  <circle cx="244" cy="42" r="31" fill="#e8c07a" opacity="0.9"></circle>
  <rect y="80" width="320" height="32" fill="#262a3b"></rect>
  <rect x="56" y="32" width="15" height="48" rx="7.5" fill="#343a52"></rect>
  <path d="M56,58 h-11 v-13" stroke="#343a52" stroke-width="10" fill="none" stroke-linecap="round"></path>
  <path d="M71,52 h11 v-16" stroke="#343a52" stroke-width="10" fill="none" stroke-linecap="round"></path>
  <path d="M120,80 h22 M156,80 h14 M286,80 h20" stroke="#383e56" stroke-width="3"></path>
  <path d="M196,80 V62 h34 v18 Z" fill="#2e3342"></path>
  <path d="M192,62 L213,50 L234,62 Z" fill="#3a4058"></path>
</svg>`,
  rj: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Rio: morro, mar e guarda-sol">
  <rect width="320" height="112" fill="#1b2233"></rect>
  <circle cx="62" cy="38" r="24" fill="#e8c07a" opacity="0.85"></circle>
  <path d="M172,84 C196,24 218,18 242,84 Z" fill="#232c40"></path>
  <path d="M240,84 C258,48 274,44 292,84 Z" fill="#1d2537"></path>
  <rect y="82" width="320" height="30" fill="#101a28"></rect>
  <path d="M12,92 q10,-6 20,0 t20,0 M60,100 q10,-6 20,0 t20,0 M128,92 q10,-6 20,0 t20,0" stroke="#2c3a52" stroke-width="2.5" fill="none"></path>
  <path d="M44,82 L100,82" stroke="#343a52" stroke-width="3"></path>
  <path d="M46,58 q26,-16 52,0 Z" fill="#9184d9" opacity="0.8"></path>
  <rect x="70" y="56" width="3" height="28" fill="#343a52"></rect>
</svg>`,
  mg: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Minas: igreja no morro e rua de paralelepipedo">
  <rect width="320" height="112" fill="#1e2030"></rect>
  <circle cx="268" cy="34" r="22" fill="#e8c07a" opacity="0.7"></circle>
  <path d="M0,88 C80,52 190,64 320,82 V112 H0 Z" fill="#262a3b"></path>
  <rect x="138" y="36" width="18" height="42" fill="#343a52"></rect>
  <path d="M134,36 L147,22 L160,36 Z" fill="#343a52"></path>
  <rect x="145" y="10" width="3" height="12" fill="#343a52"></rect>
  <rect x="140" y="14" width="13" height="3" fill="#343a52"></rect>
  <path d="M120,78 V56 h18 v22 Z M156,78 V56 h18 v22 Z" fill="#2e3342"></path>
  <rect x="144" y="48" width="6" height="8" fill="#e8c07a" opacity="0.5"></rect>
  <g fill="#1a1c28">
    <ellipse cx="24" cy="102" rx="11" ry="5"></ellipse>
    <ellipse cx="56" cy="104" rx="11" ry="5"></ellipse>
    <ellipse cx="88" cy="101" rx="11" ry="5"></ellipse>
    <ellipse cx="124" cy="104" rx="11" ry="5"></ellipse>
    <ellipse cx="160" cy="102" rx="11" ry="5"></ellipse>
    <ellipse cx="196" cy="104" rx="11" ry="5"></ellipse>
    <ellipse cx="232" cy="101" rx="11" ry="5"></ellipse>
    <ellipse cx="268" cy="104" rx="11" ry="5"></ellipse>
    <ellipse cx="302" cy="102" rx="11" ry="5"></ellipse>
  </g>
</svg>`,
  sp: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Sao Paulo: quintal de periferia, casas de tijolo e roupa no varal">
  <rect width="320" height="112" fill="#1c1e2b"></rect>
  <g fill="#23262f">
    <rect x="10" y="40" width="58" height="46"></rect>
    <rect x="72" y="24" width="52" height="62"></rect>
    <rect x="128" y="48" width="46" height="38"></rect>
    <rect x="178" y="30" width="56" height="56"></rect>
    <rect x="238" y="52" width="70" height="34"></rect>
  </g>
  <g fill="#2e3342">
    <rect x="84" y="14" width="16" height="12" rx="3"></rect>
    <rect x="192" y="20" width="16" height="12" rx="3"></rect>
  </g>
  <g fill="#e8c07a" opacity="0.45">
    <rect x="24" y="54" width="7" height="9"></rect>
    <rect x="94" y="44" width="7" height="9"></rect>
    <rect x="140" y="62" width="7" height="9"></rect>
    <rect x="200" y="50" width="7" height="9"></rect>
    <rect x="264" y="66" width="7" height="9"></rect>
  </g>
  <path d="M0,36 Q160,56 320,34" stroke="#3a4058" stroke-width="1.5" fill="none"></path>
  <rect x="60" y="46" width="14" height="20" rx="2" fill="#9184d9" opacity="0.75"></rect>
  <rect x="134" y="50" width="12" height="17" rx="2" fill="#b2b6ca" opacity="0.5"></rect>
  <rect x="210" y="46" width="14" height="19" rx="2" fill="#c98b8b" opacity="0.6"></rect>
  <rect y="86" width="320" height="26" fill="#262a3b"></rect>
</svg>`,
  rs: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Rio Grande do Sul: praca de verao, arvores e banco">
  <rect width="320" height="112" fill="#1d2130"></rect>
  <circle cx="52" cy="86" r="30" fill="#191c27"></circle>
  <rect x="49" y="82" width="7" height="22" fill="#343a52"></rect>
  <circle cx="252" cy="80" r="24" fill="#191c27"></circle>
  <rect x="249" y="76" width="6" height="28" fill="#343a52"></rect>
  <rect y="98" width="320" height="14" fill="#262a3b"></rect>
  <rect x="140" y="34" width="4" height="64" fill="#343a52"></rect>
  <circle cx="142" cy="30" r="9" fill="#e8c07a" opacity="0.85"></circle>
  <circle cx="142" cy="30" r="20" fill="#e8c07a" opacity="0.1"></circle>
  <rect x="168" y="82" width="62" height="5" rx="2" fill="#333852"></rect>
  <rect x="168" y="70" width="62" height="5" rx="2" fill="#333852"></rect>
  <rect x="172" y="82" width="4" height="16" fill="#343a52"></rect>
  <rect x="222" y="82" width="4" height="16" fill="#343a52"></rect>
</svg>`,
  pa: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Para: feira coberta e chuva de fim de tarde">
  <rect width="320" height="112" fill="#191d2a"></rect>
  <g opacity="0.5" stroke="#3a4157" stroke-width="1.5">
    <path d="M18,6 L8,34"></path><path d="M64,0 L54,30"></path>
    <path d="M112,10 L102,38"></path><path d="M168,2 L158,32"></path>
    <path d="M226,8 L216,36"></path><path d="M286,0 L276,28"></path>
    <path d="M40,44 L30,66"></path><path d="M204,46 L194,68"></path>
    <path d="M302,44 L292,68"></path>
  </g>
  <path d="M8,58 q30,-24 60,0 Z" fill="#262a3b"></path>
  <path d="M74,58 q30,-24 60,0 Z" fill="#2e3344"></path>
  <path d="M140,58 q30,-24 60,0 Z" fill="#262a3b"></path>
  <path d="M206,58 q30,-24 60,0 Z" fill="#2e3344"></path>
  <path d="M8,58 H266" stroke="#9184d9" stroke-width="2" opacity="0.55"></path>
  <g fill="#343a52">
    <rect x="20" y="58" width="4" height="30"></rect>
    <rect x="100" y="58" width="4" height="30"></rect>
    <rect x="180" y="58" width="4" height="30"></rect>
    <rect x="256" y="58" width="4" height="30"></rect>
  </g>
  <rect y="86" width="320" height="26" fill="#22273a"></rect>
  <path d="M24,98 H88 M120,104 H182 M220,98 H288" stroke="#9184d9" stroke-width="2" opacity="0.25"></path>
</svg>`,
};

// Cena do ponto de venda, uma por local (tela do dia). "casa" e "escola"
// e "carrinho" nao tem vinheta propria no mockup original -- reaproveitam
// a arte mais proxima em espirito (rua/feira) em vez de inventar do zero.
export const CENA_LOCAL = {
  isopor: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Isopor na calcada, fim de tarde">
  <rect width="160" height="128" fill="#1f2130"></rect>
  <circle cx="128" cy="30" r="20" fill="#e8c07a" opacity="0.85"></circle>
  <rect y="70" width="160" height="20" fill="#262a3b"></rect>
  <rect x="34" y="30" width="15" height="46" rx="7.5" fill="#343a52"></rect>
  <path d="M34,54 h-11 v-12" stroke="#343a52" stroke-width="9" fill="none" stroke-linecap="round"></path>
  <rect y="90" width="160" height="38" fill="#262a3b"></rect>
  <ellipse cx="86" cy="118" rx="30" ry="5" fill="#191c28"></ellipse>
  <rect x="66" y="94" width="40" height="22" rx="4" fill="#1f2433"></rect>
  <rect x="63" y="88" width="46" height="7" rx="3" fill="#2d3246"></rect>
</svg>`,
  praia: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="O ponto: guarda-sol na areia, mar ao fundo">
  <rect width="160" height="128" fill="#1b2233"></rect>
  <circle cx="122" cy="34" r="20" fill="#e8c07a" opacity="0.9"></circle>
  <circle cx="122" cy="34" r="32" fill="#e8c07a" opacity="0.1"></circle>
  <rect y="66" width="160" height="24" fill="#101a28"></rect>
  <path d="M6,74 q9,-5 18,0 t18,0 M96,80 q9,-5 18,0 t18,0" stroke="#2c3a52" stroke-width="2" fill="none"></path>
  <rect y="88" width="160" height="40" fill="#262a3b"></rect>
  <path d="M14,56 q34,-26 68,0 Z" fill="#9184d9" opacity="0.85"></path>
  <path d="M48,56 V104" stroke="#343a52" stroke-width="4"></path>
  <rect x="86" y="92" width="40" height="22" rx="4" fill="#1f2433"></rect>
  <rect x="83" y="86" width="46" height="7" rx="3" fill="#2d3246"></rect>
  <ellipse cx="106" cy="118" rx="30" ry="5" fill="#191c28"></ellipse>
</svg>`,
  escola: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Portao da escola, fim de aula">
  <rect width="160" height="128" fill="#1e2030"></rect>
  <circle cx="128" cy="30" r="18" fill="#e8c07a" opacity="0.7"></circle>
  <rect x="20" y="30" width="120" height="46" fill="#262a3b"></rect>
  <g fill="#343a52">
    <rect x="34" y="42" width="14" height="18"></rect>
    <rect x="62" y="42" width="14" height="18"></rect>
    <rect x="90" y="42" width="14" height="18"></rect>
    <rect x="118" y="42" width="14" height="18"></rect>
  </g>
  <rect y="76" width="160" height="18" fill="#191c28"></rect>
  <rect y="94" width="160" height="34" fill="#262a3b"></rect>
  <rect x="68" y="98" width="34" height="20" rx="4" fill="#1f2433"></rect>
</svg>`,
  carrinho: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Carrinho proprio na rua">
  <rect width="160" height="128" fill="#1c1e2b"></rect>
  <circle cx="126" cy="28" r="18" fill="#e8c07a" opacity="0.75"></circle>
  <rect y="88" width="160" height="18" fill="#191c28"></rect>
  <rect y="106" width="160" height="22" fill="#262a3b"></rect>
  <rect x="46" y="60" width="68" height="34" rx="6" fill="#333852"></rect>
  <rect x="42" y="52" width="76" height="10" rx="4" fill="#434a66"></rect>
  <circle cx="60" cy="100" r="8" fill="#0e1018"></circle>
  <circle cx="100" cy="100" r="8" fill="#0e1018"></circle>
</svg>`,
  casa: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Freezer de casa, cozinha simples">
  <rect width="160" height="128" fill="#1c1e2b"></rect>
  <rect x="46" y="20" width="68" height="88" rx="6" fill="#232739"></rect>
  <rect x="46" y="20" width="68" height="34" rx="6" fill="#2b3049"></rect>
  <rect x="94" y="34" width="6" height="10" rx="3" fill="#5b5e70"></rect>
  <rect x="94" y="78" width="6" height="10" rx="3" fill="#5b5e70"></rect>
  <g fill="#e8c07a" opacity="0.5">
    <rect x="58" y="66" width="6" height="8"></rect>
    <rect x="72" y="90" width="6" height="8"></rect>
  </g>
</svg>`,

  rua: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Menino vendendo na rua movimentada, isopor no chao">
  <rect width="160" height="128" fill="#1f212f"></rect>
  <circle cx="118" cy="32" r="19" fill="#e8c07a" opacity="0.8"></circle>
  <rect y="78" width="160" height="22" fill="#262a3b"></rect>
  <path d="M12 82 L148 82" stroke="#383e56" stroke-width="3"></path>
  <rect x="22" y="48" width="52" height="38" rx="4" fill="#2c3348"></rect>
  <rect x="28" y="52" width="18" height="28" rx="2" fill="#1a1d2c"></rect>
  <g fill="#e8c07a" opacity="0.6">
    <rect x="78" y="55" width="6" height="22"></rect>
    <rect x="88" y="52" width="6" height="26"></rect>
  </g>
  <circle cx="68" cy="92" r="7" fill="#11141f"></circle>
  <circle cx="112" cy="92" r="7" fill="#11141f"></circle>
</svg>`,

  feira: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Feira movimentada com barracas de frutas e isopor">
  <rect width="160" height="128" fill="#1e1f2c"></rect>
  <circle cx="115" cy="28" r="21" fill="#e8c07a" opacity="0.75"></circle>
  <rect y="72" width="160" height="28" fill="#25293a"></rect>
  <rect x="8" y="38" width="38" height="42" rx="3" fill="#343a52"></rect>
  <rect x="52" y="36" width="34" height="46" rx="3" fill="#2a3046"></rect>
  <g fill="#e8b76a" opacity="0.9">
    <circle cx="22" cy="52" r="6"></circle>
    <circle cx="32" cy="48" r="7"></circle>
    <circle cx="68" cy="49" r="8"></circle>
  </g>
  <rect x="96" y="55" width="42" height="26" rx="4" fill="#1c2233"></rect>
  <path d="M12 82 L148 82" stroke="#3f475f" stroke-width="4"></path>
</svg>`,

  cozinha: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Cozinha simples ao amanhecer, panelas no fogao">
  <rect width="160" height="128" fill="#1a1d29"></rect>
  <rect x="18" y="38" width="118" height="52" rx="4" fill="#252a3a"></rect>
  <rect x="32" y="22" width="22" height="18" rx="2" fill="#3a4259"></rect>
  <rect x="78" y="48" width="48" height="12" fill="#4a2c1f"></rect>
  <g fill="#e8c07a" opacity="0.55">
    <rect x="38" y="68" width="9" height="18"></rect>
    <rect x="52" y="65" width="9" height="22"></rect>
    <rect x="112" y="71" width="11" height="14"></rect>
  </g>
  <rect y="92" width="160" height="36" fill="#1f2433"></rect>
  <rect x="68" y="98" width="28" height="22" rx="3" fill="#2c3348"></rect>
</svg>`,
};

// Cena de fechamento da tela de relatorio (isopor quase vazio).
export const CENA_RELATORIO = `
<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Fim de tarde na praia, isopor aberto e quase vazio">
  <rect width="400" height="260" fill="#1b2233"></rect>
  <circle cx="298" cy="118" r="40" fill="#e8c07a" opacity="0.85"></circle>
  <circle cx="298" cy="118" r="66" fill="#e8c07a" opacity="0.09"></circle>
  <rect y="146" width="400" height="34" fill="#101a28"></rect>
  <path d="M282,150 q16,-6 34,0 t34,0" stroke="#e8c07a" stroke-width="2" opacity="0.35" fill="none"></path>
  <path d="M20,158 q12,-6 24,0 t24,0 M120,168 q12,-6 24,0 t24,0" stroke="#2c3a52" stroke-width="2.5" fill="none"></path>
  <rect y="178" width="400" height="82" fill="#262a3b"></rect>
  <path d="M0,192 H400" stroke="#383e56" stroke-width="2"></path>
  <ellipse cx="150" cy="238" rx="92" ry="10" fill="#1b1f2c"></ellipse>
  <rect x="86" y="200" width="118" height="42" rx="7" fill="#1b1f2c"></rect>
  <path d="M84,200 L204,200 L228,172 L112,172 Z" fill="#333852"></path>
  <rect x="104" y="210" width="11" height="22" rx="5.5" fill="#9184d9" opacity="0.5"></rect>
  <rect x="122" y="210" width="11" height="22" rx="5.5" fill="#c98b8b" opacity="0.35"></rect>
  <path d="M246,242 V204 a14,14 0 0 1 28,0 v38 Z" fill="#0e1018"></path>
  <circle cx="260" cy="184" r="14" fill="#0e1018"></circle>
  <path d="M272,208 L288,190" stroke="#0e1018" stroke-width="8" stroke-linecap="round"></path>
  <rect x="284" y="172" width="11" height="26" rx="5.5" fill="#8fd3a6" opacity="0.8" transform="rotate(16 289 185)"></rect>
</svg>`;

export function cenaLocal(key) {
  return CENA_LOCAL[key] ?? CENA_LOCAL.isopor;
}

export function cenaRegiao(key) {
  return CENA_REGIAO[key] ?? CENA_REGIAO.ce;
}
