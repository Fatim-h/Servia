import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css'; // import the new CSS file
import { setCurrentUser } from '../services/authStore';
import api from '../services/api';

const LoginPage = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting login...");
    const success = await login({ name, password });
    const res = await api.post('/api/auth/login', { name, password });
    const logged_user = res.data;
    localStorage.setItem("logged_user", JSON.stringify(logged_user));
    console.log("Logged in user:", logged_user);
    console.log("Login result:", success);
    if (success) {
      navigate('/'); // redirect after successful login
    }
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="login-form">
        <input 
          type="text" 
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input 
          type="password" 
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      <p className="signup-text">
        Don't have an account? <a href="/signup">Sign up here</a>
      </p>
    </div>
  );
};

export default LoginPage;