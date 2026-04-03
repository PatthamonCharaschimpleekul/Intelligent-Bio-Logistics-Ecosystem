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