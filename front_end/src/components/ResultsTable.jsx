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

  // Sort scores by confidence (descending) and pick best
  const sortedScores = uniqueScores.slice().sort((a, b) => {
    const ca = typeof a.confidence === 'number' ? a.confidence : 0;
    const cb = typeof b.confidence === 'number' ? b.confidence : 0;
    if (cb !== ca) return cb - ca;
    return (a.crop || '').localeCompare(b.crop || '');
  });
  const bestCrop = sortedScores[0] || null;
  // Confidence threshold (if you want to highlight)
  const CONFIDENCE_THRESHOLD = 74; // match backend recommendation threshold
  const isCropRecommended = bestCrop && bestCrop.confidence >= CONFIDENCE_THRESHOLD;

  const topExplanations = bestCrop?.explanation?.slice(0, 3) || [];

  return (
    <div>
      <div className="decision-banner" data-state={isCropRecommended ? "ok" : "warn"}>
        {isCropRecommended ? (
          <>
            <span className="dot" aria-hidden="true" />
            Suitable crop identified: <strong>{bestCrop.crop}</strong>
          </>
        ) : (
          <>
            <span className="dot" aria-hidden="true" />
            No crop recommended for the given environmental conditions
          </>
        )}
      </div>

      {isCropRecommended && topExplanations.length > 0 && (
        <div className="card-lite" style={{ marginBottom: 12 }}>
          <div className="card-lite-title">Why this crop</div>
          <ul className="explanation-list">
            {topExplanations.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}
      {/* ---------- Table ---------- */}
      <div className="modern-form-card" style={{ padding: 0, background: 'none', boxShadow: 'none' }}>
        <table className="modern-table">
          <thead>
            <tr>
              <th>Crop</th>
              <th>Confidence (%)</th>
            </tr>
          </thead>
          <tbody>
            {sortedScores.map((item) => (
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
                <td style={{ textAlign: 'right', paddingRight: 6 }}>{typeof item.confidence === 'number' ? Math.round(item.confidence) + '%' : item.confidence}</td>
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
