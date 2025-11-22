import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [name, setName] = useState('');
  const [id, setId] = useState('');
  const [role, setRole] = useState('user');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    login({
      name,
      id,
      role,
    });

    navigate('/');
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Login</h1>

      <form onSubmit={handleSubmit} style={{ maxWidth: "400px" }}>
        
        <input 
          type="text" 
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ width: "100%", marginBottom: "1rem" }}
        />

        <input 
          type="password"
          placeholder="ID / Password"
          value={id}
          onChange={(e) => setId(e.target.value)}
          style={{ width: "100%", marginBottom: "1rem" }}
        />

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{ width: "100%", marginBottom: "1rem" }}
        >
          <option value="admin">Admin</option>
          <option value="user">User</option>
          <option value="cause">Cause</option>
        </select>

        <button type="submit" style={{ width: "100%", padding: "0.5rem" }}>
          Login
        </button>
      </form>

      <p>
          Don't have an account? <a href="/signup">Sign up here</a>
      </p>
    </div>
  );
};

export default LoginPage;