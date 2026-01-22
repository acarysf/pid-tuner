import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Control Systems Workbench", layout="wide")
st.title("🛰️ Control Systems Design & PID Tuning Workbench")
st.markdown("---")

# --- 2. THEORETICAL OVERVIEW (Citations from Lecture) ---
st.header("1. Controller Design Process")
col_a, col_b = st.columns(2)
with col_a:
    st.write("**Key Principles:**")
    st.write("* **Stability First:** Stability is the first and major requirement[cite: 49].")
    st.write("* **Flow Down:** Requirements flow from system to sub-system and actuator levels[cite: 28].")
    st.write("* **Algorithm Selection:** Finding the proper algorithm to minimize error and satisfy performance[cite: 29].")

with col_b:
    st.write("**Tuning Methodology:**")
    st.write("* **Empirical:** Ziegler-Nichols (1942) provides a starting point for unknown systems[cite: 91, 92].")
    st.write("* **Model-Based:** Characteristic Equation Matching (Pole Placement) for known plants[cite: 41, 143].")

# --- 3. INTERACTIVE PID SIMULATOR ---
st.header("2. Interactive Simulation: Pitch Motion ($1/Js^2$)")
st.write("This simulation uses the **Spacecraft Man Maneuvering Unit (MMU)** model[cite: 164, 170].")

with st.sidebar:
    st.header("Design Parameters")
    J = st.number_input("Spacecraft Inertia (J)", value=1.0, step=0.1) # 
    
    st.subheader("PID Tuning [cite: 56]")
    Kp = st.slider("Proportional (Kp) - Fixes Rise Time", 0.0, 50.0, 15.0)
    Ki = st.slider("Integral (Ki) - Fixes Steady State Error", 0.0, 20.0, 5.0)
    Kd = st.slider("Derivative (Kd) - Reduces Overshoot", 0.0, 30.0, 10.0)
    
    st.subheader("Practical Issues [cite: 31, 32]")
    sat_limit = st.slider("Actuator Saturation (Max Torque)", 0.1, 10.0, 2.0)
    noise_lvl = st.slider("Sensor Noise Level", 0.0, 0.1, 0.02)
    anti_windup = st.checkbox("Enable Anti-Windup Logic", value=True)

# Simulation Engine
dt, t_total = 0.01, 20.0
t = np.arange(0, t_total, dt)
theta, vel, err_sum, prev_err = 0.0, 0.0, 0.0, 0.0
history = []

for _ in t:
    # Sensor noise implementation [cite: 32]
    measured = theta + np.random.normal(0, noise_lvl)
    err = 1.0 - measured # Reference tracking [cite: 24]
    
    # PID Logic [cite: 196]
    u = (Kp * err) + (Ki * err_sum * dt) + (Kd * (err - prev_err) / dt)
    
    # Saturation & Windup [cite: 254, 255]
    if abs(u) > sat_limit:
        u = np.sign(u) * sat_limit
        if anti_windup: err_sum -= err # Reset logic [cite: 256]
            
    # Plant Physics (Double Integrator) [cite: 64, 187]
    accel = u / J
    vel += accel * dt
    theta += vel * dt
    err_sum += err
    prev_err = err
    history.append(theta)

# Visualization

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=history, name="Theta Response", line=dict(color="#00CC96", width=2)))
fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Reference")
fig.update_layout(title="Time-Domain Step Response", xaxis_title="Time (s)", yaxis_title="Pitch Angle (rad)")
st.plotly_chart(fig, use_container_width=True)

# --- 4. PERFORMANCE & TROUBLESHOOTING ---
st.header("3. Performance Assessment [cite: 48]")
p_col1, p_col2 = st.columns(2)

with p_col1:
    st.subheader("Troubleshooting Matrix")
    st.table({
        "Observation": ["High Overshoot", "Steady-State Error", "Actuator Jitter", "Divergence"],
        "Correction": ["Increase Kd ", "Increase Ki [cite: 58]", "Filter Noise [cite: 252]", "Check Anti-Windup [cite: 255]"]
    })

with p_col2:
    st.subheader("Flexible Dynamics Note [cite: 270]")
    st.warning("""
    **Bandwidth Caution:** Ensure your controller bandwidth stays below the flexible frequency (e.g., solar arrays) 
    to avoid exciting structural vibrations[cite: 271, 274].
    """)