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
