import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(
    page_title="계산기",
    page_icon="🧮",
    layout="centered",
)

st.markdown("""    
<style>
  
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 자연 숲 배경 */
.stApp {
    background:
        linear-gradient(
            135deg,
            rgba(245,250,245,0.85),
            rgba(235,245,240,0.85)
        ),
        url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1920&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 메인 영역 */
.main .block-container {
    max-width: 820px;
    padding-top: 2rem;
}

/* 제목 */
.calc-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    color: #2d5016;
    margin-bottom: 0.2rem;
    text-shadow: 0 2px 12px rgba(255,255,255,0.7);
}

.calc-subtitle {
    text-align: center;
    color: #4a6741;
    margin-bottom: 2rem;
    font-size: 0.9rem;
}

/* 유리 카드 */
.result-display,
.help-box,
.error-display {
    backdrop-filter: blur(12px);
    background: rgba(255,255,255,0.75);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.6);
    box-shadow:
        0 8px 32px rgba(45,80,22,0.1);
}

/* 결과 */
.result-display {
    padding: 1.4rem;
    margin: 1rem 0;
}

.result-expr {
    color: #4a6741;
    font-size: 0.85rem;
}

.result-value {
    color: #2d5016;
    font-size: 2.2rem;
    font-weight: 700;
}

/* 도움말 */
.help-box {
    padding: 1rem;
    color: #3d5a30;
    margin-bottom: 1rem;
}

/* 오류 */
.error-display {
    background: rgba(255,235,238,0.85);
    color: #c83c3c;
    padding: 1rem;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.60);
    border-radius: 15px;
    padding: 6px;
}

.stTabs [data-baseweb="tab"] {
    color: #4a6741 !important;
    border-radius: 10px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(
        135deg,
        #5ab359,
        #4a9d50
    ) !important;

    color: white !important;
}

/* 버튼 */
div.stButton > button {
    background: linear-gradient(
        135deg,
        #5ab359,
        #4a9d50
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem !important;
    font-weight: 600 !important;

    box-shadow:
        0 6px 20px rgba(90,179,89,0.3);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 8px 24px rgba(90,179,89,0.4);
}

/* 입력창 */
.stNumberInput input,
.stTextInput input {
    background: rgba(255,255,255,0.85) !important;
    color: #333 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(90,179,89,0.3) !important;
}

/* 셀렉트 */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
}

/* 멀티셀렉트 */
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
}

/* 라벨 */
label {
    color: #3d5a30 !important;
}

/* 제목 */
h4 {
    color: #2d5016 !important;
    font-weight: 700 !important;
}

/* 구분선 */
hr {
    border: none;
    height: 1px;
    background: rgba(90,179,89,0.2);
}

/* 푸터 */
.footer {
    text-align: center;
    color: #4a6741;
    padding: 1rem;
}""")


# ── 헬퍼 함수 ──────────────────────────────────
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


def trig_label(fname, A, B, C, D):
    A_str = "" if A == 1 else ("-" if A == -1 else f"{A:g}·")
    B_str = "" if B == 1 else f"{B:g}"
    C_str = f" + {C:g}" if C > 0 else (f" - {abs(C):g}" if C < 0 else "")
    D_str = f" + {D:g}" if D > 0 else (f" - {abs(D):g}" if D < 0 else "")
    return f"y = {A_str}{fname}({B_str}x{C_str}){D_str}"


# ── 헤더 ───────────────────────────────────────
st.markdown('<div class="calc-title">⟨ CALC.EXE ⟩</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="calc-subtitle">arithmetic · modular · exponent · log · trigonometry</div>',
    unsafe_allow_html=True,
)

# ── 탭 ─────────────────────────────────────────
tab_arith, tab_mod, tab_exp, tab_log, tab_trig = st.tabs(
    ["사칙연산", "모듈러", "지수", "로그", "삼각함수 그래프"]
)

# ── 사칙연산 ────────────────────────────────────
with tab_arith:
    st.markdown("#### 사칙연산")
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a", value=0.0, format="%g", key="a_arith")
    with col2:
        b = st.number_input("b", value=0.0, format="%g", key="b_arith")
    op = st.selectbox("연산", ["+  덧셈", "−  뺄셈", "×  곱셈", "÷  나눗셈"], label_visibility="collapsed")
    if st.button("계산", key="btn_arith"):
        try:
            sym = op.split()[0]
            if sym == "+":   result = a + b
            elif sym == "−": result = a - b
            elif sym == "×": result = a * b
            else:
                if b == 0: raise ZeroDivisionError("0으로 나눌 수 없습니다.")
                result = a / b
            show_result(result, f"{a} {sym} {b}")
        except ZeroDivisionError as e:
            show_error(str(e))

# ── 모듈러 ──────────────────────────────────────
with tab_mod:
    st.markdown("#### 모듈러 연산")
    st.markdown('<div class="help-box">a mod b — a를 b로 나눈 <b>나머지</b>를 구합니다.<br>예: 17 mod 5 = 2</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        ma = st.number_input("a (피제수)", value=17, step=1, key="ma")
    with col2:
        mb = st.number_input("b (제수)", value=5, step=1, key="mb")
    if st.button("계산", key="btn_mod"):
        try:
            if mb == 0: raise ZeroDivisionError("b는 0이 될 수 없습니다.")
            show_result(int(ma) % int(mb), f"{int(ma)} mod {int(mb)}")
        except ZeroDivisionError as e:
            show_error(str(e))

# ── 지수 ────────────────────────────────────────
with tab_exp:
    st.markdown("#### 지수 연산")
    st.markdown('<div class="help-box">base ^ exponent — base를 exponent번 거듭제곱합니다.<br>예: 2 ^ 10 = 1024</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("밑 (base)", value=2.0, format="%g", key="base")
    with col2:
        exponent = st.number_input("지수 (exponent)", value=10.0, format="%g", key="exponent")
    if st.button("계산", key="btn_exp"):
        try:
            result = base ** exponent
            if math.isinf(result): raise OverflowError("결과가 너무 커서 표현할 수 없습니다.")
            show_result(result, f"{base} ^ {exponent}")
        except (ValueError, OverflowError) as e:
            show_error(str(e))

# ── 로그 ────────────────────────────────────────
with tab_log:
    st.markdown("#### 로그 연산")
    st.markdown(
        '<div class="help-box">'
        '• 상용 로그 log₁₀(x) — 밑이 10인 로그<br>'
        '• 자연 로그 ln(x) — 밑이 e(≈2.718)인 로그<br>'
        '• 임의 밑 log_b(x) — 밑을 직접 지정<br>'
        '진수 x는 반드시 양수여야 합니다.'
        '</div>', unsafe_allow_html=True)
    log_kind = st.radio("로그 종류", ["log₁₀(x)  상용 로그", "ln(x)  자연 로그", "log_b(x)  임의 밑"],
                        horizontal=True, label_visibility="collapsed")
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
            if lx <= 0: raise ValueError("진수(x)는 0보다 커야 합니다.")
            if "상용" in log_kind:
                show_result(math.log10(lx), f"log₁₀({lx})")
            elif "자연" in log_kind:
                show_result(math.log(lx), f"ln({lx})")
            else:
                if lb <= 0 or lb == 1: raise ValueError("밑(b)은 양수이고 1이 아니어야 합니다.")
                show_result(math.log(lx, lb), f"log_{lb}({lx})")
        except ValueError as e:
            show_error(str(e))

# ── 삼각함수 그래프 ─────────────────────────────
with tab_trig:
    st.markdown("#### 삼각함수 그래프")
    st.markdown(
        '<div class="help-box">'
        '• <b>A · f(Bx + C) + D</b> 형태로 그래프를 그립니다.<br>'
        '• A = 진폭 &nbsp;|&nbsp; B = 주기 배율 &nbsp;|&nbsp; C = 위상 &nbsp;|&nbsp; D = 수직 이동<br>'
        '• sin · cos · tan 을 동시에 선택해 겹쳐 그릴 수 있습니다.'
        '</div>', unsafe_allow_html=True)
    funcs_selected = st.multiselect("그릴 함수 선택", options=["sin", "cos", "tan"], default=["sin"])
    col1, col2, col3, col4 = st.columns(4)
    with col1: amp   = st.number_input("진폭  A",    value=1.0, format="%g", key="trig_amp")
    with col2: freq  = st.number_input("주기 배율 B", value=1.0, format="%g", key="trig_freq")
    with col3: phase = st.number_input("위상  C",    value=0.0, format="%g", key="trig_phase")
    with col4: vert  = st.number_input("수직 이동 D", value=0.0, format="%g", key="trig_vert")
    col_unit, col_range = st.columns([1, 2])
    with col_unit:
        x_unit = st.radio("x축 단위", ["라디안 (rad)", "도 (°)"], key="trig_unit")
    with col_range:
        if "도" in x_unit:
            x_min = st.number_input("x 최솟값 (°)",   value=-360.0, format="%g", key="trig_xmin")
            x_max = st.number_input("x 최댓값 (°)",   value= 360.0, format="%g", key="trig_xmax")
        else:
            x_min = st.number_input("x 최솟값 (π배수)", value=-2.0, format="%g", key="trig_xmin")
            x_max = st.number_input("x 최댓값 (π배수)", value= 2.0, format="%g", key="trig_xmax")

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

            COLORS = {"sin": "#5ab359", "cos": "#2d8f50", "tan": "#3db86d"}
            fig, ax = plt.subplots(figsize=(8, 4.4))
            fig.patch.set_facecolor("#f5faf5")
            ax.set_facecolor("#fafbfa")
            for spine in ax.spines.values():
                spine.set_edgecolor("#d0e5c8")
            ax.tick_params(colors="#4a6741", labelsize=8.5)
            ax.xaxis.label.set_color("#4a6741")
            ax.yaxis.label.set_color("#4a6741")
            ax.grid(color="#e8f0e6", linewidth=0.8, linestyle="--")
            ax.axhline(0, color="#a8d5a8", linewidth=1.1)
            ax.axvline(0, color="#a8d5a8", linewidth=1.1)

            for fname in funcs_selected:
                arg = freq * x_rad + phase
                if fname == "sin":   y = amp * np.sin(arg) + vert
                elif fname == "cos": y = amp * np.cos(arg) + vert
                else:
                    y = amp * np.tan(arg) + vert
                    y = np.where(np.abs(y) > 30, np.nan, y)
                c = COLORS[fname]
                ax.plot(x_plot, y, color=c, linewidth=5,   alpha=0.15)
                ax.plot(x_plot, y, color=c, linewidth=2.2, alpha=0.9,
                        label=trig_label(fname, amp, freq, phase, vert))

            if "라디안" in x_unit:
                ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.4g}π"))
            ax.set_xlabel(xlabel, fontsize=9)
            ax.set_ylabel("y", fontsize=9)
            ax.legend(facecolor="#f0f5ed", edgecolor="#a8d5a8", labelcolor="#2d5016", fontsize=8.5)
            ax.set_title("TRIGONOMETRY GRAPH", color="#2d5016", fontsize=10, pad=12,
                         fontfamily="monospace", fontweight="bold")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

# ── 푸터 ────────────────────────────────────────
st.markdown("---")
st.markdown("<p class='footer'>◈ BUILT WITH STREAMLIT & PYTHON MATH ◈</p>", unsafe_allow_html=True)
