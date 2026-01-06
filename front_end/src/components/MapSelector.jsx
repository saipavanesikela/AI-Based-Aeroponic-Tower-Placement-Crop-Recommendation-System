import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";

function LocationMarker({ onSelect }) {
  const [position, setPosition] = useState(null);

  useMapEvents({
    click(e) {
      setPosition(e.latlng);
      onSelect(e.latlng);
    }
  });

  return position ? <Marker position={position} /> : null;
}

// MapSelector is now a placeholder component (no map/location selection)
import React from "react";

export default function MapSelector() {
  return null;
}
