import React, { useState } from 'react';
import NGOCard from './components/NGOCard';
import ngos from './demoData';

function App() {
 
  const [ngoList] = useState(ngos);

  return (
    <div>
      <h1>NGO Directory (Demo)</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {ngoList.map(ngo => (
          <NGOCard key={ngo.id} ngo={ngo} />
        ))}
      </div>
    </div>
  );
}

export default App;