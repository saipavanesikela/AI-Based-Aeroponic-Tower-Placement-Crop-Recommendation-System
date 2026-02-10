import React from "react";
import PropTypes from "prop-types";

export default function PlacementView({ placement, error }) {
  if (error) {
    return <div className="error-msg" style={{ margin: '18px 0', textAlign: 'center' }}>{error}</div>;
  }
  if (!placement) {
    return <div style={{ color: '#888', textAlign: 'center', margin: '24px 0', fontStyle: 'italic' }}>No placement data to display.</div>;
  }

  // Prefer image_url from backend; if not present, attempt to derive from image_file
  const API_BASE = "http://127.0.0.1:8000";
  let imageUrl = null;
  if (placement.image_url) imageUrl = placement.image_url.startsWith("http") ? placement.image_url : API_BASE + placement.image_url;
  else if (placement.image_file) {
    const filename = placement.image_file.split(/[\\/]/).pop();
    imageUrl = `${API_BASE}/static/${filename}`;
  }

  if (!imageUrl) {
    return <div style={{ color: '#888', textAlign: 'center', margin: '24px 0', fontStyle: 'italic' }}>No placement image to display.</div>;
  }

  return (
    <div className="modern-form-card" style={{ padding: 0, background: 'none', boxShadow: 'none' }}>
      <div style={{ textAlign: 'center', margin: '18px 0' }}>
        <img src={imageUrl} alt="Optimized Tower Placement" style={{ maxWidth: '100%', borderRadius: 10, boxShadow: '0 2px 12px rgba(0,0,0,0.10)' }} />
        <div style={{ marginTop: 10 }}>
          <strong>Total Towers Placed:</strong> {placement.total_towers}
        </div>
      </div>
    </div>
  );
}

PlacementView.propTypes = {
  placement: PropTypes.object,
  error: PropTypes.string
};
