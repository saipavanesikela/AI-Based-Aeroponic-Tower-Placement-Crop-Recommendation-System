import React from "react";
import PropTypes from "prop-types";


export default function ResultsTable({ data, error }) {
  // Log the backend response for debugging
  console.log("[ResultsTable] Backend response:", data);

  // Show backend error if present
  if (error) {
    return <div className="error-msg" style={{ margin: '18px 0', textAlign: 'center' }}>{error}</div>;
  }
  if (data && (data.detail || data.error)) {
    const msg = data.detail || data.error;
    return <div className="error-msg" style={{ margin: '18px 0', textAlign: 'center' }}>{msg}</div>;
  }

  // Accepts 'data' prop for compatibility with Home.jsx
  const results = Array.isArray(data) ? data : (data && data.all_scores ? data.all_scores : []);
  if (!results || !Array.isArray(results) || results.length === 0) {
    return <div style={{ color: '#888', textAlign: 'center', margin: '24px 0', fontStyle: 'italic' }}>No results to display.</div>;
  }

  // Remove duplicate crops (safety)
  const uniqueScores = Array.from(
    new Map(results.map(item => [item.crop, item])).values()
  );

  // Find best crop (if any)
  const bestCrop = uniqueScores[0] || null;
  // Confidence threshold (if you want to highlight)
  const CONFIDENCE_THRESHOLD = 70;
  const isCropRecommended = bestCrop && bestCrop.confidence >= CONFIDENCE_THRESHOLD;

  return (
    <div>
      {/* ---------- Decision Message ---------- */}
      {isCropRecommended ? (
        <div
          style={{
            padding: "10px",
            marginBottom: "12px",
            backgroundColor: "#ecfdf5",
            color: "#065f46",
            borderRadius: "6px",
            fontSize: "14px"
          }}
        >
          Suitable crop identified: <strong>{bestCrop.crop}</strong>
        </div>
      ) : (
        <div
          style={{
            padding: "10px",
            marginBottom: "12px",
            backgroundColor: "#fef2f2",
            color: "#991b1b",
            borderRadius: "6px",
            fontSize: "14px"
          }}
        >
          No crop recommended for the given environmental conditions
        </div>
      )}
      {/* ---------- Table ---------- */}
      <div className="modern-form-card" style={{ padding: 0, background: 'none', boxShadow: 'none' }}>
        <table className="modern-table">
          <thead>
            <tr>
              <th>Crop</th>
              <th>Suitability Score</th>
              <th>Confidence (%)</th>
            </tr>
          </thead>
          <tbody>
            {uniqueScores.map((item) => (
              <tr
                key={item.crop}
                style={{
                  fontWeight:
                    isCropRecommended && item.crop === bestCrop.crop
                      ? "600"
                      : "normal",
                  backgroundColor:
                    isCropRecommended && item.crop === bestCrop.crop
                      ? "#f0f9ff"
                      : "transparent"
                }}
              >
                <td>{item.crop}</td>
                <td>{item.suitability_score}</td>
                <td>{item.confidence}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* ---------- Recommended Crop (ONLY IF VALID) ---------- */}
      {isCropRecommended && (
        <div style={{ marginTop: "12px" }}>
          <strong>Recommended Crop:</strong> {bestCrop.crop}
        </div>
      )}
    </div>
  );
}

ResultsTable.propTypes = {
  data: PropTypes.oneOfType([
    PropTypes.array,
    PropTypes.object
  ]),
  error: PropTypes.string
};
