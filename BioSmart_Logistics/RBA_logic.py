def calculate_rba(temp_int, temp_amb, pcm_mass, traffic_density):
    latent_heat = 180
    u_value = 0.2 # Realistic U-Value for 25mm VIP Insulation (W/m^2*K)
    surface_area = 0.35

    total_energy_joules = pcm_mass * latent_heat

    # Heat Flow (Q) = U * A * Delta_T
    temp_diff = max(0.1, temp_amb - temp_int) #0.1 aviod zero deff (prevent runtime error)
    heat_inflow_watts = u_value * surface_area * temp_diff

    base_time_seconds = total_energy_joules / heat_inflow_watts
    base_time_minutes = base_time_seconds / 60

    risk_factor = 1 - (0.25 * traffic_density)

    final_rba = risk_factor * base_time_minutes
    return final_rba

if __name__ == "__main__":
    # Test with realistic VIP Box: 500g PCM, 40C Outside, 4C Inside, Heavy Traffic (0.8)
    res = calculate_rba(4, 40, 500, 0.8)
    print(res, " minutes")