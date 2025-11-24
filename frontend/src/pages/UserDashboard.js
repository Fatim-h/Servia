// src/pages/UserDashboard.js
import React, { useEffect, useState } from 'react';
import api from '../services/api'; // make sure this has withCredentials: true if needed
import './UserDashboard.css';
import Header from "../components/Header";
import { Link } from 'react-router-dom';

const UserDashboard = () => {
  const [user, setUser] = useState(null);
  const [causes, setCauses] = useState([]);
  const [donations, setDonations] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [volunteers, setVolunteers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState('info');
  const [formData, setFormData] = useState({});

  // --- Fetch dashboard data ---
  const fetchData = async () => {
    setLoading(true);
    try {
      const logged_user = JSON.parse(localStorage.getItem("logged_user"));
      if (!logged_user) throw new Error("No logged_user found in localStorage");

      const res = await api.post(
        "/api/user/dashboard/data",
        { logged_user },
        { headers: { "Content-Type": "application/json" } }
      );
      const data = res.data;

      setUser(data.user);
      setFormData(data.user);
      setCauses(data.causes || []);
      setDonations(data.donations || []);
      setFeedbacks(data.feedbacks || []);
      setVolunteers(data.volunteers || []);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
      alert("Failed to fetch dashboard data");
    } finally {
      setLoading(false);
    }
  };

  // --- Initialize user from localStorage ---
  useEffect(() => {
    const storedUser = localStorage.getItem("logged_user");
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);
      setFormData(parsedUser);
    } else {
      alert("No logged-in user found. Please log in.");
      setLoading(false);
    }
  }, []);

  // --- Fetch dashboard once user is set ---
  useEffect(() => {
    if (user?.auth_id) {
      fetchData();
    }
  }, [user]);

  if (loading) return <p>Loading...</p>;
  if (!user) return <p>User data not found</p>;

  // --- Form change handler ---
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // --- Update user ---
  const handleUpdateUser = async () => {
    try {
      await api.patch(`/api/user/${user.user_id}`, formData);
      alert('User info updated successfully');
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Failed to update user info');
    }
  };

  // --- Delete handlers ---
  const handleDeleteCause = async (id) => {
    if (!window.confirm('Are you sure you want to delete this cause?')) return;
    try {
      await api.delete(`/api/user/cause/${id}`);
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Failed to delete cause');
    }
  };

  const handleDeleteItem = async (type, id) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    try {
      await api.delete(`/api/user/${type}/${id}`);
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Failed to delete item');
    }
  };

  // --- JSX render ---
  return (
    <>
      <Header />
      <div className="user-dashboard">
        <h1>User Dashboard</h1>

        <div className="section-buttons">
          <button className={activeSection === 'info' ? 'active' : ''} onClick={() => setActiveSection('info')}>My Info</button>
          <button className={activeSection === 'causes' ? 'active' : ''} onClick={() => setActiveSection('causes')}>My Causes</button>
          <button className={activeSection === 'activity' ? 'active' : ''} onClick={() => setActiveSection('activity')}>My Activity</button>
        </div>

        {activeSection === 'info' && (
          <div className="details-section">
            <h2>My Info</h2>
            <table className="user-info-table">
              <tbody>
                <tr>
                  <td>Name:</td>
                  <td><input type="text" name="name" value={formData.name || ''} onChange={handleChange} /></td>
                </tr>
                <tr>
                  <td>Email:</td>
                  <td><input type="email" name="email" value={formData.email || ''} onChange={handleChange} /></td>
                </tr>
                <tr>
                  <td>Age:</td>
                  <td><input type="number" name="age" value={formData.age || ''} onChange={handleChange} /></td>
                </tr>
              </tbody>
            </table>
            <button className="update-btn" onClick={handleUpdateUser}>Update Info</button>
          </div>
        )}

        {activeSection === 'causes' && (
          <div className="details-section">
            <h2>My Causes</h2>
            {causes.length === 0 ? <p>No causes owned</p> :
              <table className="owned-causes-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Verified</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {causes.map(c => (
                    <tr key={c.cause_id}>
                      <td><Link to={`/cause/${c.cause_id}`}>{c.name}</Link></td>
                      <td>{c.type}</td>
                      <td>{c.verified ? 'Yes' : 'No'}</td>
                      <td>
                        <button className="btn btn-delete" onClick={() => handleDeleteCause(c.cause_id)}>Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            }
          </div>
        )}

        {activeSection === 'activity' && (
          <div className="details-section">
            <h2>My Donations</h2>
            {donations.length === 0 ? <p>No donations</p> :
              <table className="activity-table">
                <thead>
                  <tr>
                    <th>Cause</th>
                    <th>Amount</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {donations.map(d => (
                    <tr key={d.donation_id}>
                      <td><Link to={`/cause/${d.cause_id}`}>{d.cause_name}</Link></td>
                      <td>{d.amount}</td>
                      <td>{d.date}</td>
                      <td><button className="btn btn-delete" onClick={() => handleDeleteItem('donation', d.donation_id)}>Delete</button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            }

            <h2>My Feedbacks</h2>
            {feedbacks.length === 0 ? <p>No feedbacks</p> :
              <table className="activity-table">
                <thead>
                  <tr>
                    <th>Cause</th>
                    <th>Feedback</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {feedbacks.map(f => (
                    <tr key={f.feedback_id}>
                      <td><Link to={`/cause/${f.cause_id}`}>{f.cause_name}</Link></td>
                      <td>{f.comment || f.message}</td>
                      <td>{f.date}</td>
                      <td><button className="btn btn-delete" onClick={() => handleDeleteItem('feedback', f.feedback_id)}>Delete</button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            }

            <h2>My Volunteer Activities</h2>
            {volunteers.length === 0 ? <p>No volunteer activities</p> :
              <table className="activity-table">
                <thead>
                  <tr>
                    <th>Cause</th>
                    <th>Hours</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {volunteers.map(v => (
                    <tr key={v.volunteer_id}>
                      <td><Link to={`/cause/${v.cause_id}`}>{v.cause_name}</Link></td>
                      <td>{v.hours}</td>
                      <td>{v.date}</td>
                      <td><button className="btn btn-delete" onClick={() => handleDeleteItem('volunteer', v.volunteer_id)}>Delete</button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            }
          </div>
        )}
      </div>
    </>
  );
};

export default UserDashboard;