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
#  커스텀 스타일
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+KR:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans KR', sans-serif;
}

/* 전체 배경 */
.stApp { background-color: #f5f5f0; }

/* 헤더 */
.calc-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #1a1a1a;
    letter-spacing: -1px;
    padding: 1.5rem 0 0.2rem;
}
.calc-subtitle {
    font-size: 0.85rem;
    color: #888;
    margin-bottom: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
}

/* 결과 박스 */
.result-display {
    background: #1a1a1a;
    border-radius: 8px;
    padding: 1.4rem 1.8rem;
    margin: 1rem 0;
    font-family: 'IBM Plex Mono', monospace;
}
.result-expr { color: #666; font-size: 0.8rem; margin-bottom: 0.3rem; }
.result-value { color: #e8ff6e; font-size: 2.2rem; font-weight: 600; word-break: break-all; }

/* 오류 박스 */
.error-display {
    background: #fff0f0;
    border-left: 3px solid #e55;
    border-radius: 4px;
    padding: 0.8rem 1.2rem;
    color: #c00;
    font-size: 0.9rem;
    margin: 0.8rem 0;
    font-family: 'IBM Plex Mono', monospace;
}

/* 도움말 박스 */
.help-box {
    background: #eeeee8;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    color: #555;
    font-size: 0.82rem;
    margin: 0.5rem 0 1rem;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.7;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: #eeeee8;
    border-radius: 8px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #777;
    padding: 0.45rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: #1a1a1a !important;
    color: #e8ff6e !important;
}

/* 버튼 */
div.stButton > button {
    width: 100%;
    background: #1a1a1a;
    color: #e8ff6e;
    border: none;
    border-radius: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.6rem 0;
    transition: opacity 0.15s;
    margin-top: 0.5rem;
}
div.stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  헬퍼 함수
# ──────────────────────────────────────────────
def show_result(value, expression: str):
    """계산 결과를 검은 디스플레이 박스로 출력"""
    if isinstance(value, float):
        formatted = f"{value:,.10g}"
    else:
        formatted = f"{value:,}"
    st.markdown(f"""
    <div class="result-display">
        <div class="result-expr">{expression}</div>
        <div class="result-value">{formatted}</div>
    </div>
    """, unsafe_allow_html=True)


def show_error(msg: str):
    st.markdown(f'<div class="error-display">⚠ {msg}</div>', unsafe_allow_html=True)


def trig_label(fname: str, A: float, B: float, C: float, D: float) -> str:
    """삼각함수 그래프 범례용 수식 문자열 생성 (A·f(Bx + C) + D)"""
    A_str = "" if A == 1 else ("-" if A == -1 else f"{A:g}·")
    B_str = "" if B == 1 else f"{B:g}"
    C_str = f" + {C:g}" if C > 0 else (f" - {abs(C):g}" if C < 0 else "")
    D_str = f" + {D:g}" if D > 0 else (f" - {abs(D):g}" if D < 0 else "")
    inner = f"{B_str}x{C_str}"
    return f"y = {A_str}{fname}({inner}){D_str}"


# ──────────────────────────────────────────────
#  헤더
# ──────────────────────────────────────────────
st.markdown('<div class="calc-title">🧮 계산기</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="calc-subtitle">사칙연산 · 모듈러 · 지수 · 로그 · 삼각함수</div>',
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

    # 함수 선택 (멀티셀렉트)
    funcs_selected = st.multiselect(
        "그릴 함수 선택 (복수 선택 가능)",
        options=["sin", "cos", "tan"],
        default=["sin"],
        key="trig_funcs",
    )

    # 파라미터 입력
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        amp = st.number_input("진폭  A", value=1.0, format="%g", key="trig_amp")
    with col2:
        freq = st.number_input("주기 배율  B", value=1.0, format="%g", key="trig_freq")
    with col3:
        phase = st.number_input("위상  C", value=0.0, format="%g", key="trig_phase")
    with col4:
        vert = st.number_input("수직 이동  D", value=0.0, format="%g", key="trig_vert")

    # x축 단위 & 범위
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
            # x 배열 생성
            if "도" in x_unit:
                x_deg = np.linspace(x_min, x_max, 1800)
                x_rad = np.deg2rad(x_deg)
                x_plot = x_deg
                xlabel = "x (°)"
            else:
                x_plot = np.linspace(x_min, x_max, 1800)   # π 배수
                x_rad = x_plot * np.pi
                xlabel = "x (π)"

            # 그래프 스타일 (기존 다크 테마에 맞춤)
            COLORS = {"sin": "#e8ff6e", "cos": "#6eb5ff", "tan": "#ff9e6e"}

            fig, ax = plt.subplots(figsize=(8, 4.2))
            fig.patch.set_facecolor("#1a1a1a")
            ax.set_facecolor("#1a1a1a")

            for spine in ax.spines.values():
                spine.set_edgecolor("#444")

            ax.tick_params(colors="#aaa", labelsize=9)
            ax.xaxis.label.set_color("#aaa")
            ax.yaxis.label.set_color("#aaa")
            ax.grid(color="#2e2e2e", linewidth=0.7, linestyle="--")
            ax.axhline(0, color="#555", linewidth=0.9)
            ax.axvline(0, color="#555", linewidth=0.9)

            for fname in funcs_selected:
                arg = freq * x_rad + phase      # B·x + C (라디안)

                if fname == "sin":
                    y = amp * np.sin(arg) + vert
                elif fname == "cos":
                    y = amp * np.cos(arg) + vert
                else:  # tan
                    y = amp * np.tan(arg) + vert
                    # 불연속점 마스킹: |y| > 30 이면 nan 처리
                    y = np.where(np.abs(y) > 30, np.nan, y)

                ax.plot(
                    x_plot, y,
                    color=COLORS[fname],
                    linewidth=1.8,
                    label=trig_label(fname, amp, freq, phase, vert),
                )

            # 라디안 모드일 때 x축 눈금을 "값π" 형식으로 표시
            if "라디안" in x_unit:
                ax.xaxis.set_major_formatter(
                    ticker.FuncFormatter(lambda v, _: f"{v:.4g}π")
                )

            ax.set_xlabel(xlabel, fontsize=9)
            ax.set_ylabel("y", fontsize=9)
            ax.legend(
                facecolor="#2a2a2a",
                edgecolor="#444",
                labelcolor="white",
                fontsize=8.5,
                loc="upper right",
            )
            ax.set_title(
                "삼각함수 그래프",
                color="#ccc",
                fontsize=11,
                pad=10,
                fontfamily="monospace",
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)


# ──────────────────────────────────────────────
#  푸터
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#bbb;font-size:0.78rem;"
    "font-family:IBM Plex Mono,monospace;'>Built with Streamlit & Python math</p>",
    unsafe_allow_html=True,
)
