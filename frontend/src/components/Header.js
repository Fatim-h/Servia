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
      navigate(`/admin/auth/${auth.auth_id}`); 
        break;
      default:
        break;
    }
  };

  return (
    <header className="header">
      <div className="logo">
        <Link to="/">Servia</Link>
      </div>
      <nav>
        {auth ? (
          <>
            <span className="welcome-text">Welcome, {auth.name}</span>
            <button className="header-btn" onClick={handleDashboard}>
              Dashboard
            </button>
            <button className="header-btn logout-btn" onClick={() => { logout(); navigate('/login'); }}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link className="header-btn" to="/login">Login</Link>
            <Link className="header-btn signup-btn" to="/signup">Sign Up</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
