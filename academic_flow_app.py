import streamlit as st
import matplotlib.pyplot as plt
import requests
import json

# Page Config
st.set_page_config(
    page_title="Academic Flow",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom High-End Minimal & Poetic CSS + Mobile Scroll Fixes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

    html, body, .stApp {
        background: #0B0C10;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #E0E2EC;
        -webkit-overflow-scrolling: touch !important;
        overflow-y: auto !important;
    }

    header, footer, #MainMenu { visibility: hidden; display: none; }
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 440px !important; 
    }

    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.1rem;
    }
    
    .brand-subtitle {
        font-size: 0.72rem;
        font-weight: 300;
        color: #6366F1;
        text-align: center;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .status-card {
        padding: 12px 16px;
        border-radius: 14px;
        font-size: 0.85rem;
        font-weight: 400;
        letter-spacing: 0.02em;
        text-align: center;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
    }
    .status-cooking {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34D399;
    }
    .status-cooked {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.25);
        color: #F87171;
    }
    .status-neutral {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.25);
        color: #818CF8;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(21, 23, 30, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        padding: 14px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem !important;
    }

    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #161822 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #E0E2EC !important;
    }
    
    input {
        color: #E0E2EC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.05em !important;
        padding: 10px !important;
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.35) !important;
    }

    .reset-btn > div > button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #6B7280 !important;
        box-shadow: none !important;
        padding: 6px !important;
        font-size: 0.75rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch Credentials Safely
BIN_ID = st.secrets.get("JSONBIN_BIN_ID", "").strip()
API_KEY = st.secrets.get("JSONBIN_API_KEY", "").strip()

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

def is_configured():
    return bool(BIN_ID and API_KEY and "YOUR_" not in BIN_ID)

# Cloud Fetch
def fetch_cloud_data():
    if not is_configured():
        return None
    try:
        resp = requests.get(f"{URL}/latest", headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            rec = resp.json().get("record", {})
            if isinstance(rec, dict):
                return rec
    except Exception:
        pass
    return None

def sync_save_data(data_dict):
    if not is_configured():
        st.error("🚨 Setup Error: Cloud database keys are not configured in Streamlit Secrets!")
        return False
    try:
        resp = requests.put(URL, headers=HEADERS, json=data_dict, timeout=5)
        if resp.status_code == 200:
            st.toast("🔒 Saved permanently to Cloud!", icon="✅")
            return True
        else:
            st.error(f"Save failed (HTTP {resp.status_code}). Check your JSONBin Master Key.")
            return False
    except Exception as e:
        st.error(f"Network error while saving: {e}")
        return False

# Load data on start
if "flow_data" not in st.session_state:
    cloud_rec = fetch_cloud_data()
    if cloud_rec:
        st.session_state["flow_data"] = {str(i): cloud_rec.get(str(i)) for i in range(1, 21)}
    else:
        st.session_state["flow_data"] = {str(i): None for i in range(1, 21)}

data = st.session_state["flow_data"]

# Header
st.markdown('<div class="brand-title">A C A D E M I A</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">The Arc of Momentum</div>', unsafe_allow_html=True)

# Warning Banner if Cloud Keys are missing
if not is_configured():
    st.warning("⚠️ Cloud persistence is OFF! Open Streamlit Cloud Settings -> Secrets and paste your actual JSONBin keys so your data never resets.")

# Dynamic Status Banner
entered_weeks = [i for i in range(1, 21) if data[str(i)] is not None]

if len(entered_weeks) >= 2:
    latest = data[str(entered_weeks[-1])]
    prev = data[str(entered_weeks[-2])]
    if latest > prev:
        st.markdown('<div class="status-card status-cooking">✨ "The fire rises. You are cooking, keep ascending."</div>', unsafe_allow_html=True)
    elif latest < prev:
        st.markdown('<div class="status-card status-cooked">🥀 "A slight stumble. You are getting cooked—return to the books."</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-card status-neutral">⚡ "Equilibrium. Hold steady before the breakout."</div>', unsafe_allow_html=True)
elif len(entered_weeks) == 1:
    st.markdown('<div class="status-card status-neutral">🕯️ "The journey begins. Week 1 is inscribed."</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-card status-neutral">⚡ "Log your scores to render the horizon."</div>', unsafe_allow_html=True)

# Input Control Block
with st.container(border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        selected_week = st.selectbox("TIMELINE", [f"Week {i}" for i in range(1, 21)])
        week_num = selected_week.split()[1]

    with col2:
        current_val = data.get(week_num)
        val_input = st.number_input(
            "SCORE (0–300)", 
            min_value=0.0, 
            max_value=300.0,
            value=float(current_val) if current_val is not None else 150.0, 
            step=1.0
        )

    if st.button("Log Progression", type="primary", use_container_width=True):
        st.session_state["flow_data"][week_num] = val_input
        if sync_save_data(st.session_state["flow_data"]):
            st.rerun()

# Plot Visual - Fixed Typography & Layout Spacing
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='#0B0C10')
ax.set_facecolor('#11131A')

weeks_labels = [f"W{i}" for i in range(1, 21)]
valid_x = []
valid_y = []

for i in range(1, 21):
    val = data[str(i)]
    if val is not None:
        valid_x.append(f"W{i}")
        valid_y.append(val)

# Ambient Baseline at 150
ax.axhline(y=150, color='#F87171', linestyle=':', linewidth=1.2, alpha=0.6, label='Baseline (150)')

if valid_x:
    ax.plot(
        valid_x, valid_y, 
        marker='o', markersize=6, markerfacecolor='#818CF8', markeredgecolor='#FFFFFF', markeredgewidth=1.2,
        color='#6366F1', linewidth=2.5, 
        label='Flow Horizon'
    )
    for x_val, y_val in zip(valid_x, valid_y):
        ax.annotate(
            f"{int(y_val)}", (x_val, y_val), 
            textcoords="offset points", 
            xytext=(0, 9), ha='center', 
            fontfamily='sans-serif', fontweight='700', fontsize=9, color='#FFFFFF'
        )

# Y-Axis & X-Axis Spacing Fixes
ax.set_ylim(0, 330)
ax.set_xlim(-0.8, 19.8)
ax.set_xticks(range(20))

ax.set_xticklabels(weeks_labels, color='#9CA3AF', fontsize=7.5, fontweight='600')
ax.tick_params(axis='x', pad=6)
ax.tick_params(axis='y', colors='#6B7280', labelsize=8)

for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

ax.grid(True, linestyle='--', alpha=0.08, color='#FFFFFF')

# High-contrast, clean legend
ax.legend(
    loc='upper right', 
    frameon=True, 
    facecolor='#161822', 
    edgecolor='rgba(255, 255, 255, 0.1)', 
    labelcolor='#E0E2EC', 
    fontsize=8.5,
    prop={'weight': '600', 'size': 8.5}
)

plt.tight_layout()

# Render Chart
st.pyplot(fig)

# Reset Button
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("Reset Matrix", use_container_width=True):
        empty_data = {str(i): None for i in range(1, 21)}
        st.session_state["flow_data"] = empty_data
        sync_save_data(empty_data)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
