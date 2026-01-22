# Spacecraft PID Control & Tuning Workbench
# Project Overview:
This interactive web application is a specialized control engineering tool designed to simulate and tune PID (Proportional-Integral-Derivative) controllers for spacecraft pitch motion. The project focuses on a Double Integrator Plant ($1/Js^2$), which is the standard model for the NASA Man Maneuvering Unit (MMU) and satellite attitude control.The goal of this workbench is to bridge the gap between theoretical "perfect" control math and the practical constraints of aerospace hardware, such as actuator limits and sensor noise.
# Theoretical Foundations
**1. Control Methodology**
The app implements two primary tuning strategies discussed in the lecture:
 
**Empirical Tuning (Ziegler-Nichols):** Utilizing the 1942 "Step Response" and "Sustained Oscillation" methods to find initial gains without a full system model.

**Model-Based Tuning (Characteristic Equation Matching):** Using Laplace transforms to match the coefficients of the actual system to a desired performance model.

**2. The Third-Order Challenge**
When applying PID control to a second-order plant, the closed-loop system order increases to three.

**The 10x Rule:** To ensure the system behaves like a predictable second-order model, the app places a "Third Pole" at least 10 times further from the origin than the dominant poles. This ensures the third pole decays rapidly and does not dominate the visible response.

# Key Interactive Features
**1. Dynamic Step Response**
Adjust gains in real-time to observe the impact on performance metrics:
**Rise Time:** Speed of response (improved by $K_p$).
**Overshoot:** The percentage the system exceeds the target (reduced by $K_d$).
**Steady-State Error:** The remaining offset (eliminated by $K_i$).

**2. Practical Constraints Simulation** 
The app includes non-linear physics to demonstrate real-world issues:
**Actuator Saturation:** Simulates the maximum torque limits of physical thrusters.
**Integral Windup & Anti-Windup:** Shows how error accumulation during saturation can cause divergence, and how "reset" logic prevents it.
**Sensor Noise:** Demonstrates how derivative action can amplify jitter, requiring filtering for stability.

**3. Frequency Analysis (Bode Plots)** 
For satellites with flexible appendages (solar arrays/antennas), the controller bandwidth must be carefully selected.Vibration Avoidance: Users can verify that the controller frequency is "low enough" to avoid exciting the flexible modes of the structure.

# Getting Started
**Prerequisites**
Python 3.8+
Libraries: streamlit, numpy, plotly, control

# Installation & Execution
1. Install the required dependencies:

pip install streamlit numpy plotly control
 
2. Run the application locally:

streamlit run control_system_dashboard.py


