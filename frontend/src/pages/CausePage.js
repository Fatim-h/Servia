import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header"; 
import axios from "axios";
import "./CausePage.css";
import './LeafletIcons'; // custom Leaflet icon setup

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function CausePage() {
  const { id } = useParams();
  const [cause, setCause] = useState(null);
  const [loading, setLoading] = useState(true);

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

  if (loading) return <div className="loading">Loading...</div>;
  if (!cause) return <div className="error">Cause not found.</div>;

  const locations = cause.locations || [];
  const hasLocations = locations.length > 0;

  // Center map on first location if exists, otherwise default
  const center = hasLocations
    ? [locations[0].latitude, locations[0].longitude]
    : [20.5937, 78.9629]; // fallback: India center

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

          <div className="cta-buttons">
            <button className="donate-btn">Donate</button>
            <button className="volunteer-btn">Volunteer</button>
          </div>
        </div>

        {/* CONTACTS */}
        <div className="details-section">
          <h2>Contact Information</h2>
          {cause.contacts?.length > 0 ? (
            <ul>
              {cause.contacts.map((c, index) => <li key={index}>{c}</li>)}
            </ul>
          ) : <p>No contacts listed.</p>}
        </div>

        {/* SOCIALS */}
        <div className="details-section">
          <h2>Social Media</h2>
          {cause.socials?.length > 0 ? (
            <ul>
              {cause.socials.map((s, index) => <li key={index}>{s}</li>)}
            </ul>
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

        {/* MAP / LOCATIONS (at bottom) */}
        <div className="cause-map-section">
          <h2>Location</h2>
          {hasLocations ? (
            <MapContainer
              center={center}
              zoom={12}
              scrollWheelZoom={false}
              style={{ height: "400px", width: "100%" }}
            >
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              {locations.map((loc) =>
                loc.latitude && loc.longitude ? (
                  <Marker key={loc.loc_id} position={[loc.latitude, loc.longitude]}>
                    <Popup>
                      {loc.address ? loc.address : loc.city ? loc.city : "Location"}
                    </Popup>
                  </Marker>
                ) : null
              )}
            </MapContainer>
          ) : (
            <p>No location listed.</p>
          )}
        </div>

      </div>
    </>
  );
}