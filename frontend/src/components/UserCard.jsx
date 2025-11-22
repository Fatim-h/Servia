import React from "react";
import "./Card.css";

export default function UserCard({ user, onVerify, onUnverify, onDelete, onView }) {
    return (
        <div className="card">
            <h3>{user.name}</h3>
            <p><strong>Role:</strong> {user.role}</p>
            <p><strong>Status:</strong> {user.verified ? "Verified" : "Unverified"}</p>

            <div className="card-actions">
                {!user.verified && <button className="verify" onClick={onVerify}>Verify</button>}
                {user.verified && <button className="unverify" onClick={onUnverify}>Unverify</button>}

                <button className="view" onClick={onView}>View Details</button>
                <button className="delete" onClick={onDelete}>Delete</button>
            </div>
        </div>
    );
}