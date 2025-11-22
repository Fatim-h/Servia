import React from "react";
import "./ConfirmDeleteModal.css";

export default function ConfirmDeleteModal({ target, onClose, onConfirm }) {
    return (
        <div className="delete-overlay">
            <div className="delete-box">
                <h3>Confirm Deletion</h3>
                <p>
                    Delete this {target.type}? This action cannot be undone.
                </p>

                <div className="delete-actions">
                    <button className="cancel" onClick={onClose}>Cancel</button>
                    <button className="confirm" onClick={onConfirm}>Delete</button>
                </div>
            </div>
        </div>
    );
}