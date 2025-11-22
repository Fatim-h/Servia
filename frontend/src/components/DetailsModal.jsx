import React from "react";
import "./DetailsModal.css";

export default function DetailsModal({ item, onClose }) {
    return (
        <div className="details-overlay">
            <div className="details-panel">
                <button className="close-btn" onClick={onClose}>✖</button>
                <h2>Details</h2>

                <pre>{JSON.stringify(item, null, 2)}</pre>
            </div>
        </div>
    );
}