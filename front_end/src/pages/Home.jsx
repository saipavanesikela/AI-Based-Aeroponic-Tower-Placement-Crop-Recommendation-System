import { useState } from "react";
import InputForm from "../components/InputForm";
import ResultsTable from "../components/ResultsTable";
import PlacementView from "../components/PlacementView";
import { optimizePlacement, predictCrops } from "../services/api";

export default function Home() {
  const [result, setResult] = useState(null);
  const [resultError, setResultError] = useState(null);
  const [placement, setPlacement] = useState(null);
  const [placementError, setPlacementError] = useState(null);
  const [view, setView] = useState("predict");

  const recommendedCrop = result?.recommended_crops?.[0] || null;

  const [farm, setFarm] = useState({
    farm_length: 20,
    farm_width: 20,
    min_spacing: 2.5,
    max_towers: 15
  });

  const handleFarmChange = (e) => {
    setFarm({ ...farm, [e.target.name]: Number(e.target.value) });
  };

  const handlePlacement = async () => {
    setPlacement(null);
    setPlacementError(null);
    try {
      const data = await optimizePlacement(farm);
      setPlacement(data);
    } catch (err) {
      setPlacementError(err.message || String(err));
    }
  };

  return (
    <div className="page-shell">
      <div className="hero">
        <div className="pill">Aeroponics • Live control</div>
        <h1>Smarter tower placement</h1>
        <p>Enter your on-site conditions, get the best crop for your towers, then lay out towers with safe spacing.</p>
        <div className="hero-stats">
          <div className="stat-card">
            <div className="stat-label">Inputs</div>
            <div className="stat-value">6 factors</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Model</div>
            <div className="stat-value">RF, weighted</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Outputs</div>
            <div className="stat-value">Crop + score</div>
          </div>
        </div>
      </div>

      <div className="toggle-bar">
        <button
          className={view === "predict" ? "toggle active" : "toggle"}
          onClick={() => setView("predict")}
        >
          Predict Crop Suitability
        </button>
        <button
          className={view === "placement" ? "toggle active" : "toggle"}
          onClick={() => setView("placement")}
        >
          Tower Placement
        </button>
      </div>

      <div className="layout">
        <div className="stack">
          {view === "predict" && (
            <div className="panel">
              <h3>Environmental Inputs</h3>
              <InputForm
                onResult={async (data) => {
                  setResult(null);
                  setResultError(null);
                  setPlacement(null);
                  try {
                    const resp = await predictCrops(data);
                    setResult(resp);
                  } catch (err) {
                    setResultError(err.message || String(err));
                  }
                }}
              />
            </div>
          )}

          {view === "placement" && (
            <div className="panel">
              <h3>Farm Configuration</h3>
              <div className="form-group">
                <label>Farm Length (m)</label>
                <input
                  type="number"
                  name="farm_length"
                  value={farm.farm_length}
                  onChange={handleFarmChange}
                />
              </div>

              <div className="form-group">
                <label>Farm Width (m)</label>
                <input
                  type="number"
                  name="farm_width"
                  value={farm.farm_width}
                  onChange={handleFarmChange}
                />
              </div>

              <div className="form-group">
                <label>Minimum Tower Spacing (m)</label>
                <input
                  type="number"
                  step="0.1"
                  name="min_spacing"
                  value={farm.min_spacing}
                  onChange={handleFarmChange}
                />
              </div>

              <div className="form-group">
                <label>Maximum Towers</label>
                <input
                  type="number"
                  name="max_towers"
                  value={farm.max_towers}
                  onChange={handleFarmChange}
                />
              </div>

              <button onClick={handlePlacement}>
                Optimize Tower Placement
              </button>
            </div>
          )}
          {view === "predict" && (
            <div className="panel tips-panel">
              <h3>Quick tips</h3>
              <ul className="tips-list">
                <li>Stay inside the shown ranges to avoid hard rejections.</li>
                <li>pH 5.5–6.5 keeps most leafy greens happy.</li>
                <li>AQI above 180 sharply reduces suitability.</li>
                <li>Wind above 5 m/s is too harsh for these towers.</li>
              </ul>
            </div>
          )}
        </div>

        <div className="stack">
          {view === "predict" && recommendedCrop && (
            <div className="panel highlight-card">
              <div className="pill pill-soft">Recommended crop</div>
              <h3 style={{ marginBottom: 6 }}>{recommendedCrop}</h3>
              <p className="muted">Highest suitability for the given conditions.</p>
            </div>
          )}
          {view === "predict" && (
            <div className="panel">
              <h3>Crop Suitability Results</h3>
              <ResultsTable data={result} error={resultError} />
            </div>
          )}

          {view === "placement" && placement && (
            <div className="panel">
              <h3>Placement Output</h3>
              <PlacementView placement={placement} />
            </div>
          )}
          {view === "placement" && placementError && (
            <div className="panel">
              <h3>Placement Output</h3>
              <div className="error-msg">{placementError}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
