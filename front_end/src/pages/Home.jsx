import { useState } from "react";
import InputForm from "../components/InputForm";
import ResultsTable from "../components/ResultsTable";
import PlacementView from "../components/PlacementView";
import { optimizePlacement } from "../services/api";

export default function Home() {
  const [result, setResult] = useState(null);
  const [placement, setPlacement] = useState(null);

  const handlePlacement = async () => {
    const data = await optimizePlacement();
    setPlacement(data);
  };

  return (
    <div className="app-container">
      <h2>Aeroponic Crop Recommendation & Tower Optimization</h2>

      <InputForm onResult={setResult} />
      <ResultsTable data={result} />

      <div className="card">
        <button onClick={handlePlacement}>Optimize Tower Placement</button>
      </div>

      <PlacementView placement={placement} />
    </div>
  );
}
