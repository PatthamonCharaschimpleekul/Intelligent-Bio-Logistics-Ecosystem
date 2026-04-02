import time
from RBA_logic import rba_calculator
from sensor_sim import box_simulator
from traffic_ai import traffic_prediction

def run_biologis_system():
    print("--- BioSmart Logistics System Starting :) ---")

    # 1. Initialize Components
    # Using 40.0°C as the constant ambient stress test
    sensor = box_simulator(start_temp=2.0, ambient_temp=40.0)
    logic = rba_calculator()
    ai = traffic_prediction() # Added () to instantiate the class

    # 2. Train AI before starting
    print("AI is learning from Kaggle dataset...")
    # Use the absolute path or relative path to your CSV
    ai.train_from_csv(r'data\Traffic.csv')

    if not ai.is_trained:
        print("Error: System cannot start without AI training.")
        return

    # --- NEW: STEP 3 - PRE-TRIP ANALYSIS (PLANNING PHASE) ---
    print("\n[STEP 1: PRE-TRIP PLANNING]")
    # Predict traffic for 8 AM Monday
    predicted_traffic = ai.predict_density(hour=8, day_index=0)
    
    # Calculate recommended PCM for a 2-hour planned trip at 40°C
    recommended_pcm = logic.analyze_required_pcm(
        target_hours=2, 
        ambient_temp=40.0, 
        traffic_density=predicted_traffic
    )

    print(f"Predicted Traffic Density: {predicted_traffic}")
    print(f"Required PCM Mass (with 5% Safety Factor): {recommended_pcm} g")
    print("--------------------------------------------------")
    input("System Ready. Press ENTER to start real-time monitoring...")

    # --- STEP 4 - REAL-TIME MONITORING ---
    print("\n[STEP 2: REAL-TIME MONITORING] (Press Ctrl+C to stop)")
    print("-" * 50)

    try:
        # Simulate 20 minutes of delivery (1 loop = 1 second for demo)
        for minute in range(1, 21):
            # A. Get current Internal Temp from sensor
            current_t = sensor.get_temperature()

            # B. Calculate RBA using the recommended PCM mass from our analysis
            # Now passing 4 parameters: (temp_int, temp_amb, pcm_mass, traffic_density)
            t_rba = logic.calculate_rba(
                temp_int=current_t, 
                temp_amb=40.0, 
                pcm_mass=recommended_pcm, 
                traffic_density=predicted_traffic
            )

            # C. Display Dashboard
            print(f"Minute: {minute:02d} | Temp: {current_t:.2f}°C | PCM: {recommended_pcm}g")
            print(f"Traffic Density: {predicted_traffic} | tRBA: {t_rba} mins")

            if t_rba < 30: # Warning threshold adjusted for realism
                print("!!! WARNING: THERMAL BUFFER LOW - SHIPMENT AT RISK !!!")
            
            print("-" * 50)
            time.sleep(1) 

    except KeyboardInterrupt:
        print("\nSystem shut down safely.")

if __name__ == "__main__":
    run_biologis_system()