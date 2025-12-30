export default function ResultsTable({ data }) {
  if (!data || data.all_scores?.length === 0) return null;

  return (
    <div className="card">
      <h3>Crop Suitability Scores</h3>

      <table>
        <thead>
          <tr>
            <th>Crop</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {data.all_scores.map((item, index) => (
            <tr key={index}>
              <td>{item.crop}</td>
              <td>{item.suitability_score}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h4 style={{ marginTop: "15px" }}>Recommended Crops</h4>
      {data.recommended_crops.map((crop, idx) => (
        <span className="badge" key={idx}>{crop}</span>
      ))}
    </div>
  );
}
