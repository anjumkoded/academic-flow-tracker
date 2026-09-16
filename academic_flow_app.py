import streamlit as st
import matplotlib.pyplot as plt
import json
import os

DATA_FILE = "academic_flow_data.json"

st.set_page_config(page_title="Academic Flow Tracker", layout="centered")

# Load existing data
data = {str(i): None for i in range(1, 21)}
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            data.update(json.load(f))
    except Exception:
        pass

# Top Input Controls
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    selected_week = st.selectbox("Select Week:", [f"Week {i}" for i in range(1, 21)])
    week_num = selected_week.split()[1]

with col2:
    current_val = data.get(week_num)
    val_input = st.number_input("Value (0-300):", min_value=0.0, max_value=300.0,
                                value=float(current_val) if current_val is not None else 150.0, step=1.0)

with col3:
    st.write("")
    st.write("")
    if st.button("Save & Plot", type="primary", use_container_width=True):
        data[week_num] = val_input
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        st.rerun()

# Dynamic Status Banner
entered_weeks = [i for i in range(1, 21) if data[str(i)] is not None]

if len(entered_weeks) >= 2:
    latest = data[str(entered_weeks[-1])]
    prev = data[str(entered_weeks[-2])]
    if latest > prev:
        st.success("🔥 Damn dude, you are cooking!")
    elif latest < prev:
        st.error("😜 Man you are getting cooked. Read more!")
    else:
        st.info("⚡ Holding steady. Push for the spike next week!")
elif len(entered_weeks) == 1:
    st.info("🚀 Week 1 locked in. Let's build a streak!")

# Build Matplotlib Chart Matching Desktop Layout
fig, ax = plt.subplots(figsize=(10, 5))

weeks_labels = [f"Wk {i}" for i in range(1, 21)]
valid_x = []
valid_y = []

for i in range(1, 21):
    val = data[str(i)]
    if val is not None:
        valid_x.append(f"Wk {i}")
        valid_y.append(val)

# Red dashed Baseline at 150
ax.axhline(y=150, color='r', linestyle='--', label='Baseline (150)')

# Plot Progression line + dots + score numbers above dots
if valid_x:
    ax.plot(valid_x, valid_y, marker='o', color='#1f77b4', linewidth=2, label='Academic Progression')
    for x_val, y_val in zip(valid_x, valid_y):
        ax.annotate(f"{y_val:g}", (x_val, y_val), textcoords="offset points", 
                    xytext=(0, 8), ha='center', fontweight='bold', fontsize=9)

# Axis & Grid Formatting
ax.set_ylim(0, 300)
ax.set_xlim(-0.5, 19.5)
ax.set_xticks(range(20))
ax.set_xticklabels(weeks_labels, rotation=45, ha='right')

ax.set_title("20-Week Academic Flow Tracker", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Weeks", fontsize=11, fontweight='bold')
ax.set_ylabel("Performance Level (0-300)", fontsize=11, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left', framealpha=0.9)

plt.tight_layout()

# Render chart inside Streamlit
st.pyplot(fig)

# Reset Button
if st.button("Reset All Data"):
    data = {str(i): None for i in range(1, 21)}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    st.rerun()
