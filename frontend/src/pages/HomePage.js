import React, { useState } from 'react';
import NGOCard from '../components/NGOCard';
import NGOMap from '../components/map';
import ngos from '../demoData';

const HomePage = () => {
  const [view, setView] = useState('gallery');       // gallery or map
  const [isLoggedIn, setIsLoggedIn] = useState(false); // login state

  const toggleView = () => {
    setView((prev) => (prev === 'gallery' ? 'map' : 'gallery'));
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <div>

      {/* HEADER BAR */}
      <header style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '1rem 2rem',
        background: '#f5f5f5',
        borderBottom: '1px solid #ddd',
        position: 'sticky',
        top: 0,
        zIndex: 1000
      }}>
        
        {/* Left side: Switch View Button */}
        <button 
          onClick={toggleView}
          style={{
            padding: '0.5rem 1rem',
            cursor: 'pointer'
          }}
        >
          Switch to {view === 'gallery' ? 'Map' : 'Gallery'}
        </button>

        {/* Right side: Conditional Login / Logout */}
        <div style={{ display: 'flex', gap: '1rem' }}>
          {!isLoggedIn && (
            <button 
              onClick={handleLogin} 
              style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
            >
              Login
            </button>
          )}

          {isLoggedIn && (
            <button 
              onClick={handleLogout} 
              style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
            >
              Logout
            </button>
          )}
        </div>
      </header>

      {/* CONTENT */}
      {view === 'gallery' ? (
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: '2rem' }}>
          {ngos.map(ngo => (
            <NGOCard key={ngo.id} ngo={ngo} />
          ))}
        </div>
      ) : (
        <div style={{ marginTop: '2rem' }}>
          <NGOMap ngos={ngos} />
        </div>
      )}

    </div>
  );
};

export default HomePage;