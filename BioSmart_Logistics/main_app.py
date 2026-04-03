import time
from RBA_logic import rba_calculator
from sensor_sim import box_simulator
from traffic_ai import traffic_prediction

def run_biologis_system():
    print("--- BioSmart Logistics System Starting :) ---")

    # 1. Initialize Components
    # Ensure sensor_sim has a class/function named box_simulator
    sensor = box_simulator(start_temp=2.0, ambient_temp=40.0)
    
    # Ensure RBA_logic has a class/function named rba_calculator
    logic = rba_calculator()
    
    # Ensure traffic_ai has a class/function named traffic_prediction
    ai = traffic_prediction() 

    # 2. Train AI before starting
    print("AI is learning from Kaggle dataset...")
    ai.train_from_csv(r'data\Traffic.csv')

    if not ai.is_trained:
        print("Error: System cannot start without AI training.")
        return

    # --- STEP 1: PRE-TRIP PLANNING ---
    print("\n[STEP 1: PRE-TRIP PLANNING]")
    
    # Calling function from traffic_ai
    predicted_traffic = ai.predict_density(hour=8, day_index=0)
    
    # Calling planning function from RBA_logic
    recommended_pcm = logic.analyze_required_pcm(
        target_hours=2, 
        ambient_temp=40.0, 
        traffic_density=predicted_traffic
    )

    print(f"Predicted Traffic Density: {predicted_traffic}")
    print(f"Required PCM Mass (with 5% Safety Factor): {recommended_pcm} g")
    print("--------------------------------------------------")
    input("System Ready. Press ENTER to start real-time monitoring...")

    # --- STEP 2: REAL-TIME MONITORING ---
    print("\n[STEP 2: REAL-TIME MONITORING] (Press Ctrl+C to stop)")
    print("-" * 50)

    try:
        for minute in range(1, 21):
            # A. Get Temp
            current_t = sensor.get_temperature()

            # B. Calculate RBA
            # Ensure the function in rba_calculator accepts these 4 arguments
            t_rba = logic.calculate_rba(
                temp_int=current_t, 
                temp_amb=40.0, 
                pcm_mass=recommended_pcm, 
                traffic_density=predicted_traffic
            )

            # C. Dashboard display
            print(f"Minute: {minute:02d} | Temp: {current_t:.2f}°C | PCM: {recommended_pcm}g")
            print(f"Traffic Density: {predicted_traffic} | tRBA: {t_rba} mins")

            if t_rba < 30:
                print("!!! WARNING: THERMAL BUFFER LOW - SHIPMENT AT RISK !!!")
            
            print("-" * 50)
            time.sleep(1) 

    except KeyboardInterrupt:
        print("\nSystem shut down safely.")

if __name__ == "__main__":
    run_biologis_system()