import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [causes, setCauses] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch logged-in user
  const fetchCurrentUser = async () => {
    try {
      const res = await api.get('/api/auth/user');
      setCurrentUser(res.data);
    } catch (err) {
      console.warn('Not logged in or session expired');
      navigate('/login');
    }
  };

  // Fetch users for admin
  const fetchUsers = async () => {
    try {
      const res = await api.get('/api/admin/users');
      setUsers(res.data);
    } catch (err) {
      console.error('Failed to load users:', err.response || err);
      alert('Failed to load users');
    }
  };

  // Fetch causes for admin
  const fetchCauses = async () => {
    try {
      const res = await api.get('/api/admin/causes');
      setCauses(res.data);
    } catch (err) {
      console.error('Failed to load causes:', err.response || err);
      alert('Failed to load causes');
    }
  };

  // Toggle user verification
  const toggleVerifyUser = async (auth_id, verified) => {
    if (!auth_id) return;
    try {
      await api.patch(`/api/admin/${verified ? 'unverify' : 'verify'}/${auth_id}`);
      await fetchUsers();
      await fetchCauses(); // Also update causes of this user
    } catch (err) {
      console.error(err);
      alert('Failed to update user verification');
    }
  };

  // Delete a user
  const handleDeleteUser = async (user_id) => {
    if (!user_id) return;
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      await api.delete(`/api/admin/delete/user/${user_id}`);
      await fetchUsers();
      await fetchCauses();
    } catch (err) {
      console.error(err);
      alert('Failed to delete user');
    }
  };

  // Toggle cause verification
  const toggleVerifyCause = async (auth_id, verified) => {
    if (!auth_id) return;
    try {
      await api.patch(`/api/admin/${verified ? 'unverify' : 'verify'}/${auth_id}`);
      await fetchCauses();
    } catch (err) {
      console.error(err);
      alert('Failed to update cause verification');
    }
  };

  // Delete a cause
  const handleDeleteCause = async (cause_id) => {
    if (!cause_id) return;
    if (!window.confirm('Are you sure you want to delete this cause?')) return;
    try {
      await api.delete(`/api/admin/delete/cause/${cause_id}`);
      await fetchCauses();
    } catch (err) {
      console.error(err);
      alert('Failed to delete cause');
    }
  };

  useEffect(() => {
    const init = async () => {
      await fetchCurrentUser();
      await fetchUsers();
      await fetchCauses();
      setLoading(false);
    };
    init();
  }, []);

  if (loading) return <p>Loading...</p>;

  if (!currentUser || currentUser.role !== 'admin') {
    return <p>Access denied. Admins only.</p>;
  }

  return (
    <div className="admin-container">
      <h1>Admin Dashboard</h1>

      {/* Users Section */}
      <h2>Users</h2>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Verified</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u, index) => (
            <tr key={u.auth_id || `user-${index}`}>
              <td>
                <Link to={`/admin/user/${u.user_id}`}>{u.name}</Link>
              </td>
              <td>{u.verified ? 'Yes' : 'No'}</td>
              <td>
                <button
                  className="btn"
                  onClick={() => toggleVerifyUser(u.auth_id, u.verified)}
                >
                  {u.verified ? 'Unverify' : 'Verify'}
                </button>
                <button className="btn btn-delete" onClick={() => handleDeleteUser(u.user_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Causes Section */}
      <h2>Causes</h2>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Verified</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {causes.map((c, index) => (
            <tr key={c.cause_id || `cause-${index}`}>
              <td>
                <Link to={`/cause/${c.cause_id}`}>{c.name}</Link>
              </td>
              <td>{c.verified ? 'Yes' : 'No'}</td>
              <td>
                {c.verified ? (
                    <span style={{color: "green"}}>Verified</span>
                  ) : (
                    <span style={{color: "red"}}>Unverified</span>
                  )}

                <button className="btn btn-delete" onClick={() => handleDeleteCause(c.cause_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;