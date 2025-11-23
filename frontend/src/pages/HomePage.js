import React, { useEffect, useState } from "react";
import { getAllCauses } from "../services/causeService";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";
import Header from "../components/Header";

// import your map library (Leaflet)
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function HomePage() {
  const [causes, setCauses] = useState([]);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const navigate = useNavigate();

  useEffect(() => {
    fetchCauses();
  }, []);

  async function fetchCauses() {
    try {
      const data = await getAllCauses();
      setCauses(data.causes);
    } catch (err) {
      console.error("Error fetching causes:", err);
    }
  }

  const filteredCauses = causes.filter((c) => {
    const matchesFilter =
      filter === "all" ||
      (filter === "ngo" && c.type === "NGO") ||
      (filter === "event" && c.type === "Event");

    const searchText = (c.name + " " + c.description + " " + c.type).toLowerCase();
    const matchesSearch = searchText.includes(search.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  return (
    <div className="homepage-container">
      <Header />

      <div className="homepage-content">

        {/* Search Bar */}
        <input
          type="text"
          className="search-bar"
          placeholder="Search causes..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {/* Filter Toggle */}
        <div className="filter-buttons">
          <button
            className={filter === "all" ? "active" : ""}
            onClick={() => setFilter("all")}
          >
            All
          </button>
          <button
            className={filter === "ngo" ? "active" : ""}
            onClick={() => setFilter("ngo")}
          >
            NGOs
          </button>
          <button
            className={filter === "event" ? "active" : ""}
            onClick={() => setFilter("event")}
          >
            Events
          </button>
        </div>

        {/* Map Section */}
        <div className="map-section">
          <MapContainer center={[20.5937, 78.9629]} zoom={4} scrollWheelZoom={true}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

            {filteredCauses.map((cause) => (
              cause.latitude && cause.longitude ? (
                <Marker
                  key={cause.cause_id}
                  position={[cause.latitude, cause.longitude]}
                  eventHandlers={{
                    click: () => navigate(`/cause/${cause.cause_id}`)
                  }}
                >
                  <Popup>{cause.name}</Popup>
                </Marker>
              ) : null
            ))}
          </MapContainer>
        </div>

        {/* Gallery Section */}
        <div className="cause-gallery">
          {filteredCauses.map((cause) => (
            <div
              className="cause-card"
              key={cause.cause_id}
              onClick={() => navigate(`/cause/${cause.cause_id}`)}
            >
              <img
                src={cause.logo || "/placeholder.png"}
                alt={cause.name}
                className="cause-logo"
              />
              <h3>{cause.name}</h3>
              <p>{cause.type}</p>
              <p className="cause-description">{cause.description}</p>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}