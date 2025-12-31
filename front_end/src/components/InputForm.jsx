import { useState } from "react";
import { predictCrops } from "../services/api";

export default function InputForm({ onResult }) {
  const [form, setForm] = useState({
    temperature: 26,
    humidity: 65,
    wind_speed: 2,
    sunlight_hours: 7,
    x_coord: 5,
    y_coord: 5,
    spacing: 1.2,
    shade_percent: 10
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: Number(e.target.value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await predictCrops(form);
    onResult(result);
  };

  return (
    <div className="card">
      <h3>Environmental Conditions</h3>

      <form onSubmit={handleSubmit}>
        {/* Temperature */}
        <div className="form-group">
          <label>Temperature (°C): {form.temperature}</label>
          <input
            type="range"
            name="temperature"
            min="0"
            max="45"
            value={form.temperature}
            onChange={handleChange}
          />
        </div>

        {/* Humidity */}
        <div className="form-group">
          <label>Humidity (%): {form.humidity}</label>
          <input
            type="range"
            name="humidity"
            min="20"
            max="100"
            value={form.humidity}
            onChange={handleChange}
          />
        </div>

        {/* Sunlight */}
        <div className="form-group">
          <label>Sunlight Hours: {form.sunlight_hours}</label>
          <input
            type="range"
            name="sunlight_hours"
            min="0"
            max="24"
            value={form.sunlight_hours}
            onChange={handleChange}
          />
        </div>

        {/* Spacing */}
        <div className="form-group">
          <label>Spacing (meters)</label>
          <input
            type="number"
            name="spacing"
            min="0.5"
            max="5.0"
            step="0.1"
            value={form.spacing}
            onChange={handleChange}
          />
        </div>

        {/* Wind Speed */}
        <div className="form-group">
          <label>Wind Speed (m/s)</label>
          <input
            type="number"
            name="wind_speed"
            value={form.wind_speed}
            onChange={handleChange}
          />
        </div>

        {/* Shade Percentage */}
        <div className="form-group">
          <label>Shade Percentage</label>
          <input
            type="number"
            name="shade_percent"
            value={form.shade_percent}
            onChange={handleChange}
          />
        </div>

        <button type="submit">Predict Crop Suitability</button>
      </form>
    </div>
  );
}
