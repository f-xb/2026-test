"""
进制转换工具
十六进制 <-> 二进制 转换（纯原生 Streamlit 组件版）
"""
import streamlit as st

st.set_page_config(page_title="进制转换", page_icon="🔢", layout="centered")

# 隐藏侧边栏 + 全局样式优化
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { background: #f0f2f5; }

    /* 位标签行 */
    .bit-labels-row {
        display: flex;
        justify-content: stretch;
        gap: 6px;
        margin-bottom: 4px;
    }
    .bit-label-cell {
        flex: 1;
        text-align: center;
        font-size: 11px;
        font-weight: 600;
        color: #999;
        letter-spacing: 0.04em;
    }

    /* 让每个按钮列等宽且居中 */
    div[data-testid="column"] {
        padding: 0 3px !important;
    }
    div[data-testid="column"] > div {
        display: flex;
        justify-content: center;
    }

    /* 按钮正方形 + 大字体 */
    div[data-testid="column"] button {
        width: 100% !important;
        aspect-ratio: 1 / 1;
        font-size: 22px !important;
        font-weight: 700 !important;
        font-family: monospace !important;
        padding: 0 !important;
        border-radius: 10px !important;
        min-height: 56px !important;
    }

    /* 0 状态：灰色 */
    div[data-testid="column"] button[kind="secondary"] {
        background: #e0e0e0 !important;
        border-color: #ccc !important;
        color: #888 !important;
    }
    div[data-testid="column"] button[kind="secondary"]:hover {
        background: #d0d0d0 !important;
        color: #555 !important;
    }

    /* 结果卡片 */
    .result-box {
        background: white;
        border-radius: 14px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    }
    .result-label {
        font-size: 11px;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
    }
    .result-value {
        font-size: 28px;
        font-weight: 700;
        color: #1565c0;
        font-family: monospace;
    }
    .result-value.zero { color: #bbb; }
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if "bin_bits" not in st.session_state:
    st.session_state.bin_bits = [0] * 8

def get_bin_string():
    # bits[7]=BIT7(MSB) ... bits[0]=BIT0(LSB)，从高位到低位拼接
    return "".join(str(st.session_state.bin_bits[7 - i]) for i in range(8))

def get_dec_value():
    return int(get_bin_string(), 2)

def get_hex_string():
    return get_dec_value().to_bytes(1, 'big').hex().upper()

def get_bin_groups(s):
    return " ".join([s[i:i+4] for i in range(0, len(s), 4)])

# ──────────────────────────────────────────────
st.title("🔢 进制转换工具")

# ========== 二进制按钮区域 ==========
st.markdown("#### 二进制位 — 点击切换 0 / 1")

# 位标签行（纯 HTML，轻量安全）
st.markdown("""
<div class="bit-labels-row">
  <div class="bit-label-cell">BIT7</div>
  <div class="bit-label-cell">BIT6</div>
  <div class="bit-label-cell">BIT5</div>
  <div class="bit-label-cell">BIT4</div>
  <div class="bit-label-cell">BIT3</div>
  <div class="bit-label-cell">BIT2</div>
  <div class="bit-label-cell">BIT1</div>
  <div class="bit-label-cell">BIT0</div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(8)
for i, col in enumerate(cols):
    bit_index = 7 - i
    val = st.session_state.bin_bits[bit_index]
    with col:
        if st.button(
            str(val),
            key=f"btn_{bit_index}",
            use_container_width=True,
            type="primary" if val == 1 else "secondary",
        ):
            st.session_state.bin_bits[bit_index] = 1 - val
            st.rerun()

# 重置按钮
if st.button("🔄 重置全部为 0", use_container_width=False):
    st.session_state.bin_bits = [0] * 8
    st.rerun()

st.divider()

# ========== 转换结果 ==========
st.markdown("#### 转换结果")

bin_str   = get_bin_string()
dec_val   = get_dec_value()
hex_str   = get_hex_string()
bin_disp  = get_bin_groups(bin_str)

c1, c2, c3 = st.columns(3)
with c1:
    cls = "" if dec_val else " zero"
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">二进制</div>
        <div class="result-value{cls}">{bin_disp}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    cls = "" if dec_val else " zero"
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">十六进制</div>
        <div class="result-value{cls}">0x{hex_str}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    cls = "" if dec_val else " zero"
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">十进制</div>
        <div class="result-value{cls}">{dec_val}</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ========== 手动输入区域 ==========
st.markdown("#### 手动输入转换")
tab1, tab2 = st.tabs(["十六进制 → 二进制", "二进制 → 十六进制"])

with tab1:
    hex_input = st.text_input(
        "输入十六进制（可带或不带 0x 前缀）",
        placeholder="例如: FF, 0xFF, A1B2",
        key="hex_input"
    )
    if hex_input:
        try:
            clean = hex_input.strip().lstrip("0x").lstrip("0X")
            if not clean:
                clean = "0"
            dv = int(clean, 16)
            bv = bin(dv)[2:].zfill(max(8, len(bin(dv)[2:]) + (4 - len(bin(dv)[2:]) % 4) % 4))
            st.success(f"**二进制**: `{get_bin_groups(bv)}`　　**十进制**: {dv}")
        except ValueError:
            st.error("⚠️ 输入无效，请输入有效的十六进制数")

with tab2:
    bin_input = st.text_input(
        "输入二进制（只含 0 和 1）",
        placeholder="例如: 11111111, 1010",
        key="bin_input_manual"
    )
    if bin_input:
        clean = bin_input.strip()
        if clean.lower().startswith("0b"):
            clean = clean[2:]
        if not clean or not all(c in "01" for c in clean):
            st.error("⚠️ 输入无效，请输入只包含 0 和 1 的二进制数")
        else:
            dv = int(clean, 2)
            hv = hex(dv)[2:].upper()
            st.success(f"**十六进制**: `0x{hv}`　　**十进制**: {dv}")

st.divider()
st.caption("💡 提示：点击上方位按钮可直接切换各位的值，支持 8 位（0x00 ~ 0xFF）")