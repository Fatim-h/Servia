// src/pages/UserDashboard.js
import React, { useEffect, useState } from 'react';
import api from '../services/api';
import './UserDashboard.css';
import Header from "../components/Header"
import { Link } from 'react-router-dom';

const UserDashboard = () => {
  const [user, setUser] = useState(null);
  const [causes, setCauses] = useState([]);
  const [donations, setDonations] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [volunteers, setVolunteers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState('info'); // info / causes / activity
  const [formData, setFormData] = useState({});

  // Fetch user and related data
  const fetchData = async () => {
    try {
      const resUser = await api.get('/api/auth/user'); // current logged in user
      setUser(resUser.data);
      setFormData(resUser.data); // populate form data

      const resCauses = await api.get(`/api/user/${resUser.data.id}/causes`);
      setCauses(resCauses.data.causes);

      const resDonations = await api.get(`/api/user/${resUser.data.id}/donations`);
      setDonations(resDonations.data.donations);

      const resFeedbacks = await api.get(`/api/user/${resUser.data.id}/feedbacks`);
      setFeedbacks(resFeedbacks.data.feedbacks);

      const resVolunteers = await api.get(`/api/user/${resUser.data.id}/volunteers`);
      setVolunteers(resVolunteers.data.volunteers);

      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (!user) return <p>User data not found</p>;

  // Handle form changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Update user info
  const handleUpdateUser = async () => {
    try {
      await api.patch(`/api/user/${user.id}`, formData);
      alert('User info updated successfully');
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Failed to update user info');
    }
  };

  // Delete cause
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

  // Delete donation/feedback/volunteer
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

  return (
    <><Header />
    <div className="user-dashboard">
      <h1>User Dashboard</h1>

      {/* Section toggle buttons */}
      <div className="section-buttons">
        <button
          className={activeSection === 'info' ? 'active' : ''}
          onClick={() => setActiveSection('info')}
        >
          My Info
        </button>
        <button
          className={activeSection === 'causes' ? 'active' : ''}
          onClick={() => setActiveSection('causes')}
        >
          My Causes
        </button>
        <button
          className={activeSection === 'activity' ? 'active' : ''}
          onClick={() => setActiveSection('activity')}
        >
          My Activity
        </button>
      </div>

      {/* USER INFO SECTION */}
      {activeSection === 'info' && (
        <div className="details-section">
          <h2>My Info</h2>
          <table className="user-info-table">
            <tbody>
              <tr>
                <td>Name:</td>
                <td>
                  <input
                    type="text"
                    name="name"
                    value={formData.name || ''}
                    onChange={handleChange}
                  />
                </td>
              </tr>
              <tr>
                <td>Email:</td>
                <td>
                  <input
                    type="email"
                    name="email"
                    value={formData.email || ''}
                    onChange={handleChange}
                  />
                </td>
              </tr>
              <tr>
                <td>Age:</td>
                <td>
                  <input
                    type="number"
                    name="age"
                    value={formData.age || ''}
                    onChange={handleChange}
                  />
                </td>
              </tr>
            </tbody>
          </table>
          <button className="update-btn" onClick={handleUpdateUser}>
            Update Info
          </button>
        </div>
      )}

      {/* USER CAUSES SECTION */}
      {activeSection === 'causes' && (
        <div className="details-section">
          <h2>My Causes</h2>
          {causes.length === 0 ? (
            <p>No causes owned</p>
          ) : (
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
                {causes.map((c) => (
                  <tr key={c.cause_id}>
                    <td>
                      <Link to={`/cause/${c.cause_id}`}>{c.name}</Link>
                    </td>
                    <td>{c.type}</td>
                    <td>{c.verified ? 'Yes' : 'No'}</td>
                    <td>
                      <button
                        className="btn btn-delete"
                        onClick={() => handleDeleteCause(c.cause_id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* USER ACTIVITY SECTION */}
      {activeSection === 'activity' && (
        <div className="details-section">
          <h2>My Donations</h2>
          {donations.length === 0 ? (
            <p>No donations</p>
          ) : (
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
                {donations.map((d) => (
                  <tr key={d.id}>
                    <td>{d.cause_name}</td>
                    <td>{d.amount}</td>
                    <td>{d.date}</td>
                    <td>
                      <button
                        className="btn btn-delete"
                        onClick={() => handleDeleteItem('donation', d.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          <h2>My Feedbacks</h2>
          {feedbacks.length === 0 ? (
            <p>No feedbacks</p>
          ) : (
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
                {feedbacks.map((f) => (
                  <tr key={f.id}>
                    <td>{f.cause_name}</td>
                    <td>{f.feedback}</td>
                    <td>{f.date}</td>
                    <td>
                      <button
                        className="btn btn-delete"
                        onClick={() => handleDeleteItem('feedback', f.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          <h2>My Volunteer Activities</h2>
          {volunteers.length === 0 ? (
            <p>No volunteer activities</p>
          ) : (
            <table className="activity-table">
              <thead>
                <tr>
                  <th>Cause</th>
                  <th>Role</th>
                  <th>Date</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {volunteers.map((v) => (
                  <tr key={v.id}>
                    <td>{v.cause_name}</td>
                    <td>{v.role}</td>
                    <td>{v.date}</td>
                    <td>
                      <button
                        className="btn btn-delete"
                        onClick={() => handleDeleteItem('volunteer', v.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  </>);
};

export default UserDashboard;