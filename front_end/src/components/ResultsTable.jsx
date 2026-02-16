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
  // If backend returns an object, prefer `all_scores` and `recommended_crops`.
  const results = Array.isArray(data) ? data : (data && data.all_scores ? data.all_scores : []);
  const backendRecommended = data && data.recommended_crops ? data.recommended_crops : [];
  if (!results || !Array.isArray(results) || results.length === 0) {
    return <div style={{ color: '#888', textAlign: 'center', margin: '24px 0', fontStyle: 'italic' }}>No results to display.</div>;
  }

  // Remove duplicate crops (safety)
  const uniqueScores = Array.from(
    new Map(results.map(item => [item.crop, item])).values()
  );

  // Find best crop by confidence (primary) then suitability_score (tie-breaker)
  const bestCrop = uniqueScores
    .slice()
    .sort((a, b) => {
      if ((b.confidence || 0) !== (a.confidence || 0)) return (b.confidence || 0) - (a.confidence || 0);
      return (b.suitability_score || 0) - (a.suitability_score || 0);
    })[0] || null;
  const recommendedFromBackend = backendRecommended && backendRecommended.length > 0 ? backendRecommended[0] : null;
  const displayedCropName = recommendedFromBackend || (bestCrop && bestCrop.crop) || null;
  const displayedCropEntry = uniqueScores.find((it) => it.crop === displayedCropName) || bestCrop || null;
  // Confidence threshold (if you want to highlight)
  const CONFIDENCE_THRESHOLD = 74; // match backend recommendation threshold

  // Consider backend `recommended_crops` first to avoid contradictory UI.
  const isCropRecommended = Boolean(
    (backendRecommended && backendRecommended.length > 0) ||
    (bestCrop && bestCrop.confidence >= CONFIDENCE_THRESHOLD)
  );

  const topExplanations = bestCrop?.explanation?.slice(0, 3) || [];

  return (
    <div>
      <div className="decision-banner" data-state={isCropRecommended ? "ok" : "warn"}>
        {isCropRecommended ? (
          <>
            <span className="dot" aria-hidden="true" />
            Recommended crop: <strong>{displayedCropEntry ? displayedCropEntry.crop : (bestCrop && bestCrop.crop)}</strong>
          </>
        ) : (
            <>
              <span className="dot" aria-hidden="true" />
              No crop recommended for the given environmental conditions
            </>
        )}
      </div>

      {isCropRecommended && (displayedCropEntry?.explanation || []).slice(0,3).length > 0 && (
        <div className="card-lite" style={{ marginBottom: 12 }}>
          <div className="card-lite-title">Why this crop</div>
          <ul className="explanation-list">
            {(displayedCropEntry?.explanation || []).slice(0,3).map((item, idx) => (
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
            {uniqueScores.map((item) => (
              <tr
                key={item.crop}
                style={{
                  fontWeight:
                    isCropRecommended && item.crop === (displayedCropEntry ? displayedCropEntry.crop : bestCrop?.crop)
                      ? "600"
                      : "normal",
                  backgroundColor:
                    isCropRecommended && item.crop === bestCrop.crop
                      ? "#f0f9ff"
                      : "transparent"
                }}
              >
                <td>{item.crop}</td>
                  <td>{item.confidence}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* ---------- Recommended Crop (ONLY IF VALID) ---------- */}
      {isCropRecommended && displayedCropEntry && (
        <div style={{ marginTop: "12px" }}>
          <strong>Recommended Crop:</strong> {displayedCropEntry.crop}
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
