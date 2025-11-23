// src/pages/SignUp.js
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./SignUp.css";

const API_URL = "http://localhost:5000/api";

const SignUp = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState("user");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    age: "",
    description: "",
    if_online: false,
    logo: "",
    year_est: "",
    capacity: "",
    date: "",
    time: "",
    ngo_id: ""
  });

  const [ownerUserId, setOwnerUserId] = useState(""); // For NGO/Event
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const payload = { role, name: formData.name, email: formData.email };

      if (role === "user") {
        payload.password = formData.password;
        payload.age = formData.age;
      } else {
        payload.owner_user_id = ownerUserId;
        payload.password = formData.password; // only used if backend expects, can be ignored

        if (role === "ngo") {
          payload.description = formData.description;
          payload.logo = formData.logo;
          payload.year_est = formData.year_est;
        }

        if (role === "event") {
          payload.description = formData.description;
          payload.capacity = formData.capacity;
          payload.date = formData.date;
          payload.time = formData.time;
          payload.ngo_id = formData.ngo_id;
        }
      }

      const res = await axios.post(`${API_URL}/auth/register`, payload);
      setSuccess(res.data.message);
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Registration failed");
    }
  };

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>

      {/* Role Toggle */}
      <div className="role-toggle">
        <button className={role === "user" ? "active" : ""} onClick={() => setRole("user")}>User</button>
        <button className={role === "ngo" ? "active" : ""} onClick={() => setRole("ngo")}>NGO</button>
        <button className={role === "event" ? "active" : ""} onClick={() => setRole("event")}>Event</button>
      </div>

      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}

      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </label>

        <label>
          Email:
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </label>

        <label>
          Password:
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </label>

        {role === "user" && (
          <label>
            Age:
            <input type="number" name="age" value={formData.age} onChange={handleChange} />
          </label>
        )}

        {role !== "user" && (
          <label>
            Owner User ID (must be verified):
            <input type="number" value={ownerUserId} onChange={(e) => setOwnerUserId(e.target.value)} required />
          </label>
        )}

        {role === "ngo" && (
          <>
            <label>
              Description:
              <textarea name="description" value={formData.description} onChange={handleChange} />
            </label>
            <label>
              Logo URL:
              <input type="text" name="logo" value={formData.logo} onChange={handleChange} />
            </label>
            <label>
              Year Established:
              <input type="number" name="year_est" value={formData.year_est} onChange={handleChange} />
            </label>
          </>
        )}

        {role === "event" && (
          <>
            <label>
              Description:
              <textarea name="description" value={formData.description} onChange={handleChange} />
            </label>
            <label>
              Capacity:
              <input type="number" name="capacity" value={formData.capacity} onChange={handleChange} />
            </label>
            <label>
              Date:
              <input type="date" name="date" value={formData.date} onChange={handleChange} />
            </label>
            <label>
              Time:
              <input type="time" name="time" value={formData.time} onChange={handleChange} />
            </label>
            <label>
              NGO ID:
              <input type="number" name="ngo_id" value={formData.ngo_id} onChange={handleChange} />
            </label>
          </>
        )}

        <button type="submit">Sign Up</button>
      </form>

      <p>Already have an account? <a href="/login">Login here</a></p>
    </div>
  );
};

export default SignUp;
