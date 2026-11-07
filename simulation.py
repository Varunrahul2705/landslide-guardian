import random
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class SensorReading(BaseModel):
    timestamp: str
    rainfall: float = Field(ge=0, le=100)           # 0 to 100
    soil_moisture: float = Field(ge=0, le=100)      # 0 to 100%
    ground_tilt: float = Field(ge=0, le=45)         # 0 to 45 deg
    ground_displacement: float = Field(ge=0, le=50) # 0 to 50 mm
    source: str = "simulated"

class SimulationState:
    def __init__(self):
        self.is_running = False
        self.current_reading = SensorReading(
            timestamp=datetime.now(timezone.utc).isoformat(),
            rainfall=10.0,
            soil_moisture=20.0,
            ground_tilt=1.5,
            ground_displacement=0.5
        )

    def step(self, scenario: str = "normal") -> SensorReading:
        if scenario == "heavy_rainfall":
            self.current_reading.rainfall = min(100.0, self.current_reading.rainfall + random.uniform(5, 12))
            self.current_reading.soil_moisture = min(100.0, self.current_reading.soil_moisture + random.uniform(4, 9))
        elif scenario == "movement":
            self.current_reading.ground_tilt = min(45.0, self.current_reading.ground_tilt + random.uniform(0.5, 2.0))
            self.current_reading.ground_displacement = min(50.0, self.current_reading.ground_displacement + random.uniform(1.0, 3.5))
        elif scenario == "severe":
            self.current_reading.rainfall = min(100.0, self.current_reading.rainfall + random.uniform(8, 15))
            self.current_reading.soil_moisture = min(100.0, self.current_reading.soil_moisture + random.uniform(6, 12))
            self.current_reading.ground_tilt = min(45.0, self.current_reading.ground_tilt + random.uniform(1.0, 3.0))
            self.current_reading.ground_displacement = min(50.0, self.current_reading.ground_displacement + random.uniform(2.0, 5.0))
        else: # normal drift
            self.current_reading.rainfall = max(0.0, min(100.0, self.current_reading.rainfall + random.uniform(-1, 1)))
            self.current_reading.soil_moisture = max(0.0, min(100.0, self.current_reading.soil_moisture + random.uniform(-0.5, 0.5)))
            self.current_reading.ground_tilt = max(0.0, min(45.0, self.current_reading.ground_tilt + random.uniform(-0.1, 0.1)))
            self.current_reading.ground_displacement = max(0.0, min(50.0, self.current_reading.ground_displacement + random.uniform(-0.1, 0.1)))

        self.current_reading.timestamp = datetime.now(timezone.utc).isoformat()
        return self.current_reading

# Simulated MCU firmware logic
def evaluate_mcu_logic(reading: SensorReading) -> dict:
    alarms = []
    status = "NORMAL"

    if reading.rainfall > 70 or reading.soil_moisture > 75:
        status = "WARNING"
        alarms.append("MCU_WARN: High hydrological load detected.")

    if reading.ground_tilt > 10.0 or reading.ground_displacement > 15.0:
        status = "CRITICAL"
        alarms.append("MCU_ALARM: Slope deformation exceeds safety limits!")

    return {
        "status": status,
        "alarms": alarms,
        "timestamp": reading.timestamp,
        "firmware_version": "v1.0.4-sim"
    }

sim = SimulationState()