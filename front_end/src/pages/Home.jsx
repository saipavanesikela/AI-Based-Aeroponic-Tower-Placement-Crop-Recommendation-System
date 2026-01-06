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
    <div className="app-container">

      {/* ---------- Header ---------- */}
      <div className="app-header">
        <h1>Aeroponic Optimization System</h1>
        <p>
          AI-based crop suitability analysis and tower placement optimization
        </p>
      </div>

      {/* ---------- Main Layout ---------- */}
      <div className="main-layout">

        {/* ---------- Left Panel ---------- */}
        <div>
          <div className="panel">
            <h3>Environmental Inputs</h3>
            <InputForm
              onResult={async (data) => {
                setResult(null);
                setResultError(null);
                setPlacement(null); // clear placement when predicting
                try {
                  const resp = await predictCrops(data);
                  setResult(resp);
                } catch (err) {
                  setResultError(err.message || String(err));
                }
              }}
            />
          </div>

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
        </div>

        {/* ---------- Right Panel ---------- */}
        <div>
          {result && (
            <div className="panel">
              <h3>Crop Suitability Results</h3>
              <ResultsTable data={result} />
            </div>
          )}

          {resultError && (
            <div className="panel">
              <h3>Crop Suitability Results</h3>
              <ResultsTable data={null} error={resultError} />
            </div>
          )}

          {placement && (
            <div className="panel">
              <h3>Placement Output</h3>
              <PlacementView placement={placement} />
            </div>
          )}
          {placementError && (
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
