import random
import time

class box_simulator:
    def __init__(self, start_temp=2.0, ambient_temp=40.0):
        self.current_temp = start_temp
        self.ambient_temp = ambient_temp
        self.rise_rate_pen_min = 0.05 # How fast the temp rises per minute when PCM is active (Very slow)
    
    def get_temperature(self):
        """Simulates a sensor reading. Temp creep up slowly"""
        #add a tiny random noise :)
        noise = random.uniform(-1.0,1.0)
        self.current_temp += self.rise_rate_pen_min + noise

        self.current_temp = min(self.current_temp, self.ambient_temp)
        return round(self.current_temp, 2)
    
#test
if __name__ == "__main__":
    sim = box_simulator(ambient_temp=40.0)
    print("Simulating 5 minutes of heat soak at 40°C...")
    for _ in range(5):
        print(f"Internal Temp: {sim.get_temperature()}°C")
        time.sleep(0.5) # Fast-forward for demo