import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header"; 
import axios from "axios";
import "./CausePage.css";
import './LeafletIcons'; // custom Leaflet icon setup

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function CausePage() {
  const { id } = useParams(); // cause_id
  const [cause, setCause] = useState(null);
  const [loading, setLoading] = useState(true);

  // Get logged-in user from localStorage
  const storedUser = localStorage.getItem("logged_user");
  const currentUser = storedUser ? JSON.parse(storedUser) : null;

  // Form visibility states
  const [activeForm, setActiveForm] = useState(""); // "donate", "volunteer", "feedback"

  // Form data states
  const [donateAmount, setDonateAmount] = useState("");
  const [volunteerHours, setVolunteerHours] = useState("");
  const [volunteerDate, setVolunteerDate] = useState("");
  const [feedbackComment, setFeedbackComment] = useState("");
  const [feedbackRating, setFeedbackRating] = useState("");

  useEffect(() => {
    fetchCause();
  }, [id]);

  async function fetchCause() {
    try {
      const res = await axios.get(`/api/causes/${id}`);
      setCause(res.data);
    } catch (err) {
      console.error("Error loading cause:", err);
    } finally {
      setLoading(false);
    }
  }

  // ----- Helper function to handle errors -----
  const handleAxiosError = (err) => {
    if (err.response) {
      alert(err.response.data.error || "Something went wrong");
    } else {
      alert("Network error");
    }
  };

  // ----- Form submit handlers -----
  const handleDonate = async (e) => {
    e.preventDefault();
    if (!currentUser) return alert("You must be logged in");

    try {
      const res = await axios.post(`/api/cause/${id}/donate`, {
        auth_id: currentUser.auth_id,
        amount: parseFloat(donateAmount)
      });
      alert(res.data.message);
      setDonateAmount("");
      setActiveForm("");
    } catch (err) {
      handleAxiosError(err);
    }
  };

  const handleVolunteer = async (e) => {
    e.preventDefault();
    if (!currentUser) return alert("You must be logged in");

    try {
      const res = await axios.post(`/api/cause/${id}/volunteer`, {
        auth_id: currentUser.auth_id,
        hours: parseFloat(volunteerHours),
        date: volunteerDate || null
      });
      alert(res.data.message);
      setVolunteerHours("");
      setVolunteerDate("");
      setActiveForm("");
    } catch (err) {
      handleAxiosError(err);
    }
  };

  const handleFeedback = async (e) => {
    e.preventDefault();
    if (!currentUser) return alert("You must be logged in");

    try {
      const res = await axios.post(`/api/cause/${id}/feedback`, {
        auth_id: currentUser.auth_id,
        comment: feedbackComment,
        rating: parseInt(feedbackRating)
      });
      alert(res.data.message);
      setFeedbackComment("");
      setFeedbackRating("");
      setActiveForm("");
    } catch (err) {
      handleAxiosError(err);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!cause) return <div className="error">Cause not found.</div>;

  const locations = cause.locations || [];
  const hasLocations = locations.length > 0;
  const center = hasLocations
    ? [locations[0].latitude, locations[0].longitude]
    : [20.5937, 78.9629];

  return (
    <>
      <Header />
      <div className="cause-page">
        {/* HEADER IMAGE */}
        <div className="cause-banner">
          <img src={cause.logo || "/placeholder.png"} alt={cause.name} />
        </div>

        {/* MAIN INFO */}
        <div className="cause-info-section">
          <h1>{cause.name}</h1>
          <p className="cause-type">{cause.type}</p>
          <p className="cause-description">{cause.description || "No description available."}</p>

          {/* CTA BUTTONS */}
          <div className="cta-buttons">
            <button onClick={() => setActiveForm(activeForm === "donate" ? "" : "donate")} className="donate-btn">Donate</button>
            <button onClick={() => setActiveForm(activeForm === "volunteer" ? "" : "volunteer")} className="volunteer-btn">Volunteer</button>
            <button onClick={() => setActiveForm(activeForm === "feedback" ? "" : "feedback")} className="feedback-btn">Feedback</button>
          </div>

          {/* DONATE FORM */}
          {activeForm === "donate" && (
            <form onSubmit={handleDonate} className="cause-form">
              <label>
                Amount:
                <input type="number" step="0.01" value={donateAmount} onChange={(e) => setDonateAmount(e.target.value)} required />
              </label>
              <button type="submit">Submit Donation</button>
            </form>
          )}

          {/* VOLUNTEER FORM */}
          {activeForm === "volunteer" && (
            <form onSubmit={handleVolunteer} className="cause-form">
              <button type="submit">Submit Volunteer</button>
            </form>
          )}

          {/* FEEDBACK FORM */}
          {activeForm === "feedback" && (
            <form onSubmit={handleFeedback} className="cause-form">
              <label>
                Comment:
                <textarea value={feedbackComment} onChange={(e) => setFeedbackComment(e.target.value)} required />
              </label>
              <label>
                Rating:
                <input type="number" min="1" max="5" value={feedbackRating} onChange={(e) => setFeedbackRating(e.target.value)} required />
              </label>
              <button type="submit">Submit Feedback</button>
            </form>
          )}
        </div>

        {/* CONTACTS */}
        <div className="details-section">
          <h2>Contact Information</h2>
          {cause.contacts?.length > 0 ? (
            <ul>{cause.contacts.map((c, i) => <li key={i}>{c}</li>)}</ul>
          ) : <p>No contacts listed.</p>}
        </div>

        {/* SOCIALS */}
        <div className="details-section">
          <h2>Social Media</h2>
          {cause.socials?.length > 0 ? (
            <ul>{cause.socials.map((s, i) => <li key={i}>{s}</li>)}</ul>
          ) : <p>No social media listed.</p>}
        </div>

        {/* EVENT-SPECIFIC DETAILS */}
        {cause.type === "Event" && (
          <div className="details-section">
            <h2>Event Details</h2>
            <p><strong>Date:</strong> {cause.date || "TBA"}</p>
            <p><strong>Time:</strong> {cause.time || "TBA"}</p>
            <p><strong>Capacity:</strong> {cause.capacity || "Unlimited"}</p>
          </div>
        )}

        {/* NGO-SPECIFIC DETAILS */}
        {cause.type === "NGO" && (
          <div className="details-section">
            <h2>NGO Information</h2>
            <p><strong>Year Established:</strong> {cause.year_est || "Unknown"}</p>
            <p><strong>Organization Age:</strong> {cause.age || "Unknown"}</p>
          </div>
        )}

        {/* MAP */}
        <div className="cause-map-section">
          <h2>Location</h2>
          {hasLocations ? (
            <MapContainer center={center} zoom={12} scrollWheelZoom={false} style={{ height: "400px", width: "100%" }}>
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              {locations.map((loc) => loc.latitude && loc.longitude && (
                <Marker key={loc.loc_id} position={[loc.latitude, loc.longitude]}>
                  <Popup>{loc.address || loc.city || "Location"}</Popup>
                </Marker>
              ))}
            </MapContainer>
          ) : <p>No location listed.</p>}
        </div>

        
      </div>
    </>
  );
}