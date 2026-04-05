import streamlit as st
import pandas as pd
from traffic_ai import traffic_prediction
from RBA_logic import rba_calculator
import time

st.set_page_config(page_title="BioSmart Dashboard", layout="wide")
st.title("Intelligent Bio-Logistics Ecosystem")

#initial AI logic
@st.cache_resource
def init_system():
    ai = traffic_prediction()
    ai.train_from_csv(r'data\Traffic.csv')
    logic = rba_calculator()
    return ai, logic

ai, logic = init_system()

#Sidebar user input
st.sidebar.header("Step 1: Pre-trip Planning")
target_hours = st.sidebar.number_input("Standard travel duraton (hours)" , min_value=0.5, value=2.0)
ambient_temp =st.sidebar.slider("Ambient Temoerature (°C)", 30, 50, 40)
trip_hour = st.sidebar.slider("Departure hour", 0, 23, 8)
trip_day = st.sidebar.selectbox("Day of week", options=[0,1,2,3,4,5,6], format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x])

#Logic AI analysis
predict_traffic = ai.predict_density(trip_hour, trip_day)
recommended_pcm = logic.analyze_required_pcm(target_hours, ambient_temp, predict_traffic)

#AI main dashboard display
col1, col2, col3 = st.columns(3)
col1.metric("Traffic density", f"{predict_traffic}")
col2.metric("Estimated time", f"{target_hours* (1 + 0.5*predict_traffic):.1f} hrs")
col3.metric("Recommended PCM", f"{recommended_pcm} g", delta = "+5% Safety")

st.divider()

#Simulation segment
# Simulation segment
st.header("Step 2: Real-Time Monitoring Simulation")

# Create two columns for a cleaner look
sim_col1, sim_col2 = st.columns([1, 2])

with sim_col1:
    st.subheader("Manual Check")
    # Manual Slider: Let users play with the timeline
    elapsed_time = st.slider("Simulate Elapsed Time (Hours)", 0.0, target_hours, 0.0)
    
    # Calculate values based on slider
    simulated_temp = 2.0 + (elapsed_time * 1.5) 
    current_trba = logic.calculate_rba(simulated_temp, ambient_temp, recommended_pcm, predict_traffic)

    st.metric("Internal Temp", f"{simulated_temp:.1f} °C")
    st.metric("Remaining Window (tRBA)", f"{current_trba:.0f} mins")

with sim_col2:
    st.subheader("Auto-Run Demo")
    if st.button("Start Delivery Simulation"):
        progress_bar = st.progress(0)
        status_text = st.empty() # We keep this to show real-time updates
        
        # Simulate 10 steps of the journey
        for i in range(1, 11):
            # Calculate simulation logic
            sim_elapsed = (target_hours / 10) * i
            sim_temp = 2.0 + (sim_elapsed * 1.5)
            sim_trba = logic.calculate_rba(sim_temp, ambient_temp, recommended_pcm, predict_traffic)
            
            # Update the UI
            progress_bar.progress(i * 10)
            status_text.info(f"🚚 Shipping Status: {i*10}% complete | Current Temp: {sim_temp:.1f}°C")
            
            time.sleep(0.3) # Fast-forward for demo
        
        st.success("✅ Simulation Finished! Shipment data verified.")
