import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const { auth } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch users
  const fetchUsers = async () => {
    try {
      const res = await api.get('/api/admin/users', {
        headers: { Authorization: `Bearer ${auth.token}` }
      });
      setUsers(res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      alert('Failed to load users');
    }
  };

  useEffect(() => {
    if (!auth || auth.role !== 'admin') {
      navigate('/login');
    } else {
      fetchUsers();
    }
  }, [auth]);

 // Verify/unverify user
   const toggleVerify = async (authId, verified) => {
     try {
       const route = verified 
         ? `/api/admin/unverify/${authId}` 
         : `/api/admin/verify/${authId}`;
   
       await api.patch(route, {}, {
         headers: { Authorization: `Bearer ${auth.token}` }
       });
   
       fetchUsers(); // refresh list
     } catch (err) {
       console.error(err);
       alert('Failed to update user verification');
     }
   };
   

  // Delete user
  const handleDelete = async (authId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;

    try {
      await api.delete(`/api/admin/delete/user/${authId}`, {
        headers: { Authorization: `Bearer ${auth.token}` }
      });
      fetchUsers();
    } catch (err) {
      console.error(err);
      alert('Failed to delete user');
    }
  };

  const handleView = (authId) => {
    navigate(`/user/${authId}`);
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Admin Dashboard</h1>

      <table border="1" cellPadding="10" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Name</th>
            <th>Verified</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {users.map(u => (
            <tr key={u.auth_id}>
              <td>{u.name}</td>
              <td>{u.verified ? 'Yes' : 'No'}</td>

              <td>
                <button onClick={() => toggleVerify(u.auth_id, u.verified)}>
                  {u.verified ? 'Unverify' : 'Verify'}
                </button>

                <button onClick={() => handleView(u.auth_id)}>
                  View
                </button>

                <button onClick={() => handleDelete(u.auth_id)}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>

      </table>
    </div>
  );
};

export default AdminDashboard;