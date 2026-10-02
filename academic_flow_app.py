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

# Custom High-End Minimal & Poetic CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

    /* Global Dark Canvas */
    .stApp {
        background: #0B0C10;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #E0E2EC;
    }

    /* Hide default clutter */
    header, footer, #MainMenu { visibility: hidden; display: none; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 480px; }

    /* Minimalist Title Area */
    .brand-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .brand-subtitle {
        font-size: 0.78rem;
        font-weight: 300;
        color: #6366F1;
        text-align: center;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 1.8rem;
    }

    /* Poetic Banner Cards */
    .status-card {
        padding: 16px 20px;
        border-radius: 16px;
        font-size: 0.9rem;
        font-weight: 400;
        letter-spacing: 0.02em;
        text-align: center;
        margin-bottom: 1.5rem;
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

    /* Input Glass Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(21, 23, 30, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
    }

    /* Selectbox & Inputs */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #161822 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #E0E2EC !important;
    }
    
    input {
        color: #E0E2EC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Elegant Indigo Glow Button */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.05em !important;
        padding: 12px !important;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 24px rgba(79, 70, 229, 0.55) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary Reset Button */
    .reset-btn > div > button {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #6B7280 !important;
        box-shadow: none !important;
    }
    .reset-btn > div > button:hover {
        color: #EF4444 !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Read Secrets
BIN_ID = st.secrets["JSONBIN_BIN_ID"]
API_KEY = st.secrets["JSONBIN_API_KEY"]

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": API_KEY
}

# Helper functions for JSONBin
def load_data():
    try:
        response = requests.get(f"{URL}/latest", headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("record", {})
    except Exception:
        pass
    return {}

def save_data(data_dict):
    try:
        requests.put(URL, headers=HEADERS, json=data_dict)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Fetch remote data
raw_data = load_data()
data = {str(i): raw_data.get(str(i)) for i in range(1, 21)}

# Brand Header
st.markdown('<div class="brand-title">A C A D E M I A</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">The Arc of Momentum</div>', unsafe_allow_html=True)

# Dynamic Poetic Status Banners
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

# Control Center Container
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
        data[week_num] = val_input
        save_data(data)
        st.rerun()

# Canvas Style Matplotlib Visual
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 4.8), facecolor='#0B0C10')
ax.set_facecolor('#11131A')

weeks_labels = [f"W{i}" for i in range(1, 21)]
valid_x = []
valid_y = []

for i in range(1, 21):
    val = data[str(i)]
    if val is not None:
        valid_x.append(f"W{i}")
        valid_y.append(val)

# Ambient Red Baseline at 150
ax.axhline(y=150, color='#F87171', linestyle=':', linewidth=1.2, alpha=0.5, label='Baseline (150)')

# Glowing Indigo Curve & Soft Data Nodes
if valid_x:
    ax.plot(
        valid_x, valid_y, 
        marker='o', markersize=6, markerfacecolor='#818CF8', markeredgecolor='#FFFFFF', markeredgewidth=1.2,
        color='#6366F1', linewidth=2.5, 
        label='Flow Horizon'
    )
    for x_val, y_val in zip(valid_x, valid_y):
        ax.annotate(
            f"{y_val:g}", (x_val, y_val), 
            textcoords="offset points", 
            xytext=(0, 9), ha='center', 
            fontfamily='sans-serif', fontweight='600', fontsize=8.5, color='#F3F4F6'
        )

# Axis & Grid Formatting
ax.set_ylim(0, 310)
ax.set_xlim(-0.5, 19.5)
ax.set_xticks(range(20))
ax.set_xticklabels(weeks_labels, rotation=0, color='#4B5563', fontsize=7.5, fontweight='500')
ax.tick_params(axis='y', colors='#4B5563', labelsize=8)

# Clean Spines
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

ax.grid(True, linestyle='-', alpha=0.04, color='#FFFFFF')
ax.legend(loc='upper left', frameon=False, labelcolor='#6B7280', fontsize=8.5)

plt.tight_layout()

# Render Chart inside Glass Container
with st.container(border=True):
    st.pyplot(fig)

# Minimal Reset Button
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("Reset Matrix", use_container_width=True):
        empty_data = {str(i): None for i in range(1, 21)}
        save_data(empty_data)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
