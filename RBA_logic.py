class rba_calculator:
    def __init__(self):
        self.cs = 2.1 
        self.cl = 4.2       
        self.L = 180     
        self.tm = 5.0        
        self.ti = 2.0      
        
        # Insulation Properties (VIP Box)
        self.u_value = 0.2   # W/m^2*K
        self.surface_area = 0.35

    def analyze_required_pcm(self, target_hours, ambient_temp, traffic_density):

        estimated_time_sec = target_hours * (1 + (0.5 * traffic_density)) * 3600
        
        temp_diff = ambient_temp - 5.0
        total_heat_load = self.u_value * self.surface_area * temp_diff * estimated_time_sec
        
        energy_per_gram = (self.cs * (self.tm - self.ti)) + self.L + (self.cl * (5.5 - self.tm))
        
        required_mass = (total_heat_load / energy_per_gram) * 1.05
        
        return round(required_mass, 2)

    def calculate_rba(self, temp_int, temp_amb, pcm_mass, traffic_density):

        e_ideal = pcm_mass * (
            (self.cs * (self.tm - self.ti)) + 
            self.L + 
            (self.cl * max(0, temp_int - self.tm))
        )

        temp_diff = max(0.1, temp_amb - temp_int)
        heat_inflow_watts = self.u_value * self.surface_area * temp_diff

        base_time_minutes = (e_ideal / heat_inflow_watts) / 60

        risk_factor = 1 - (0.25 * traffic_density)
        
        final_rba = round(risk_factor * base_time_minutes, 2)
        return final_rba

if __name__ == "__main__":
    logic = rba_calculator()
    
    recommended_pcm = logic.analyze_required_pcm(2, 40, 0.8)
    print(f"Analysis: Recommended PCM Mass: {recommended_pcm} g")
    
    res = logic.calculate_rba(4, 40, recommended_pcm, 0.8)
    print(f"Monitoring: Current tRBA: {res} minutes")