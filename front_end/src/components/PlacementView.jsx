export default function PlacementView({ placement }) {
  if (!placement) return null;

  const imageUrl =
    "http://127.0.0.1:8000/static/optimized_tower_layout.png?t=" +
    new Date().getTime();

  return (
    <div className="card">
      <h3>Optimized Tower Placement</h3>

      <p><strong>Total Towers:</strong> {placement.total_towers}</p>

      <img
        src={imageUrl}
        alt="Tower Placement"
        className="placement-image"
      />

      <h4 style={{ marginTop: "15px" }}>Tower Coordinates</h4>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>X (m)</th>
            <th>Y (m)</th>
          </tr>
        </thead>
        <tbody>
          {placement.tower_positions.map((pos, i) => (
            <tr key={i}>
              <td>{i + 1}</td>
              <td>{pos[0].toFixed(2)}</td>
              <td>{pos[1].toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
