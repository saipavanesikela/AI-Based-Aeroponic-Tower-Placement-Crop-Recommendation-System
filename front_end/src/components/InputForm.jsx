
import { useState } from "react";


const initialForm = {
  temperature: "",
  humidity: "",
  sunlight_hours: "",
  water_ph: "",
  air_quality_index: "",
  wind_speed: ""
};

export default function InputForm({ onResult }) {
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");

  // Validation rules

  const validate = (fields = form) => {
    const newErrors = {};
    // Only show error if value is not empty and invalid
    if (fields.temperature === "" || isNaN(Number(fields.temperature)) || Number(fields.temperature) < 0 || Number(fields.temperature) > 45) {
      newErrors.temperature = "Temperature must be 0-45°C";
    }
    if (fields.humidity === "" || isNaN(Number(fields.humidity)) || Number(fields.humidity) < 20 || Number(fields.humidity) > 100) {
      newErrors.humidity = "Humidity must be 20-100%";
    }
    if (fields.sunlight_hours === "" || isNaN(Number(fields.sunlight_hours)) || Number(fields.sunlight_hours) < 0 || Number(fields.sunlight_hours) > 24) {
      newErrors.sunlight_hours = "Sunlight hours must be 0-24";
    }
    if (fields.water_ph === "" || isNaN(Number(fields.water_ph)) || Number(fields.water_ph) < 4.5 || Number(fields.water_ph) > 8) {
      newErrors.water_ph = "Water pH must be 4.5-8.0";
    }
    if (fields.air_quality_index === "" || isNaN(Number(fields.air_quality_index)) || Number(fields.air_quality_index) < 0 || Number(fields.air_quality_index) > 500) {
      newErrors.air_quality_index = "AQI must be 0-500";
    }
    if (fields.wind_speed === "" || isNaN(Number(fields.wind_speed)) || Number(fields.wind_speed) < 0 || Number(fields.wind_speed) > 5) {
      newErrors.wind_speed = "Wind speed must be 0-5 m/s";
    }
    return newErrors;
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value === undefined || e.target.value === null ? "" : e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
    setSuccessMsg("");
  };

  const handlePredict = () => {
    const validation = validate();
    if (Object.keys(validation).length > 0) {
      setErrors(validation);
      setSuccessMsg("");
      return;
    }
    setErrors({});
    setSuccessMsg("");
    onResult({
      temperature: Number(form.temperature),
      humidity: Number(form.humidity),
      sunlight_hours: Number(form.sunlight_hours),
      water_ph: Number(form.water_ph),
      air_quality_index: Number(form.air_quality_index),
      wind_speed: Number(form.wind_speed)
    });
  };

  return (
    <div className="modern-form-card">
      <div className="form-title" style={{ marginTop: 0 }}>Enter Crop Prediction Details</div>
      <div className="field-grid">
        <div className="form-group">
          <label>Temperature (°C)</label>
          <input
            type="number"
            name="temperature"
            value={form.temperature ?? ""}
            onChange={handleChange}
            min={0}
            max={45}
            step={0.1}
            className={errors.temperature ? "input-error" : ""}
            disabled={loading}
          />
          <div className="form-hint">Keep between 15–30 for most crops.</div>
          {errors.temperature && <div className="error-msg">{errors.temperature}</div>}
        </div>
        <div className="form-group">
          <label>Humidity (%)</label>
          <input
            type="number"
            name="humidity"
            value={form.humidity ?? ""}
            onChange={handleChange}
            min={20}
            max={100}
            step={0.1}
            className={errors.humidity ? "input-error" : ""}
            disabled={loading}
          />
          <div className="form-hint">50–80% works best for leafy greens.</div>
          {errors.humidity && <div className="error-msg">{errors.humidity}</div>}
        </div>
      </div>

      <div className="field-grid">
        <div className="form-group">
          <label>Sunlight Hours</label>
          <input
            type="number"
            name="sunlight_hours"
            value={form.sunlight_hours ?? ""}
            onChange={handleChange}
            min={0}
            max={24}
            step={0.1}
            className={errors.sunlight_hours ? "input-error" : ""}
            disabled={loading}
          />
          <div className="form-hint">Aim for 4–8 hours of usable light.</div>
          {errors.sunlight_hours && <div className="error-msg">{errors.sunlight_hours}</div>}
        </div>
        <div className="form-group">
          <label>Water pH</label>
          <input
            type="number"
            name="water_ph"
            value={form.water_ph ?? ""}
            onChange={handleChange}
            min={4.5}
            max={8}
            step={0.01}
            className={errors.water_ph ? "input-error" : ""}
            disabled={loading}
          />
          <div className="form-hint">Most crops: 5.5–6.5.</div>
          {errors.water_ph && <div className="error-msg">{errors.water_ph}</div>}
        </div>
      </div>

      <div className="field-grid">
        <div className="form-group">
          <label>Air Quality Index</label>
          <input
            type="number"
            name="air_quality_index"
            value={form.air_quality_index ?? ""}
            onChange={handleChange}
            min={0}
            max={500}
            step={1}
            className={errors.air_quality_index ? "input-error" : ""}
            disabled={loading}
          />
          <div className="form-hint">Below 180 avoids heavy penalty.</div>
          {errors.air_quality_index && <div className="error-msg">{errors.air_quality_index}</div>}
        </div>
        <div className="form-group">
          <label>Wind Speed (m/s)</label>
          <input
            type="number"
            name="wind_speed"
            value={form.wind_speed ?? ""}
            onChange={handleChange}
            min={0}
            max={5}
            step={0.1}
            className={errors.wind_speed ? "input-error" : ""}
            disabled={loading}
          />
          <div className="form-hint">Keep under 5 m/s for tower stability.</div>
          {errors.wind_speed && <div className="error-msg">{errors.wind_speed}</div>}
        </div>
      </div>
      <button type="button" onClick={handlePredict} disabled={loading} style={{ marginTop: 10, fontWeight: 600, fontSize: 16 }}>
        Predict Crop Suitability
      </button>
      {successMsg && <div className="success-msg">{successMsg}</div>}
    </div>
  );
}
