import React from 'react';
import { GoogleMap, Marker, useLoadScript } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '400px'
};

// Center the map (example: Karachi)
const center = {
  lat: 24.8607,
  lng: 67.0011
};

const NGOMap = ({ ngos }) => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  if (loadError) return <div>Error loading maps</div>;
  if (!isLoaded) return <div>Loading Maps...</div>;

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={12}
    >
      {ngos.map((ngo) => (
        <Marker
          key={ngo.id}
          position={{ lat: ngo.latitude, lng: ngo.longitude }}
          title={ngo.name}
        />
      ))}
    </GoogleMap>
  );
};

export default React.memo(NGOMap);