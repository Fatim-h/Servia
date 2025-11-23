// frontend/src/components/Header.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import "./Header.css";

const Header = () => {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();

  const handleDashboard = () => {
    if (!auth) return;
    switch(auth.role) {
      case 'admin':
        navigate('/admindashboard');
        break;
      case 'user':
        navigate('/userdashboard');
        break;
      case 'cause':
        navigate('/causedashboard');
        break;
      default:
        break;
    }
  };

  return (
    <header style={{ padding: '1rem', background: '#f5f5f5', display: 'flex', justifyContent: 'space-between' }}>
      <h2><Link to="/">Servia</Link></h2>
      <div>
        {auth ? (
          <>
            <span style={{ marginRight: '1rem' }}>Welcome, {auth.name}</span>
            <button onClick={handleDashboard} style={{ marginRight: '1rem' }}>
              Dashboard
            </button>
            <button onClick={() => { logout(); navigate('/login'); }}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ marginRight: '1rem' }}>Login</Link>
            <Link to="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;