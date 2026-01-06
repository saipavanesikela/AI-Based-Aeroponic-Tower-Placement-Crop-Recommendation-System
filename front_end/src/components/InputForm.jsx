
import { useState } from "react";
import { fetchEnvironment, fetchEnvironmentByCoords } from "../services/api";
import MapSelector from "./MapSelector";


const initialForm = {
  temperature: "",
  humidity: "",
  wind_speed: "",
  sunlight_hours: "",
  x_coord: "",
  y_coord: "",
  spacing: "",
  shade_percent: ""
};

export default function InputForm({ onResult }) {
  const [city, setCity] = useState("");
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
    if (fields.wind_speed === "" || isNaN(Number(fields.wind_speed)) || Number(fields.wind_speed) < 0 || Number(fields.wind_speed) > 10) {
      newErrors.wind_speed = "Wind speed must be 0-10 m/s";
    }
    if (fields.sunlight_hours === "" || isNaN(Number(fields.sunlight_hours)) || Number(fields.sunlight_hours) < 0 || Number(fields.sunlight_hours) > 24) {
      newErrors.sunlight_hours = "Sunlight hours must be 0-24";
    }
    if (fields.x_coord === "" || isNaN(Number(fields.x_coord)) || Number(fields.x_coord) < 0) {
      newErrors.x_coord = "X coordinate must be ≥ 0";
    }
    if (fields.y_coord === "" || isNaN(Number(fields.y_coord)) || Number(fields.y_coord) < 0) {
      newErrors.y_coord = "Y coordinate must be ≥ 0";
    }
    if (fields.spacing === "" || isNaN(Number(fields.spacing)) || Number(fields.spacing) < 0.5 || Number(fields.spacing) > 5.0) {
      newErrors.spacing = "Spacing must be 0.5-5.0 m";
    }
    if (fields.shade_percent === "" || isNaN(Number(fields.shade_percent)) || Number(fields.shade_percent) < 0 || Number(fields.shade_percent) > 100) {
      newErrors.shade_percent = "Shade percent must be 0-100";
    }
    return newErrors;
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value === undefined || e.target.value === null ? "" : e.target.value });
    setErrors({ ...errors, [e.target.name]: undefined });
    setSuccessMsg("");
  };

  const handleFetchByCity = async () => {
    setSuccessMsg("");
    if (!city) {
      setErrors({ city: "Please enter a city name" });
      return;
    }
    setLoading(true);
    try {
      const data = await fetchEnvironment(city);
      setForm({
        temperature: data.temperature,
        humidity: data.humidity,
        sunlight_hours: 6
      });
      setErrors({});
      setSuccessMsg("Environment loaded for " + city);
    } catch {
      setErrors({ city: "City not found" });
    }
    setLoading(false);
  };

  const handleFetchByCoords = async (lat, lon) => {
    setSuccessMsg("");
    setLoading(true);
    try {
      const data = await fetchEnvironmentByCoords(lat, lon);
      setForm({
        temperature: data.temperature,
        humidity: data.humidity,
        sunlight_hours: 6
      });
      setErrors({});
      setSuccessMsg("Environment loaded for selected location");
    } catch {
      setErrors({ city: "Unable to fetch environment for this location" });
    }
    setLoading(false);
  };

  const handleCurrentLocation = () => {
    setSuccessMsg("");
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        handleFetchByCoords(pos.coords.latitude, pos.coords.longitude);
      },
      () => {
        setErrors({ city: "Location permission denied" });
        setLoading(false);
      }
    );
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
      wind_speed: Number(form.wind_speed),
      sunlight_hours: Number(form.sunlight_hours),
      x_coord: Number(form.x_coord),
      y_coord: Number(form.y_coord),
      spacing: Number(form.spacing),
      shade_percent: Number(form.shade_percent)
    });
  };

  return (
    <div className="modern-form-card">
      <div className="form-title">Get Environment Data</div>
      <div className="form-group">
        <label>City</label>
        <input
          type="text"
          value={city}
          onChange={(e) => { setCity(e.target.value); setErrors({ ...errors, city: undefined }); setSuccessMsg(""); }}
          placeholder="e.g., Bengaluru"
          disabled={loading}
          className={errors.city ? "input-error" : ""}
        />
        {errors.city && <div className="error-msg">{errors.city}</div>}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <button type="button" onClick={handleFetchByCity} disabled={loading} style={{ flex: 1 }}>
          {loading ? "Loading..." : "Fetch by City"}
        </button>
        <button type="button" onClick={handleCurrentLocation} disabled={loading} style={{ flex: 1 }}>
          Use My Location
        </button>
      </div>
      <div style={{ margin: "14px 0" }}>
        <MapSelector onLocationSelect={(pos) => handleFetchByCoords(pos.lat, pos.lng)} />
      </div>

      <div className="form-title" style={{ marginTop: 18 }}>Enter Crop Prediction Details</div>
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
        {errors.humidity && <div className="error-msg">{errors.humidity}</div>}
      </div>
      <div className="form-group">
        <label>Wind Speed (m/s)</label>
        <input
          type="number"
          name="wind_speed"
          value={form.wind_speed ?? ""}
          onChange={handleChange}
          min={0}
          max={10}
          step={0.1}
          className={errors.wind_speed ? "input-error" : ""}
          disabled={loading}
        />
        {errors.wind_speed && <div className="error-msg">{errors.wind_speed}</div>}
      </div>
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
        {errors.sunlight_hours && <div className="error-msg">{errors.sunlight_hours}</div>}
      </div>
      <div className="form-group">
        <label>X Coordinate</label>
        <input
          type="number"
          name="x_coord"
          value={form.x_coord ?? ""}
          onChange={handleChange}
          min={0}
          step={1}
          className={errors.x_coord ? "input-error" : ""}
          disabled={loading}
        />
        {errors.x_coord && <div className="error-msg">{errors.x_coord}</div>}
      </div>
      <div className="form-group">
        <label>Y Coordinate</label>
        <input
          type="number"
          name="y_coord"
          value={form.y_coord ?? ""}
          onChange={handleChange}
          min={0}
          step={1}
          className={errors.y_coord ? "input-error" : ""}
          disabled={loading}
        />
        {errors.y_coord && <div className="error-msg">{errors.y_coord}</div>}
      </div>
      <div className="form-group">
        <label>Spacing (m)</label>
        <input
          type="number"
          name="spacing"
          value={form.spacing ?? ""}
          onChange={handleChange}
          min={0.5}
          max={5.0}
          step={0.1}
          className={errors.spacing ? "input-error" : ""}
          disabled={loading}
        />
        {errors.spacing && <div className="error-msg">{errors.spacing}</div>}
      </div>
      <div className="form-group">
        <label>Shade Percent (%)</label>
        <input
          type="number"
          name="shade_percent"
          value={form.shade_percent ?? ""}
          onChange={handleChange}
          min={0}
          max={100}
          step={0.1}
          className={errors.shade_percent ? "input-error" : ""}
          disabled={loading}
        />
        {errors.shade_percent && <div className="error-msg">{errors.shade_percent}</div>}
      </div>
      <button type="button" onClick={handlePredict} disabled={loading} style={{ marginTop: 10, fontWeight: 600, fontSize: 16 }}>
        Predict Crop Suitability
      </button>
      {successMsg && <div className="success-msg">{successMsg}</div>}
    </div>
  );
}
