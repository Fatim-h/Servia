import React, { useState } from 'react';
import NGOCard from '../components/NGOCard';
import NGOMap from '../components/map';
import ngos from '../demoData';

const HomePage = () => {
  const [view, setView] = useState('gallery'); // default to gallery

  const toggleView = () => {
    setView((prev) => (prev === 'gallery' ? 'map' : 'gallery'));
  };

  return (
    <div>
      <div style={{ padding: '1rem' }}>
        <button onClick={toggleView} style={{
          padding: '0.5rem 1rem',
          position: 'absolute',
          top: 10,
          left: 10,
          zIndex: 1000
        }}>
          Switch to {view === 'gallery' ? 'Map' : 'Gallery'}
        </button>
      </div>

      {view === 'gallery' ? (
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: '4rem' }}>
          {ngos.map(ngo => (
            <NGOCard key={ngo.id} ngo={ngo} />
          ))}
        </div>
      ) : (
        <div style={{ marginTop: '4rem' }}>
          <NGOMap ngos={ngos} />
        </div>
      )}
    </div>
  );
};

export default HomePage;