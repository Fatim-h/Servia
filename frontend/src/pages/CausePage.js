import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const CausePage = () => {
  const { causeId } = useParams();
  const [cause, setCause] = useState(null);

  useEffect(() => {
    const fetchCause = async () => {
      try {
        const res = await axios.get(`http://localhost:5000/api/causes/${causeId}`);
        setCause(res.data);
      } catch (err) {
        console.error('Failed to fetch cause', err);
      }
    };
    fetchCause();
  }, [causeId]);

  if (!cause) return <div>Loading...</div>;

  return (
    <div style={{ padding: '2rem' }}>
      <h1>{cause.name}</h1>
      <p><strong>Type:</strong> {cause.type.toUpperCase()}</p>
      <p><strong>Description:</strong> {cause.description}</p>
      <p><strong>Email:</strong> {cause.email}</p>
      {cause.logo && <img src={cause.logo} alt={cause.name} style={{ width: '300px', marginTop: '1rem' }} />}
    </div>
  );
};

export default CausePage;