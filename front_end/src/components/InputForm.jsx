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
    spacing: 1.5,
    shade_percent: 10
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await predictCrops(form);
    onResult(result);
  };

  return (
    <div className="card">
      <h3>Environmental Inputs</h3>

      <form onSubmit={handleSubmit} className="grid-2">
        {Object.keys(form).map((key) => (
          <div className="form-group" key={key}>
            <label>{key.replace("_", " ")}</label>
            <input
              type="number"
              name={key}
              value={form[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <div style={{ gridColumn: "1 / -1" }}>
          <button type="submit">Predict Crop Suitability</button>
        </div>
      </form>
    </div>
  );
}
