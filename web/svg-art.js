/**
 * Vinhetas SVG do redesenho "Nocturne". Puro enfeite -- nenhum dado do
 * jogo mora aqui, so o key de regiao/local (e o tema claro/escuro) escolhe
 * qual cena aparece. Cada cena tem uma paleta escura (padrao, noturna) e
 * uma clara ("modo bandeira": verde/amarelo/azul da bandeira do Brasil).
 */

// Cena de abertura da tela de regioes.
export const CENA_HERO = {
  escuro: `
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
</svg>`,
  claro: `
<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Meio-dia na rua: arvores, casas e duas criancas com dindin na mao">
  <rect width="400" height="300" fill="#a9ddf3"></rect>
  <circle cx="300" cy="54" r="34" fill="#ffdf00"></circle>
  <circle cx="300" cy="54" r="54" fill="#ffdf00" opacity="0.22"></circle>
  <path d="M0,170 q54,-40 112,-12 t104,-16 q66,-16 184,20 V204 H0 Z" fill="#4f9c45"></path>
  <path d="M0,198 V168 H30 V152 H62 V176 H96 V146 H124 V162 H154 V136 H190 V166 H218 V152 H254 V172 H290 V148 H326 V168 H360 V158 H400 V198 Z" fill="#f4eeda"></path>
  <g fill="#2f8f4a">
    <path d="M28,153 L46,135 L64,153 Z"></path>
    <path d="M122,163 L139,145 L156,163 Z"></path>
    <path d="M252,173 L272,153 L292,173 Z"></path>
    <path d="M324,169 L343,151 L362,169 Z"></path>
  </g>
  <g fill="#8ec4e2">
    <rect x="36" y="176" width="7" height="9"></rect>
    <rect x="102" y="172" width="7" height="9"></rect>
    <rect x="196" y="176" width="7" height="9"></rect>
    <rect x="296" y="166" width="7" height="9"></rect>
    <rect x="366" y="172" width="7" height="9"></rect>
  </g>
  <rect x="350" y="140" width="9" height="62" fill="#8a5a32"></rect>
  <circle cx="354" cy="132" r="34" fill="#2f8f4a"></circle>
  <circle cx="330" cy="148" r="22" fill="#41a659"></circle>
  <rect x="12" y="156" width="8" height="46" fill="#8a5a32"></rect>
  <circle cx="16" cy="146" r="28" fill="#41a659"></circle>
  <rect y="196" width="400" height="104" fill="#6dbe5c"></rect>
  <rect y="196" width="400" height="16" fill="#e9e0c4"></rect>
  <path d="M0,212 H400" stroke="#cdc29b" stroke-width="2"></path>
  <ellipse cx="120" cy="258" rx="86" ry="8" fill="#4f9c45" opacity="0.55"></ellipse>
  <rect x="52" y="214" width="104" height="44" rx="7" fill="#ffffff"></rect>
  <rect x="46" y="204" width="116" height="13" rx="5" fill="#002776"></rect>
  <rect x="94" y="198" width="20" height="8" rx="4" fill="#0a3fa8"></rect>
  <g>
    <rect x="64" y="228" width="10" height="22" rx="5" fill="#2f9e4f"></rect>
    <rect x="80" y="228" width="10" height="22" rx="5" fill="#ffdf00"></rect>
    <rect x="96" y="228" width="10" height="22" rx="5" fill="#e27a7a"></rect>
    <rect x="112" y="228" width="10" height="22" rx="5" fill="#7fd08f"></rect>
  </g>
  <g fill="#0f3d21">
    <circle cx="232" cy="150" r="21"></circle>
    <path d="M211,258 V200 a21,21 0 0 1 42,0 v58 Z"></path>
    <path d="M250,206 L266,166" stroke="#0f3d21" stroke-width="11" stroke-linecap="round"></path>
    <circle cx="306" cy="166" r="17"></circle>
    <path d="M289,258 V210 a17,17 0 0 1 34,0 v48 Z"></path>
    <path d="M292,216 L278,186" stroke="#0f3d21" stroke-width="9" stroke-linecap="round"></path>
  </g>
  <rect x="262" y="140" width="13" height="34" rx="6.5" fill="#2f9e4f" transform="rotate(14 268 157)"></rect>
  <rect x="272" y="160" width="13" height="30" rx="6.5" fill="#ffdf00" transform="rotate(-18 278 175)"></rect>
</svg>`,
};

// Uma vinheta de fundo por regiao, pro cartao de escolha.
export const CENA_REGIAO = {
  escuro: {
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
  },
  claro: {
    ce: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ceara: sol a pino, mandacaru e calcada verde">
  <rect width="320" height="112" fill="#a9ddf3"></rect>
  <circle cx="248" cy="30" r="22" fill="#ffdf00"></circle>
  <path d="M0,74 q60,-16 130,-4 t190,-8 V112 H0 Z" fill="#6dbe5c"></path>
  <rect y="92" width="320" height="20" fill="#e9e0c4"></rect>
  <g fill="#2f8f4a">
    <rect x="186" y="40" width="11" height="52" rx="5"></rect>
    <rect x="170" y="56" width="9" height="36" rx="4"></rect>
    <rect x="203" y="60" width="9" height="32" rx="4"></rect>
  </g>
  <rect x="34" y="56" width="64" height="36" fill="#f4eeda"></rect>
  <path d="M28,56 L66,34 L104,56 Z" fill="#c2703f"></path>
  <rect x="58" y="70" width="16" height="22" fill="#41a659"></rect>
</svg>`,
    rj: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Rio: morro verde, mar azul e guarda-sol">
  <rect width="320" height="112" fill="#a9ddf3"></rect>
  <circle cx="62" cy="28" r="18" fill="#ffdf00"></circle>
  <path d="M150,68 q34,-56 68,0 Z" fill="#2f8f4a"></path>
  <path d="M206,68 q28,-40 56,0 Z" fill="#41a659"></path>
  <rect y="66" width="320" height="22" fill="#1f9bc4"></rect>
  <path d="M6,74 q10,-5 20,0 t20,0 M240,78 q10,-5 20,0 t20,0" stroke="#bfeaf7" stroke-width="2" fill="none"></path>
  <rect y="86" width="320" height="26" fill="#f0e3c0"></rect>
  <path d="M44,70 q26,-20 52,0 Z" fill="#00a651"></path>
  <path d="M70,70 V96" stroke="#8a5a32" stroke-width="3"></path>
</svg>`,
    mg: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Minas: igreja no morro verde e rua de paralelepipedo">
  <rect width="320" height="112" fill="#a9ddf3"></rect>
  <circle cx="272" cy="26" r="18" fill="#ffdf00"></circle>
  <path d="M0,80 q80,-46 160,-14 t160,-10 V112 H0 Z" fill="#5aa84c"></path>
  <rect x="132" y="44" width="54" height="30" fill="#f4eeda"></rect>
  <path d="M126,44 L159,26 L192,44 Z" fill="#c2703f"></path>
  <rect x="156" y="12" width="5" height="16" fill="#f4eeda"></rect>
  <rect x="152" y="17" width="13" height="4" fill="#f4eeda"></rect>
  <rect x="154" y="58" width="11" height="16" fill="#41a659"></rect>
  <rect y="92" width="320" height="20" fill="#cfc7b4"></rect>
  <g fill="#b9b09b">
    <rect x="14" y="98" width="18" height="8" rx="3"></rect>
    <rect x="48" y="98" width="18" height="8" rx="3"></rect>
    <rect x="82" y="98" width="18" height="8" rx="3"></rect>
    <rect x="232" y="98" width="18" height="8" rx="3"></rect>
    <rect x="266" y="98" width="18" height="8" rx="3"></rect>
  </g>
  <circle cx="40" cy="66" r="18" fill="#2f8f4a"></circle>
  <rect x="37" y="66" width="6" height="28" fill="#8a5a32"></rect>
</svg>`,
    sp: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Sao Paulo: quintal, casas de tijolo, roupa no varal e mangueira">
  <rect width="320" height="112" fill="#a9ddf3"></rect>
  <g fill="#c2703f">
    <rect x="12" y="34" width="58" height="52"></rect>
    <rect x="78" y="46" width="48" height="40"></rect>
    <rect x="236" y="40" width="62" height="46"></rect>
  </g>
  <g fill="#8ec4e2">
    <rect x="24" y="46" width="14" height="12"></rect>
    <rect x="90" y="56" width="12" height="10"></rect>
    <rect x="252" y="52" width="14" height="12"></rect>
  </g>
  <path d="M70,34 H126 M126,46 H236" stroke="#9c5a33" stroke-width="3"></path>
  <path d="M140,40 q34,10 76,2" stroke="#f4eeda" stroke-width="2" fill="none"></path>
  <g>
    <rect x="150" y="44" width="12" height="18" fill="#ffdf00"></rect>
    <rect x="170" y="45" width="12" height="20" fill="#e27a7a"></rect>
    <rect x="190" y="44" width="12" height="16" fill="#41a659"></rect>
  </g>
  <circle cx="296" cy="58" r="26" fill="#2f8f4a"></circle>
  <rect y="86" width="320" height="26" fill="#6dbe5c"></rect>
</svg>`,
    rs: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Rio Grande do Sul: praca de verao com arvores e banco">
  <rect width="320" height="112" fill="#a9ddf3"></rect>
  <circle cx="268" cy="24" r="17" fill="#ffdf00"></circle>
  <rect y="76" width="320" height="36" fill="#6dbe5c"></rect>
  <path d="M0,88 q80,10 160,0 t160,-4" stroke="#e9e0c4" stroke-width="7" fill="none"></path>
  <g>
    <circle cx="52" cy="52" r="28" fill="#2f8f4a"></circle>
    <rect x="48" y="52" width="8" height="30" fill="#8a5a32"></rect>
    <circle cx="122" cy="58" r="20" fill="#41a659"></circle>
    <rect x="119" y="58" width="6" height="24" fill="#8a5a32"></rect>
    <circle cx="296" cy="56" r="22" fill="#37994f"></circle>
  </g>
  <g fill="#8a5a32">
    <rect x="186" y="72" width="52" height="5" rx="2"></rect>
    <rect x="190" y="77" width="5" height="12"></rect>
    <rect x="229" y="77" width="5" height="12"></rect>
    <rect x="186" y="62" width="52" height="5" rx="2"></rect>
  </g>
</svg>`,
    pa: `
<svg viewBox="0 0 320 112" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Para: feira coberta, mangueiras e chuva de fim de tarde">
  <rect width="320" height="112" fill="#bcd9e8"></rect>
  <circle cx="38" cy="66" r="30" fill="#2f8f4a"></circle>
  <circle cx="286" cy="60" r="34" fill="#37994f"></circle>
  <g opacity="0.45" stroke="#7fb6cf" stroke-width="1.5">
    <path d="M40,0 L30,26 M96,0 L86,26 M152,0 L142,26 M208,0 L198,26 M264,0 L254,26"></path>
  </g>
  <path d="M68,44 L160,22 L252,44 Z" fill="#e27a7a"></path>
  <rect x="76" y="44" width="168" height="42" fill="#f4eeda"></rect>
  <g fill="#41a659">
    <rect x="92" y="56" width="26" height="18" rx="3"></rect>
    <rect x="130" y="56" width="26" height="18" rx="3"></rect>
    <rect x="168" y="56" width="26" height="18" rx="3"></rect>
    <rect x="206" y="56" width="26" height="18" rx="3"></rect>
  </g>
  <rect y="86" width="320" height="26" fill="#5aa84c"></rect>
  <path d="M24,98 H88 M120,104 H182 M220,98 H288" stroke="#bfeaf7" stroke-width="2" opacity="0.6"></path>
</svg>`,
  },
};

// Cena do ponto de venda, uma por local (tela do dia). "escola" e
// "carrinho" nao tem vinheta propria no mockup original -- reaproveitam
// a arte mais proxima em espirito (rua/feira) em vez de inventar do zero.
export const CENA_LOCAL = {
  escuro: {
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
  },
  claro: {
    isopor: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Isopor na calcada, meio-dia claro">
  <rect width="160" height="128" fill="#a9ddf3"></rect>
  <circle cx="128" cy="26" r="17" fill="#ffdf00"></circle>
  <rect y="70" width="160" height="20" fill="#1f9bc4"></rect>
  <rect x="34" y="30" width="15" height="46" rx="7.5" fill="#f4eeda"></rect>
  <path d="M34,54 h-11 v-12" stroke="#f4eeda" stroke-width="9" fill="none" stroke-linecap="round"></path>
  <rect y="90" width="160" height="38" fill="#f0e3c0"></rect>
  <ellipse cx="86" cy="118" rx="30" ry="5" fill="#d9c69c"></ellipse>
  <rect x="66" y="94" width="40" height="22" rx="4" fill="#ffffff"></rect>
  <rect x="63" y="88" width="46" height="7" rx="3" fill="#002776"></rect>
</svg>`,
    praia: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="O ponto: guarda-sol verde na areia, mar azul de meio-dia">
  <rect width="160" height="128" fill="#a9ddf3"></rect>
  <circle cx="126" cy="26" r="16" fill="#ffdf00"></circle>
  <path d="M0,66 q40,-14 84,-4 t76,-6 V70 H0 Z" fill="#3f9c52"></path>
  <rect y="66" width="160" height="24" fill="#1f9bc4"></rect>
  <path d="M6,74 q9,-5 18,0 t18,0 M96,80 q9,-5 18,0 t18,0" stroke="#bfeaf7" stroke-width="2" fill="none"></path>
  <rect y="88" width="160" height="40" fill="#f0e3c0"></rect>
  <path d="M14,56 q34,-26 68,0 Z" fill="#00a651"></path>
  <path d="M48,56 V104" stroke="#8a5a32" stroke-width="4"></path>
  <rect x="86" y="92" width="40" height="22" rx="4" fill="#ffffff"></rect>
  <rect x="83" y="86" width="46" height="7" rx="3" fill="#002776"></rect>
  <ellipse cx="106" cy="118" rx="30" ry="5" fill="#ddcda3"></ellipse>
</svg>`,
    escola: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Portao da escola, fim de aula, dia claro">
  <rect width="160" height="128" fill="#a9ddf3"></rect>
  <circle cx="128" cy="26" r="15" fill="#ffdf00"></circle>
  <rect x="20" y="30" width="120" height="46" fill="#f4eeda"></rect>
  <g fill="#c2703f">
    <rect x="34" y="42" width="14" height="18"></rect>
    <rect x="62" y="42" width="14" height="18"></rect>
    <rect x="90" y="42" width="14" height="18"></rect>
    <rect x="118" y="42" width="14" height="18"></rect>
  </g>
  <rect y="76" width="160" height="18" fill="#e9e0c4"></rect>
  <rect y="94" width="160" height="34" fill="#6dbe5c"></rect>
  <rect x="68" y="98" width="34" height="20" rx="4" fill="#ffffff"></rect>
</svg>`,
    carrinho: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Carrinho proprio na rua, dia claro">
  <rect width="160" height="128" fill="#a9ddf3"></rect>
  <circle cx="126" cy="24" r="15" fill="#ffdf00"></circle>
  <rect y="88" width="160" height="18" fill="#1f9bc4"></rect>
  <rect y="106" width="160" height="22" fill="#f0e3c0"></rect>
  <rect x="46" y="60" width="68" height="34" rx="6" fill="#ffffff"></rect>
  <rect x="42" y="52" width="76" height="10" rx="4" fill="#002776"></rect>
  <circle cx="60" cy="100" r="8" fill="#0f3d21"></circle>
  <circle cx="100" cy="100" r="8" fill="#0f3d21"></circle>
</svg>`,
    casa: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Freezer de casa, cozinha simples e clara">
  <rect width="160" height="128" fill="#f4eeda"></rect>
  <rect x="46" y="20" width="68" height="88" rx="6" fill="#ffffff"></rect>
  <rect x="46" y="20" width="68" height="34" rx="6" fill="#dff0e4"></rect>
  <rect x="94" y="34" width="6" height="10" rx="3" fill="#7fa88f"></rect>
  <rect x="94" y="78" width="6" height="10" rx="3" fill="#7fa88f"></rect>
  <g fill="#2f8f4a" opacity="0.6">
    <rect x="58" y="66" width="6" height="8"></rect>
    <rect x="72" y="90" width="6" height="8"></rect>
  </g>
</svg>`,
    rua: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Menino vendendo na rua movimentada, dia claro">
  <rect width="160" height="128" fill="#a9ddf3"></rect>
  <circle cx="118" cy="28" r="16" fill="#ffdf00"></circle>
  <rect y="78" width="160" height="22" fill="#1f9bc4"></rect>
  <path d="M12 82 L148 82" stroke="#bfeaf7" stroke-width="3"></path>
  <rect x="22" y="48" width="52" height="38" rx="4" fill="#f4eeda"></rect>
  <rect x="28" y="52" width="18" height="28" rx="2" fill="#c2703f"></rect>
  <g fill="#2f8f4a" opacity="0.8">
    <rect x="78" y="55" width="6" height="22"></rect>
    <rect x="88" y="52" width="6" height="26"></rect>
  </g>
  <circle cx="68" cy="92" r="7" fill="#0f3d21"></circle>
  <circle cx="112" cy="92" r="7" fill="#0f3d21"></circle>
</svg>`,
    feira: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Feira movimentada com barracas de frutas, dia claro">
  <rect width="160" height="128" fill="#a9ddf3"></rect>
  <circle cx="115" cy="24" r="18" fill="#ffdf00"></circle>
  <rect y="72" width="160" height="28" fill="#6dbe5c"></rect>
  <rect x="8" y="38" width="38" height="42" rx="3" fill="#f4eeda"></rect>
  <rect x="52" y="36" width="34" height="46" rx="3" fill="#ffffff"></rect>
  <g fill="#e8b76a">
    <circle cx="22" cy="52" r="6"></circle>
    <circle cx="32" cy="48" r="7"></circle>
    <circle cx="68" cy="49" r="8"></circle>
  </g>
  <rect x="96" y="55" width="42" height="26" rx="4" fill="#002776"></rect>
  <path d="M12 82 L148 82" stroke="#4f9c45" stroke-width="4"></path>
</svg>`,
    cozinha: `
<svg viewBox="0 0 160 128" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Cozinha simples ao amanhecer, dia claro">
  <rect width="160" height="128" fill="#f4eeda"></rect>
  <rect x="18" y="38" width="118" height="52" rx="4" fill="#ffffff"></rect>
  <rect x="32" y="22" width="22" height="18" rx="2" fill="#dff0e4"></rect>
  <rect x="78" y="48" width="48" height="12" fill="#c2703f"></rect>
  <g fill="#2f8f4a" opacity="0.7">
    <rect x="38" y="68" width="9" height="18"></rect>
    <rect x="52" y="65" width="9" height="22"></rect>
    <rect x="112" y="71" width="11" height="14"></rect>
  </g>
  <rect y="92" width="160" height="36" fill="#e9e0c4"></rect>
  <rect x="68" y="98" width="28" height="22" rx="3" fill="#ffffff"></rect>
</svg>`,
  },
};

// Cena de fechamento da tela de relatorio (isopor quase vazio).
export const CENA_RELATORIO = {
  escuro: `
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
</svg>`,
  claro: `
<svg viewBox="0 0 400 260" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Meio-dia na praia: coqueiros, mar azul e isopor quase vazio">
  <rect width="400" height="260" fill="#a9ddf3"></rect>
  <circle cx="298" cy="52" r="30" fill="#ffdf00"></circle>
  <circle cx="298" cy="52" r="48" fill="#ffdf00" opacity="0.2"></circle>
  <path d="M0,146 q60,-22 130,-6 t150,-8 q70,-6 120,10 V152 H0 Z" fill="#3f9c52"></path>
  <rect y="146" width="400" height="34" fill="#1f9bc4"></rect>
  <path d="M282,152 q16,-6 34,0 t34,0" stroke="#bfeaf7" stroke-width="2" opacity="0.85" fill="none"></path>
  <path d="M20,158 q12,-6 24,0 t24,0 M120,168 q12,-6 24,0 t24,0" stroke="#8fd9ef" stroke-width="2.5" fill="none"></path>
  <rect y="178" width="400" height="82" fill="#f0e3c0"></rect>
  <path d="M0,192 H400" stroke="#e0cfa4" stroke-width="2"></path>
  <g>
    <path d="M340,178 q4,-42 14,-62" stroke="#8a5a32" stroke-width="7" fill="none" stroke-linecap="round"></path>
    <path d="M354,116 q-30,-6 -44,10 q26,-4 44,-2 Z" fill="#2f8f4a"></path>
    <path d="M354,116 q28,-10 46,4 q-26,-2 -46,2 Z" fill="#41a659"></path>
    <path d="M354,116 q-14,-24 -4,-38 q10,18 8,38 Z" fill="#37994f"></path>
    <path d="M60,178 q-6,-38 -16,-56" stroke="#8a5a32" stroke-width="6" fill="none" stroke-linecap="round"></path>
    <path d="M44,122 q-26,-8 -38,8 q22,-4 38,0 Z" fill="#41a659"></path>
    <path d="M44,122 q24,-12 42,0 q-24,-2 -42,4 Z" fill="#2f8f4a"></path>
  </g>
  <ellipse cx="150" cy="238" rx="92" ry="10" fill="#d9c69c"></ellipse>
  <rect x="86" y="200" width="118" height="42" rx="7" fill="#ffffff"></rect>
  <path d="M84,200 L204,200 L228,172 L112,172 Z" fill="#002776"></path>
  <rect x="104" y="210" width="11" height="22" rx="5.5" fill="#2f9e4f" opacity="0.55"></rect>
  <rect x="122" y="210" width="11" height="22" rx="5.5" fill="#e27a7a" opacity="0.45"></rect>
  <path d="M246,242 V204 a14,14 0 0 1 28,0 v38 Z" fill="#0f3d21"></path>
  <circle cx="260" cy="184" r="14" fill="#0f3d21"></circle>
  <path d="M272,208 L288,190" stroke="#0f3d21" stroke-width="8" stroke-linecap="round"></path>
  <rect x="284" y="172" width="11" height="26" rx="5.5" fill="#ffdf00" transform="rotate(16 289 185)"></rect>
</svg>`,
};

// Cena da fila/freguesia no isopor, usada na barra lateral do relatorio.
export const CENA_FILA = {
  escuro: `
<svg viewBox="0 0 320 190" preserveAspectRatio="xMidYMid slice" role="img" aria-label="A freguesia: fila de criancas no isopor">
  <rect width="320" height="190" fill="#1c1f2e"></rect>
  <circle cx="40" cy="44" r="26" fill="#e8c07a" opacity="0.75"></circle>
  <path d="M0,132 V104 h34 v-14 h38 v26 h44 v-22 h40 v18 h40 v-12 h48 v20 h76 v12 Z" fill="#232739"></path>
  <g fill="#e8c07a" opacity="0.4">
    <rect x="86" y="100" width="5" height="7"></rect>
    <rect x="148" y="104" width="5" height="7"></rect>
    <rect x="232" y="98" width="5" height="7"></rect>
  </g>
  <rect y="132" width="320" height="58" fill="#262a3b"></rect>
  <path d="M0,142 H320" stroke="#383e56" stroke-width="2"></path>
  <ellipse cx="52" cy="172" rx="46" ry="7" fill="#171a26"></ellipse>
  <rect x="14" y="144" width="70" height="28" rx="5" fill="#1b1f2c"></rect>
  <rect x="10" y="137" width="78" height="10" rx="4" fill="#333852"></rect>
  <g fill="#0e1018">
    <circle cx="130" cy="104" r="15"></circle>
    <path d="M115,176 V122 a15,15 0 0 1 30,0 v54 Z"></path>
    <circle cx="186" cy="96" r="17"></circle>
    <path d="M169,176 V116 a17,17 0 0 1 34,0 v60 Z"></path>
    <circle cx="246" cy="110" r="13"></circle>
    <path d="M233,176 V126 a13,13 0 0 1 26,0 v50 Z"></path>
    <path d="M116,126 L98,140" stroke="#0e1018" stroke-width="9" stroke-linecap="round"></path>
  </g>
  <rect x="88" y="128" width="12" height="28" rx="6" fill="#9184d9" transform="rotate(-24 94 142)"></rect>
  <rect x="196" y="112" width="12" height="26" rx="6" fill="#c98b8b" opacity="0.9" transform="rotate(12 202 125)"></rect>
</svg>`,
  claro: `
<svg viewBox="0 0 320 190" preserveAspectRatio="xMidYMid slice" role="img" aria-label="A freguesia: fila de criancas no isopor, quintal verde de meio-dia">
  <rect width="320" height="190" fill="#a9ddf3"></rect>
  <circle cx="40" cy="36" r="22" fill="#ffdf00"></circle>
  <path d="M0,112 q70,-34 150,-10 t170,-14 V140 H0 Z" fill="#4f9c45"></path>
  <path d="M0,132 V96 H44 V84 H92 V108 H140 V78 H186 V102 H238 V86 H286 V106 H320 V132 Z" fill="#f4eeda"></path>
  <g fill="#c2703f">
    <path d="M42,84 L68,66 L94,84 Z"></path>
    <path d="M184,102 L212,82 L240,102 Z"></path>
  </g>
  <g fill="#8ec4e2">
    <rect x="86" y="100" width="5" height="7"></rect>
    <rect x="148" y="104" width="5" height="7"></rect>
    <rect x="232" y="98" width="5" height="7"></rect>
  </g>
  <circle cx="296" cy="84" r="28" fill="#2f8f4a"></circle>
  <rect x="292" y="84" width="8" height="48" fill="#8a5a32"></rect>
  <rect y="132" width="320" height="58" fill="#6dbe5c"></rect>
  <path d="M0,142 H320" stroke="#e9e0c4" stroke-width="6"></path>
  <ellipse cx="52" cy="172" rx="46" ry="7" fill="#4f9c45" opacity="0.6"></ellipse>
  <rect x="14" y="144" width="70" height="28" rx="5" fill="#ffffff"></rect>
  <rect x="10" y="137" width="78" height="10" rx="4" fill="#002776"></rect>
  <g fill="#0f3d21">
    <circle cx="130" cy="104" r="15"></circle>
    <path d="M115,176 V122 a15,15 0 0 1 30,0 v54 Z"></path>
    <circle cx="186" cy="96" r="17"></circle>
    <path d="M169,176 V116 a17,17 0 0 1 34,0 v60 Z"></path>
    <circle cx="246" cy="110" r="13"></circle>
    <path d="M233,176 V126 a13,13 0 0 1 26,0 v50 Z"></path>
    <path d="M116,126 L98,140" stroke="#0f3d21" stroke-width="9" stroke-linecap="round"></path>
  </g>
  <rect x="88" y="128" width="12" height="28" rx="6" fill="#2f9e4f" transform="rotate(-24 94 142)"></rect>
  <rect x="196" y="112" width="12" height="26" rx="6" fill="#ffdf00" transform="rotate(12 202 125)"></rect>
</svg>`,
};

export function cenaLocal(key, tema) {
  const grupo = CENA_LOCAL[tema] ?? CENA_LOCAL.escuro;
  return grupo[key] ?? grupo.isopor;
}

export function cenaRegiao(key, tema) {
  const grupo = CENA_REGIAO[tema] ?? CENA_REGIAO.escuro;
  return grupo[key] ?? grupo.ce;
}
