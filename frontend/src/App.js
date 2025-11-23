import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CausePage from "./pages/CausePage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/cause/:id" element={<CausePage />} />
      </Routes>
    </BrowserRouter>
  );
}