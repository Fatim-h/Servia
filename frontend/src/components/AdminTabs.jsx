import React from "react";
import "./AdminTabs.css";

export default function AdminTabs({ active, setActive }) {
    const tabs = [
        ["unverifiedUsers", "Unverified Users"],
        ["verifiedUsers", "Verified Users"],
        ["unverifiedCauses", "Unverified Causes"],
        ["verifiedCauses", "Verified Causes"],
        ["allUsers", "All Users"],
        ["allCauses", "All Causes"]
    ];

    return (
        <div className="admin-tabs">
            {tabs.map(([key, label]) => (
                <button
                    key={key}
                    className={active === key ? "active" : ""}
                    onClick={() => setActive(key)}
                >
                    {label}
                </button>
            ))}
        </div>
    );
}