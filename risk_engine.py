from simulation import SensorReading

def calculate_risk(reading: SensorReading) -> dict:
    # Normalized scores (0 to 100)
    w_rain = 0.25
    w_moist = 0.25
    w_tilt = 0.25
    w_disp = 0.25

    norm_rain = reading.rainfall
    norm_moist = reading.soil_moisture
    norm_tilt = min(100.0, (reading.ground_tilt / 30.0) * 100)
    norm_disp = min(100.0, (reading.ground_displacement / 25.0) * 100)

    score = round((w_rain * norm_rain) + (w_moist * norm_moist) + (w_tilt * norm_tilt) + (w_disp * norm_disp), 1)

    thresholds_crossed = []
    if reading.rainfall > 60: thresholds_crossed.append("Rainfall > 60")
    if reading.soil_moisture > 70: thresholds_crossed.append("Soil Moisture > 70%")
    if reading.ground_tilt > 8: thresholds_crossed.append("Tilt > 8°")
    if reading.ground_displacement > 10: thresholds_crossed.append("Displacement > 10mm")

    if score < 30:
        severity = "Low"
    elif score < 55:
        severity = "Guarded"
    elif score < 75:
        severity = "High"
    else:
        severity = "Critical"

    return {
        "score": score,
        "severity": severity,
        "thresholds_crossed": thresholds_crossed,
        "contributing_factors": {
            "rainfall_impact": round(w_rain * norm_rain, 1),
            "soil_moisture_impact": round(w_moist * norm_moist, 1),
            "ground_tilt_impact": round(w_tilt * norm_tilt, 1),
            "displacement_impact": round(w_disp * norm_disp, 1)
        },
        "formula_version": "1.0-educational"
    }