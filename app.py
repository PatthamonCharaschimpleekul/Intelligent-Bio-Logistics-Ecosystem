import streamlit as st
import pandas as pd
from traffic_ai import traffic_prediction
from RBA_logic import rba_calculator

st.set_page_config(page_title="BioSmart Dashboard")
st.title("Intelligent Bio-Logistics Ecosystem")

#initial AI logic
@st.cache_resource
def load_system():
    ai = traffic_prediction
    ai.train_from_csv('data\Traffic.csv')
    logic = rba_calculator()
    return ai, logic

ai, logic = load_system()

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
col1, col2, col3 = st.columns[3]
col1.metric("Traffic density", f"{predict_traffic}")
col2.metric("Estimated time", f"{target_hours* (1 + 0.5*predict_traffic):.1f} hrs")
col3.metric("Recommended PCM", f"{recommended_pcm} g", delta = "+5% Safty")

st.divider

#Simulation segment
st.header("Step 2: Real-Time Monitoring Simulation")
if st.button("Start Delivery Simulation"):
    progess_bar = st.progress(0)
    status_text = st.empty()

elapsed_time = st.slider("Simulate Elapsed Time (Hours)", 0.0, target_hours, 0.0)

simulated_temp = 2.0 + (elapsed_time * 1.5) 
current_trba = logic.calculate_rba(simulated_temp, ambient_temp, recommended_pcm, predict_traffic)

st.metric("Predicted Internal Temp", f"{simulated_temp:.1f} °C")
st.metric("Remaining Safety Window", f"{current_trba:.0f} mins")