import React from 'react';
import { useNavigate } from 'react-router-dom';
import './CauseCard.css';

const CauseCard = ({ cause }) => {
  const navigate = useNavigate();

  const goToCausePage = () => {
    navigate(`/cause/${cause.cause_id}`);
  };

  return (
    <div className="cause-card" onClick={goToCausePage}>
      {cause.logo && <img src={cause.logo} alt={cause.name} className="cause-logo" />}

      <h3>{cause.name}</h3>
      <p><strong>Type:</strong> {cause.type || "Unknown"}</p>
      <p><strong>Location:</strong> {cause.location || "Unknown"}</p>
      <p>{cause.description}</p>
    </div>
  );
};

export default CauseCard;