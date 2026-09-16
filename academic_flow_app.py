import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = "academic_flow_data.json"

class AcademicFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Flow Tracker")
        self.root.geometry("900x700")

        self.data = {str(i): None for i in range(1, 21)}
        self.load_data()
        self.setup_ui()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    saved_data = json.load(f)
                    self.data.update(saved_data)
            except Exception:
                pass

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def setup_ui(self):
        # Top Frame for Input Controls
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(input_frame, text="Select Week:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        
        self.week_var = tk.StringVar()
        self.week_dropdown = ttk.Combobox(input_frame, textvariable=self.week_var, width=8, state="readonly")
        self.week_dropdown['values'] = [f"Week {i}" for i in range(1, 21)]
        
        first_empty = 1
        for i in range(1, 21):
            if self.data[str(i)] is None:
                first_empty = i
                break
        self.week_dropdown.current(first_empty - 1)
        self.week_dropdown.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Value (0-300):", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        
        self.entry = tk.Entry(input_frame, font=("Arial", 11), width=8)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.week_dropdown.bind("<<ComboboxSelected>>", self.on_week_select)
        self.on_week_select()

        self.root.bind('<Return>', lambda event: self.save_value())

        self.save_btn = tk.Button(input_frame, text="Save & Plot", font=("Arial", 10, "bold"), 
                                  bg="#2196F3", fg="white", command=self.save_value)
        self.save_btn.pack(side=tk.LEFT, padx=15)

        # Dynamic Status / Motivation Banner Frame
        feedback_frame = tk.Frame(self.root, bg="#F5F5F5", pady=6)
        feedback_frame.pack(side=tk.TOP, fill=tk.X, padx=15, pady=(0, 10))

        self.feedback_label = tk.Label(
            feedback_frame, 
            text="Log scores to track your flow!", 
            font=("Arial", 12, "bold"), 
            bg="#F5F5F5", 
            fg="#555555"
        )
        self.feedback_label.pack(side=tk.TOP)

        # Matplotlib Graph Setup
        self.fig, self.ax = plt.subplots(figsize=(8, 4.8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_graph()

    def on_week_select(self, event=None):
        selected_str = self.week_var.get()
        week_num = selected_str.split()[1]
        val = self.data.get(week_num)
        self.entry.delete(0, tk.END)
        if val is not None:
            self.entry.insert(0, str(val))

    def save_value(self):
        selected_str = self.week_var.get()
        week_num = selected_str.split()[1]
        user_input = self.entry.get().strip()

        if user_input == "":
            self.data[week_num] = None
            self.save_data()
            self.draw_graph()
            return

        try:
            val = float(user_input)
            if 0 <= val <= 300:
                self.data[week_num] = val
                self.save_data()
                self.draw_graph()
            else:
                messagebox.showerror("Invalid Value", "Number must be strictly between 0 and 300.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def update_feedback(self, valid_values):
        if len(valid_values) >= 2:
            latest = valid_values[-1]
            prev = valid_values[-2]
            
            if latest > prev:
                self.feedback_label.config(
                    text="🔥 Damn dude, you are cooking!", 
                    fg="#2E7D32" # Bold Green
                )
            elif latest < prev:
                self.feedback_label.config(
                    text="💀 Man you are getting cooked. Read more!", 
                    fg="#D32F2F" # Bold Red
                )
            else:
                self.feedback_label.config(
                    text="⚡ Holding steady. Push for the spike next week!", 
                    fg="#1976D2" # Blue
                )
        elif len(valid_values) == 1:
            self.feedback_label.config(
                text="🚀 Week 1 locked in. Let's build a streak!", 
                fg="#1976D2"
            )
        else:
            self.feedback_label.config(
                text="Log scores to track your flow!", 
                fg="#555555"
            )

    def draw_graph(self):
        self.ax.clear()

        self.ax.set_ylim(0, 300)
        self.ax.set_xlim(1, 20)

        # Baseline visuals
        self.ax.axhline(150, color='#E53935', linestyle='--', linewidth=1.5, label='Baseline (150)')
        self.ax.axhspan(0, 150, facecolor='#FFEBEE', alpha=0.5)
        self.ax.axhspan(150, 300, facecolor='#E8F5E9', alpha=0.5)

        valid_weeks = []
        valid_values = []
        for i in range(1, 21):
            val = self.data[str(i)]
            if val is not None:
                valid_weeks.append(i)
                valid_values.append(val)

        # Trigger dynamic text banner update
        self.update_feedback(valid_values)

        if valid_weeks:
            self.ax.plot(valid_weeks, valid_values, marker='o', linestyle='-', 
                         color='#1E88E5', linewidth=2.5, markersize=7, label='Academic Progression')
            
            for w, v in zip(valid_weeks, valid_values):
                self.ax.annotate(f"{int(v) if v.is_integer() else v}", (w, v), 
                                 textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9, fontweight='bold')

        self.ax.set_xticks(range(1, 21))
        self.ax.set_xticklabels([f"Wk {i}" for i in range(1, 21)], rotation=45, fontsize=8)

        self.ax.set_title("20-Week Academic Flow Tracker", fontsize=13, fontweight='bold', pad=12)
        self.ax.set_xlabel("Weeks", fontsize=10)
        self.ax.set_ylabel("Performance Level (0-300)", fontsize=10)
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.legend(loc="upper left")

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AcademicFlowApp(root)
    root.mainloop()
    import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "academic_flow_data.json"

st.set_page_config(page_title="Academic Flow Tracker", layout="centered")

st.title("📈 Academic Flow Tracker")

# Load existing data
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
    selected_week = st.selectbox("Select Week", [f"Week {i}" for i in range(1, 21)])
    week_num = selected_week.split()[1]

with col2:
    current_val = data.get(week_num)
    val_input = st.number_input("Value (0-300)", min_value=0.0, max_value=300.0, 
                                value=float(current_val) if current_val is not None else 150.0, step=1.0)

if st.button("Save & Update Flow", type="primary", use_container_width=True):
    data[week_num] = val_input
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    st.rerun()

# Dynamic Status Banner
valid_scores = [data[str(i)] for i in range(1, 21) if data[str(i)] is not None]

if len(valid_scores) >= 2:
    latest = valid_scores[-1]
    prev = valid_scores[-2]
    if latest > prev:
        st.success("🔥 Damn dude, you are cooking!")
    elif latest < prev:
        st.error("💀 Man you are getting cooked. Read more!")
    else:
        st.info("⚡ Holding steady. Push for the spike next week!")
elif len(valid_scores) == 1:
    st.info("🚀 Week 1 locked in. Let's build a streak!")

# Data formatting for chart
df_data = []
for i in range(1, 21):
    val = data[str(i)]
    df_data.append({"Week": f"Wk {i}", "Score": val if val is not None else None})

df = pd.DataFrame(df_data)

# Visual Chart
st.subheader("Progress Chart")
st.line_chart(df.set_index("Week"))
