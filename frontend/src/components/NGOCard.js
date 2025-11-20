import React from 'react';
import { Link } from 'react-router-dom';
import './NGOCard.css'; // optional styling file

const NGOCard = ({ ngo }) => {
  return (
    <div className="ngo-card" >
      {ngo.logo_url && (
        <img
          src={ngo.logo_url}
          alt={`${ngo.name} logo`}
          className="ngo-logo"
        />
      )}
      <h2>
        <Link to={`/ngo/${ngo.id}`} state={{ ngo }}>
          {ngo.name}
        </Link>
      </h2>
      <p><strong>Mission:</strong> {ngo.mission}</p>
      <p><strong>Category:</strong> {ngo.category}</p>
      <p><strong>Contact:</strong> {ngo.contact}</p>
      <p><strong>Location:</strong> {ngo.location}</p>
      {ngo.verified && <p className="verified">✅ Verified NGO</p>}
    </div>
  );
};

export default NGOCard;