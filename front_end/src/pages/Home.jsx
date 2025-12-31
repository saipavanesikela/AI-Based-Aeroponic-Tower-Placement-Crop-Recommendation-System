import { useState } from "react";
import InputForm from "../components/InputForm";
import ResultsTable from "../components/ResultsTable";
import PlacementView from "../components/PlacementView";
import { optimizePlacement } from "../services/api";

export default function Home() {
  const [result, setResult] = useState(null);
  const [placement, setPlacement] = useState(null);

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
    const data = await optimizePlacement(farm);
    setPlacement(data);
  };

  return (
    <div className="app-container">
      <h2>Aeroponic Crop Recommendation & Tower Optimization</h2>

      <InputForm onResult={setResult} />
      <ResultsTable data={result} />

      {/* Farm Configuration */}
      <div className="card">
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
          <label>Minimum Spacing (m)</label>
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

      <PlacementView placement={placement} />
    </div>
  );
}
