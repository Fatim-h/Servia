import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import HomePage from './pages/HomePage';
import NGOPage from './components/NGOPage'; // <-- Add this import

function App() {
  return (
    <Router>
      <Routes>

        {/* Home Page */}
        <Route path="/" element={<HomePage />} />

        {/* NGO Page */}
        <Route path="/ngo/:id" element={<NGOPage />} />

      </Routes>
    </Router>
  );
}

export default App;