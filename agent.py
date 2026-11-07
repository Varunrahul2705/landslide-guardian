from simulation import sim, evaluate_mcu_logic
from risk_engine import calculate_risk
from database import get_recent_readings

# Agent Tools
def tool_get_latest_readings():
    return sim.current_reading.model_dump()

def tool_get_risk():
    return calculate_risk(sim.current_reading)

def tool_get_mcu_status():
    return evaluate_mcu_logic(sim.current_reading)

def run_agent_investigation():
    readings = tool_get_latest_readings()
    risk = tool_get_risk()
    mcu = tool_get_mcu_status()

    # Deterministic reasoning fallback
    primary_causes = []
    if readings["rainfall"] > 60:
        primary_causes.append(f"Elevated rainfall ({readings['rainfall']}) saturation")
    if readings["ground_displacement"] > 8:
        primary_causes.append(f"Physical ground slippage ({readings['ground_displacement']} mm)")
    if readings["ground_tilt"] > 7:
        primary_causes.append(f"Steep incline angle deviation ({readings['ground_tilt']}°)")

    evidence = f"MCU Status: {mcu['status']}. Active thresholds crossed: {', '.join(risk['thresholds_crossed']) if risk['thresholds_crossed'] else 'None'}."
    
    recs = ["Maintain automated 5-second polling interval."]
    if risk["severity"] in ["High", "Critical"]:
        recs.append("Trigger virtual digital twin warning state.")
        recs.append("Flag event for incident review.")

    return {
        "status": "success",
        "agent_mode": "deterministic_fallback",
        "summary": f"Calculated risk is {risk['severity']} (Score: {risk['score']}/100). " + 
                   ("Key drivers: " + ", ".join(primary_causes) if primary_causes else "All parameters within normal tolerance."),
        "evidence": evidence,
        "recommendations": recs,
        "limitations": "Simulated output for educational demonstration only. Not calibrated for actual civil protection."
    }