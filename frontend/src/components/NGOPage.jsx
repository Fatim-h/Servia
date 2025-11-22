import { useParams, useLocation } from 'react-router-dom';

const NGOPage = () => {
  const { id } = useParams();
  const { state } = useLocation();
  const ngo = state?.ngo; // the full object from Link

  return (
    <div>
      <h1>{ngo?.name || "NGO Details"}</h1>
      {ngo && (
        <>
          <p><strong>Mission:</strong> {ngo.mission}</p>
          <p><strong>Category:</strong> {ngo.category}</p>
          <p><strong>Location:</strong> {ngo.location}</p>
        </>
      )}
    </div>
  );
};

export default NGOPage;