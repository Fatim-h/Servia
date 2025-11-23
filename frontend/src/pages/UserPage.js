// src/pages/UserPage.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import './UserPage.css';
import Header from "../components/Header"; 
import api from '../services/api';

const UserPage = () => {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [causes, setCauses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const resUser = await api.get(`/api/admin/user/${userId}`);
        setUser(resUser.data.user);

        const resCauses = await api.get(`/api/admin/user/${userId}/causes`);
        setCauses(resCauses.data.causes);

        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    };
    fetchUserData();
  }, [userId]);

  if (loading) return <p>Loading...</p>;
  if (!user) return <p>User not found</p>;

  return (
    <><Header />
    <div className="user-page">
      {/* User Info Section */}
      <div className="user-info-section">
        <h1>{user.name}</h1>
        <p>User ID: {user.user_id}</p>
        <p>Email: {user.email}</p>
        <p>Age: {user.age}</p>
        <p className="user-verified">
          Verified: {user.verified ? 'Yes' : 'No'}
        </p>

        {/* Description */}
        {user.description && (
          <p className="user-description">{user.description}</p>
        )}
      </div>

      {/* Owned Causes Section */}
      <div className="details-section">
        <h2>Owned Causes</h2>
        {causes.length === 0 ? (
          <p>No causes owned</p>
        ) : (
          <table className="owned-causes-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Verified</th>
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
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
    </>
  );
};

export default UserPage;