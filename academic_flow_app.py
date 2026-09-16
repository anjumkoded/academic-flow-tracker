import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "academic_flow_data.json"

st.set_page_config(page_title="Academic Flow Tracker", layout="centered")

st.title("📈 Academic Flow Tracker")

# Initialize data
data = {str(i): None for i in range(1, 21)}
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            data.update(json.load(f))
    except Exception:
        pass

# Input Controls
st.subheader("Update Weekly Score")
col1, col2 = st.columns(2)

with col1:
    selected_week_num = st.selectbox("Select Week", range(1, 21), format_func=lambda x: f"Week {x}")
    week_key = str(selected_week_num)

with col2:
    current_val = data.get(week_key)
    val_input = st.number_input("Value (0-300)", min_value=0.0, max_value=300.0, 
                                value=float(current_val) if current_val is not None else 150.0, step=1.0)

btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    if st.button("Save & Update Flow", type="primary", use_container_width=True):
        data[week_key] = val_input
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        st.rerun()

with btn_col2:
    if st.button("Reset All", use_container_width=True):
        data = {str(i): None for i in range(1, 21)}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        st.rerun()

# Dynamic Status Banner (Chronological Check)
entered_weeks = [i for i in range(1, 21) if data[str(i)] is not None]

if len(entered_weeks) >= 2:
    latest_week = entered_weeks[-1]
    prev_week = entered_weeks[-2]
    latest = data[str(latest_week)]
    prev = data[str(prev_week)]
    
    if latest > prev:
        st.success("🔥 Damn dude, you are cooking!")
    elif latest < prev:
        st.error("💀 Man you are getting cooked. Read more!")
    else:
        st.info("⚡ Holding steady. Push for the spike next week!")
elif len(entered_weeks) == 1:
    st.info("🚀 Week 1 locked in. Let's build a streak!")

# Numerical formatting so X-axis orders 1 through 20 cleanly
df_data = [{"Week": i, "Score": data[str(i)]} for i in range(1, 21)]
df = pd.DataFrame(df_data)

st.subheader("Progress Chart")
st.line_chart(df.set_index("Week"))
