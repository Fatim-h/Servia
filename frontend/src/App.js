import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CausePage from "./pages/CausePage";
import UserPage from "./pages/UserPage";
import LoginPage from './pages/LoginPage';
import Header from './components/Header';
import AdminDashboard from './pages/AdminDashboard';
import UserDashboard from './pages/UserDashboard';
import SignUp from './pages/SignUp';
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/cause/:id" element={<CausePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/admindashboard" element={<AdminDashboard />} />
        <Route path="/userdashboard" element={<UserDashboard />} />
        <Route path="/admin/user/:userId" element={<UserPage />} />
        <Route path="/cause/:causeId" element={<CausePage />} />
      </Routes>
    </BrowserRouter>
  );
}