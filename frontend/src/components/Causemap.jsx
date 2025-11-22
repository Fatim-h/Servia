// src/components/CauseMap.js
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const CauseMap = ({ causes }) => {
  return (
    <MapContainer center={[0, 0]} zoom={2} style={{ height: '600px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {causes.map(cause =>
        cause.locations?.map((loc, idx) => (
          <Marker key={`${cause.id}-${idx}`} position={[loc.latitude, loc.longitude]}>
            <Popup>
              <strong>{cause.name}</strong><br />
              {cause.type.toUpperCase()}<br />
              {cause.description}
            </Popup>
          </Marker>
        ))
      )}
    </MapContainer>
  );
};

export default CauseMap;