// src/pages/HomePage.js
import React, { useState, useEffect } from 'react';
import CauseCard from '../components/CauseCard';
import CauseMap from '../components/Causemap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getAllCauses } from '../services/causeservice';

const HomePage = () => {
  const [view, setView] = useState('gallery'); // gallery or map
  const [causes, setCauses] = useState([]);
  const navigate = useNavigate();
  const { user, logout } = useAuth();  // using global login state

  // Fetch causes from backend
  useEffect(() => {
    const fetchCauses = async () => {
      const data = await getAllCauses();
      setCauses(data);
    };
    fetchCauses();
  }, []);

  const toggleView = () => {
    setView(prev => (prev === 'gallery' ? 'map' : 'gallery'));
  };

  const goToLogin = () => {
    navigate("/login");
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div>
      {/* HEADER */}
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
        <button onClick={toggleView} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
          Switch to {view === 'gallery' ? 'Map' : 'Gallery'}
        </button>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          {!user && (
            <button onClick={goToLogin} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
              Login
            </button>
          )}

          {user && (
            <>
              <span>Welcome, {user.name}</span>
              <button 
                onClick={() => navigate(`/${user.role}-dashboard`)}
                style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}
              >
                Dashboard
              </button>
              <button onClick={handleLogout} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
                Logout
              </button>
            </>
          )}
        </div>
      </header>

      {/* CONTENT */}
      {view === 'gallery' ? (
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', marginTop: '2rem' }}>
          {causes.map(cause => (
            <CauseCard key={cause.id} cause={cause} />
          ))}
        </div>
      ) : (
        <div style={{ marginTop: '2rem' }}>
          <CauseMap causes={causes} />
        </div>
      )}
    </div>
  );
};

export default HomePage;