<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from simulation import sim, evaluate_mcu_logic, SensorReading
from risk_engine import calculate_risk
import database as db
import agent

app = FastAPI(title="Landslide Guardian AI")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "Landslide Guardian AI"}

@app.get("/api/readings/latest")
def get_latest():
    r = sim.current_reading
    mcu = evaluate_mcu_logic(r)
    risk = calculate_risk(r)
    return {"reading": r, "mcu": mcu, "risk": risk}

@app.get("/api/readings/history")
def get_history():
    return db.get_recent_readings(25)

@app.post("/api/simulation/step")
def step_simulation(scenario: str = "normal"):
    reading = sim.step(scenario)
    db.save_reading(reading)
    risk = calculate_risk(reading)
    
    if risk["severity"] in ["High", "Critical"]:
        db.save_incident(risk["severity"], risk["score"], f"Threshold alert at score {risk['score']}", reading.model_dump())

    return {"reading": reading, "risk": risk}

@app.post("/api/sensors/override")
def override_sensors(data: SensorReading):
    data.source = "manual"
    sim.current_reading = data
    db.save_reading(data)
    return {"status": "overridden", "reading": data}

@app.post("/api/agent/investigate")
def investigate():
    return agent.run_agent_investigation()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
=======

>>>>>>> a6bf779d7f22137b5ee31c6d9711eba3c71922d6
