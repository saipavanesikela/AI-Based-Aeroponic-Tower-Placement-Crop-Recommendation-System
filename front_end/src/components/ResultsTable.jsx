export default function ResultsTable({ data }) {
  if (!data || data.all_scores?.length === 0) return null;

  // Determine if the recommended crop can be grown (score > 0)
  let growMessage = null;
  if (data.recommended_crops && data.recommended_crops.length > 0) {
    const best = data.all_scores.find(
      (item) => item.crop === data.recommended_crops[0]
    );
    if (best) {
      growMessage = best.suitability_score > 0
        ? `You can grow ${best.crop} in these conditions.`
        : `You cannot grow any crop in these conditions.`;
    }
  }

  return (
    <div className="card premium-card world-class-hero">
      <div className="hero-image-container">
        <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80" alt="Nature Hero" className="hero-image" />
        <div className="hero-title">
          <span role="img" aria-label="leaf" style={{fontSize: '2.5rem', marginRight: '10px'}}>🌱</span>
          <span className="premium-title">Crop Suitability</span>
          <span role="img" aria-label="sun" style={{fontSize: '2.5rem', marginLeft: '10px'}}>🌞</span>
        </div>
      </div>

      <table className="premium-table">
        <thead>
          <tr>
            <th>Crop</th>
            <th>Score</th>
            <th>Confidence (%)</th>
          </tr>
        </thead>
        <tbody>
          {(() => {
            if (data.recommended_crops && data.recommended_crops.length > 0) {
              const best = data.all_scores.find(
                (item) => item.crop === data.recommended_crops[0]
              );
              return best ? (
                <tr className="premium-row premium-row-highlight">
                  <td className="premium-cell">{best.crop} <span role="img" aria-label="plant">🌿</span></td>
                  <td className="premium-cell">{best.suitability_score} <span role="img" aria-label="star">⭐</span></td>
                  <td className="premium-cell">{best.confidence} <span role="img" aria-label="rocket">🚀</span></td>
                </tr>
              ) : null;
            } else {
              return data.all_scores.slice(0, 5).map((item, index) => (
                <tr className="premium-row" key={index}>
                  <td className="premium-cell">{item.crop} <span role="img" aria-label="plant">🌿</span></td>
                  <td className="premium-cell">{item.suitability_score} <span role="img" aria-label="star">⭐</span></td>
                  <td className="premium-cell">{item.confidence} <span role="img" aria-label="rocket">🚀</span></td>
                </tr>
              ));
            }
          })()}
        </tbody>
      </table>

      {growMessage && (
        <div className={growMessage.includes('cannot') ? 'premium-message error' : 'premium-message success'}>
          {growMessage} {growMessage.includes('cannot') ? '😞' : '🎉'}
        </div>
      )}

      <h4 className="premium-subtitle">Recommended Crop</h4>
      <div className="premium-badges">
        {data.recommended_crops.map((crop, idx) => (
          <span className="premium-badge" key={idx}>
            {crop} <span role="img" aria-label="trophy">🏆</span>
          </span>
        ))}
      </div>
    </div>
  );
}
