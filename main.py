import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ──────────────────────────────────────────────
#  페이지 기본 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="계산기",
    page_icon="🧮",
    layout="centered",
)

# ──────────────────────────────────────────────
#  커스텀 스타일 (사이버펑크 × 파티클)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;900&family=IBM+Plex+Mono:wght@400;600&family=Noto+Sans+KR:wght@400;600&display=swap');

/* ── 기본 리셋 ── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* ── 파티클 배경 캔버스 ── */
#particle-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
}

/* ── 전체 배경 ── */
.stApp {
    background: linear-gradient(135deg, #0a0015 0%, #0d001f 30%, #050010 60%, #0a0a1a 100%);
    background-attachment: fixed;
    position: relative;
}

/* ── 컨텐츠를 캔버스 위로 올리기 ── */
.main .block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
    max-width: 780px;
}

/* ── 헤더 ── */
.calc-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #ff2d9b, #bf5cff, #00e5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 2px;
    padding: 1.5rem 0 0.2rem;
    text-shadow: none;
    filter: drop-shadow(0 0 18px #bf5cff88);
}
.calc-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #9966cc99;
    margin-bottom: 2rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}

/* ── 글래스모피즘 카드 ── */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(191, 92, 255, 0.25);
    border-radius: 16px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow:
        0 0 0 1px rgba(191, 92, 255, 0.08),
        0 8px 32px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255,255,255,0.05);
    padding: 1.6rem 1.8rem;
    margin: 0.8rem 0;
}

/* ── 결과 디스플레이 ── */
.result-display {
    background: rgba(0,0,0,0.6);
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin: 1rem 0;
    font-family: 'IBM Plex Mono', monospace;
    box-shadow:
        0 0 20px rgba(0, 229, 255, 0.15),
        inset 0 0 30px rgba(0, 229, 255, 0.03);
    position: relative;
    overflow: hidden;
}
.result-display::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    animation: scan-line 3s linear infinite;
}
@keyframes scan-line {
    0%   { left: -100%; }
    100% { left: 200%;  }
}
.result-expr {
    color: #9966cc;
    font-size: 0.78rem;
    margin-bottom: 0.4rem;
    letter-spacing: 1px;
}
.result-value {
    color: #00e5ff;
    font-size: 2.4rem;
    font-weight: 600;
    word-break: break-all;
    text-shadow: 0 0 20px #00e5ff88, 0 0 40px #00e5ff44;
}

/* ── 오류 박스 ── */
.error-display {
    background: rgba(255, 45, 100, 0.08);
    border: 1px solid rgba(255, 45, 100, 0.4);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    color: #ff6b9d;
    font-size: 0.9rem;
    margin: 0.8rem 0;
    font-family: 'IBM Plex Mono', monospace;
    box-shadow: 0 0 16px rgba(255, 45, 100, 0.1);
}

/* ── 도움말 박스 ── */
.help-box {
    background: rgba(191, 92, 255, 0.06);
    border-left: 2px solid #bf5cff;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    color: #ccaaff;
    font-size: 0.82rem;
    margin: 0.5rem 0 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.8;
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(191, 92, 255, 0.2);
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    backdrop-filter: blur(8px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #9966cc;
    padding: 0.45rem 1rem;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.5px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7b00d4, #c500a0) !important;
    color: #ffffff !important;
    box-shadow: 0 0 14px rgba(191, 92, 255, 0.5) !important;
}

/* ── 버튼 ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7b00d4 0%, #c500a0 100%);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-family: 'Orbitron', monospace;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 1.5px;
    padding: 0.65rem 0;
    margin-top: 0.7rem;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.25s;
    box-shadow: 0 4px 20px rgba(197, 0, 160, 0.35);
}
div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transition: left 0.4s;
}
div.stButton > button:hover::before { left: 100%; }
div.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(197, 0, 160, 0.55);
    transform: translateY(-1px);
}
div.stButton > button:active { transform: translateY(0); }

/* ── 인풋 ── */
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] > input {
    background: rgba(0,0,0,0.4) !important;
    border-color: rgba(191, 92, 255, 0.3) !important;
    color: #e0c8ff !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
div[data-baseweb="base-input"] > input:focus {
    border-color: #bf5cff !important;
    box-shadow: 0 0 0 2px rgba(191, 92, 255, 0.2) !important;
}
.stNumberInput label, .stSelectbox label, .stRadio label, .stMultiSelect label {
    color: #ccaaff !important;
    font-size: 0.82rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    letter-spacing: 0.5px;
}

/* ── selectbox / multiselect ── */
div[data-baseweb="select"] > div {
    background: rgba(0,0,0,0.4) !important;
    border-color: rgba(191, 92, 255, 0.3) !important;
    color: #e0c8ff !important;
    border-radius: 8px !important;
}

/* ── radio ── */
.stRadio [data-testid="stMarkdownContainer"] p { color: #ccaaff !important; }

/* ── 구분선 ── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #bf5cff44, transparent);
    margin: 1.5rem 0;
}

/* ── 섹션 제목 ── */
h4 {
    font-family: 'Orbitron', monospace !important;
    color: #bf5cff !important;
    font-size: 0.9rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase;
    margin-bottom: 1rem !important;
    text-shadow: 0 0 10px #bf5cff66;
}

/* ── 푸터 ── */
.footer {
    text-align: center;
    color: #66448899;
    font-size: 0.75rem;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 2px;
    padding: 1rem 0 2rem;
}
</style>

<!-- 파티클 캔버스 -->
<canvas id="particle-canvas"></canvas>

<script>
(function() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const COLORS = ['#ff2d9b', '#bf5cff', '#00e5ff', '#7b00d4'];
    const NUM = 90;

    const particles = Array.from({ length: NUM }, () => ({
        x:  Math.random() * window.innerWidth,
        y:  Math.random() * window.innerHeight,
        r:  Math.random() * 1.8 + 0.4,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        color: COLORS[Math.floor(Math.random() * COLORS.length)],
        alpha: Math.random() * 0.6 + 0.15,
    }));

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 연결선
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(191, 92, 255, ${0.18 * (1 - dist/130)})`;
                    ctx.lineWidth = 0.6;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        // 파티클
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;

            // 글로우
            ctx.shadowBlur   = 10;
            ctx.shadowColor  = p.color;
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.globalAlpha = 1;

            // 이동
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width)  p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;
        });

        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  헬퍼 함수
# ──────────────────────────────────────────────
def show_result(value, expression: str):
    if isinstance(value, float):
        formatted = f"{value:,.10g}"
    else:
        formatted = f"{value:,}"
    st.markdown(f"""
    <div class="result-display">
        <div class="result-expr">▸ {expression}</div>
        <div class="result-value">{formatted}</div>
    </div>
    """, unsafe_allow_html=True)


def show_error(msg: str):
    st.markdown(f'<div class="error-display">⚠ {msg}</div>', unsafe_allow_html=True)


def trig_label(fname: str, A: float, B: float, C: float, D: float) -> str:
    A_str = "" if A == 1 else ("-" if A == -1 else f"{A:g}·")
    B_str = "" if B == 1 else f"{B:g}"
    C_str = f" + {C:g}" if C > 0 else (f" - {abs(C):g}" if C < 0 else "")
    D_str = f" + {D:g}" if D > 0 else (f" - {abs(D):g}" if D < 0 else "")
    inner = f"{B_str}x{C_str}"
    return f"y = {A_str}{fname}({inner}){D_str}"


# ──────────────────────────────────────────────
#  헤더
# ──────────────────────────────────────────────
st.markdown('<div class="calc-title">⟨ CALC.EXE ⟩</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="calc-subtitle">arithmetic · modular · exponent · log · trigonometry</div>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
#  탭 구성
# ──────────────────────────────────────────────
tab_arith, tab_mod, tab_exp, tab_log, tab_trig = st.tabs(
    ["사칙연산", "모듈러", "지수", "로그", "삼각함수 그래프"]
)


# ── 사칙연산 ──────────────────────────────────
with tab_arith:
    st.markdown("#### 사칙연산")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a", value=0.0, format="%g", key="a_arith")
    with col2:
        b = st.number_input("b", value=0.0, format="%g", key="b_arith")

    op = st.selectbox(
        "연산",
        options=["+  덧셈", "−  뺄셈", "×  곱셈", "÷  나눗셈"],
        label_visibility="collapsed",
    )

    if st.button("계산", key="btn_arith"):
        try:
            sym = op.split()[0]
            if sym == "+":
                result = a + b
            elif sym == "−":
                result = a - b
            elif sym == "×":
                result = a * b
            else:
                if b == 0:
                    raise ZeroDivisionError("0으로 나눌 수 없습니다.")
                result = a / b
            show_result(result, f"{a} {sym} {b}")
        except ZeroDivisionError as e:
            show_error(str(e))


# ── 모듈러 연산 ───────────────────────────────
with tab_mod:
    st.markdown("#### 모듈러 연산")
    st.markdown(
        '<div class="help-box">a mod b — a를 b로 나눈 <b>나머지</b>를 구합니다.<br>'
        "예: 17 mod 5 = 2</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        ma = st.number_input("a (피제수)", value=17, step=1, key="ma")
    with col2:
        mb = st.number_input("b (제수)", value=5, step=1, key="mb")

    if st.button("계산", key="btn_mod"):
        try:
            if mb == 0:
                raise ZeroDivisionError("b는 0이 될 수 없습니다.")
            result = int(ma) % int(mb)
            show_result(result, f"{int(ma)} mod {int(mb)}")
        except ZeroDivisionError as e:
            show_error(str(e))


# ── 지수 연산 ─────────────────────────────────
with tab_exp:
    st.markdown("#### 지수 연산")
    st.markdown(
        '<div class="help-box">base ^ exponent — base를 exponent번 거듭제곱합니다.<br>'
        "예: 2 ^ 10 = 1024</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("밑 (base)", value=2.0, format="%g", key="base")
    with col2:
        exponent = st.number_input("지수 (exponent)", value=10.0, format="%g", key="exponent")

    if st.button("계산", key="btn_exp"):
        try:
            result = base ** exponent
            if math.isinf(result):
                raise OverflowError("결과가 너무 커서 표현할 수 없습니다.")
            show_result(result, f"{base} ^ {exponent}")
        except (ValueError, OverflowError) as e:
            show_error(str(e))


# ── 로그 연산 ─────────────────────────────────
with tab_log:
    st.markdown("#### 로그 연산")
    st.markdown(
        '<div class="help-box">'
        "• 상용 로그 log₁₀(x) — 밑이 10인 로그<br>"
        "• 자연 로그 ln(x) — 밑이 e(≈2.718)인 로그<br>"
        "• 임의 밑 log_b(x) — 밑을 직접 지정<br>"
        "진수 x는 반드시 양수여야 합니다."
        "</div>",
        unsafe_allow_html=True,
    )

    log_kind = st.radio(
        "로그 종류",
        ["log₁₀(x)  상용 로그", "ln(x)  자연 로그", "log_b(x)  임의 밑"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if "임의" in log_kind:
        col1, col2 = st.columns(2)
        with col1:
            lx = st.number_input("진수 x", value=8.0, min_value=1e-15, format="%g", key="lx")
        with col2:
            lb = st.number_input("밑 b", value=2.0, min_value=1e-15, format="%g", key="lb")
    else:
        lx = st.number_input("진수 x", value=100.0, min_value=1e-15, format="%g", key="lx2")

    if st.button("계산", key="btn_log"):
        try:
            if lx <= 0:
                raise ValueError("진수(x)는 0보다 커야 합니다.")
            if "상용" in log_kind:
                result = math.log10(lx)
                show_result(result, f"log₁₀({lx})")
            elif "자연" in log_kind:
                result = math.log(lx)
                show_result(result, f"ln({lx})")
            else:
                if lb <= 0 or lb == 1:
                    raise ValueError("밑(b)은 양수이고 1이 아니어야 합니다.")
                result = math.log(lx, lb)
                show_result(result, f"log_{lb}({lx})")
        except ValueError as e:
            show_error(str(e))


# ── 삼각함수 그래프 ───────────────────────────
with tab_trig:
    st.markdown("#### 삼각함수 그래프")
    st.markdown(
        '<div class="help-box">'
        "• <b>A · f(Bx + C) + D</b> 형태로 그래프를 그립니다.<br>"
        "• A = 진폭(amplitude) &nbsp;|&nbsp; B = 주기 배율 &nbsp;|&nbsp; "
        "C = 위상(phase shift) &nbsp;|&nbsp; D = 수직 이동<br>"
        "• sin · cos · tan 을 동시에 선택해 겹쳐 그릴 수 있습니다.<br>"
        "• x축 단위를 라디안(π 배수) 또는 도(°) 중에서 선택할 수 있습니다."
        "</div>",
        unsafe_allow_html=True,
    )

    funcs_selected = st.multiselect(
        "그릴 함수 선택 (복수 선택 가능)",
        options=["sin", "cos", "tan"],
        default=["sin"],
        key="trig_funcs",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        amp = st.number_input("진폭  A", value=1.0, format="%g", key="trig_amp")
    with col2:
        freq = st.number_input("주기 배율  B", value=1.0, format="%g", key="trig_freq")
    with col3:
        phase = st.number_input("위상  C", value=0.0, format="%g", key="trig_phase")
    with col4:
        vert = st.number_input("수직 이동  D", value=0.0, format="%g", key="trig_vert")

    col_unit, col_range = st.columns([1, 2])
    with col_unit:
        x_unit = st.radio(
            "x축 단위",
            ["라디안 (rad)", "도 (°)"],
            key="trig_unit",
        )
    with col_range:
        if "도" in x_unit:
            x_min = st.number_input("x 최솟값 (°)", value=-360.0, format="%g", key="trig_xmin")
            x_max = st.number_input("x 최댓값 (°)", value=360.0, format="%g", key="trig_xmax")
        else:
            x_min = st.number_input(
                "x 최솟값 (π 배수)", value=-2.0, format="%g", key="trig_xmin"
            )
            x_max = st.number_input(
                "x 최댓값 (π 배수)", value=2.0, format="%g", key="trig_xmax"
            )

    if st.button("그래프 그리기", key="btn_trig"):
        if not funcs_selected:
            show_error("함수를 하나 이상 선택해주세요.")
        elif x_min >= x_max:
            show_error("x 최솟값은 최댓값보다 작아야 합니다.")
        else:
            if "도" in x_unit:
                x_deg  = np.linspace(x_min, x_max, 1800)
                x_rad  = np.deg2rad(x_deg)
                x_plot = x_deg
                xlabel = "x (°)"
            else:
                x_plot = np.linspace(x_min, x_max, 1800)
                x_rad  = x_plot * np.pi
                xlabel = "x (π)"

            COLORS = {
                "sin": "#ff2d9b",
                "cos": "#00e5ff",
                "tan": "#bf5cff",
            }

            fig, ax = plt.subplots(figsize=(8, 4.4))
            fig.patch.set_facecolor("#080014")
            ax.set_facecolor("#080014")

            for spine in ax.spines.values():
                spine.set_edgecolor("#3a1a5e")

            ax.tick_params(colors="#9966cc", labelsize=8.5)
            ax.xaxis.label.set_color("#9966cc")
            ax.yaxis.label.set_color("#9966cc")
            ax.grid(color="#1a0a30", linewidth=0.8, linestyle="--")
            ax.axhline(0, color="#3a1a5e", linewidth=1.1)
            ax.axvline(0, color="#3a1a5e", linewidth=1.1)

            for fname in funcs_selected:
                arg = freq * x_rad + phase

                if fname == "sin":
                    y = amp * np.sin(arg) + vert
                elif fname == "cos":
                    y = amp * np.cos(arg) + vert
                else:
                    y = amp * np.tan(arg) + vert
                    y = np.where(np.abs(y) > 30, np.nan, y)

                color = COLORS[fname]
                # 글로우 효과: 넓은 선 + 얇은 선 겹치기
                ax.plot(x_plot, y, color=color, linewidth=5, alpha=0.18)
                ax.plot(x_plot, y, color=color, linewidth=2.2, alpha=0.85,
                        label=trig_label(fname, amp, freq, phase, vert))

            if "라디안" in x_unit:
                ax.xaxis.set_major_formatter(
                    ticker.FuncFormatter(lambda v, _: f"{v:.4g}π")
                )

            ax.set_xlabel(xlabel, fontsize=9)
            ax.set_ylabel("y", fontsize=9)
            ax.legend(
                facecolor="#0d0024",
                edgecolor="#3a1a5e",
                labelcolor="white",
                fontsize=8.5,
                loc="upper right",
            )
            ax.set_title(
                "TRIGONOMETRY GRAPH",
                color="#bf5cff",
                fontsize=10,
                pad=12,
                fontfamily="monospace",
                fontweight="bold",
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)


# ──────────────────────────────────────────────
#  푸터
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p class='footer'>◈ BUILT WITH STREAMLIT & PYTHON MATH ◈</p>",
    unsafe_allow_html=True,
)
