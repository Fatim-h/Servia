import React, { useState, useEffect } from "react";
import AdminService from "../services/AdminService";
import UserCard from "../components/UserCard";
import CauseCard from "../components/CauseCard";
import AdminTabs from "../components/AdminTabs";
import DetailsModal from "../components/DetailsModal";
import ConfirmDeleteModal from "../components/ConfirmDeleteModal";
import "./AdminDashboard.css";

export default function AdminDashboard() {
    const [activeTab, setActiveTab] = useState("unverifiedUsers");

    const [users, setUsers] = useState([]);
    const [causes, setCauses] = useState([]);

    const [selectedItem, setSelectedItem] = useState(null);
    const [deleteTarget, setDeleteTarget] = useState(null);

    const token = localStorage.getItem("token");

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const u = await AdminService.getUsers(token);
            const c = await AdminService.getCauses(token);

            // These come from Axios → actual data is in u.data.data
            setUsers(u.data.data || []);
            setCauses(c.data.data || []);
        } catch (e) {
            console.error("Admin load error →", e);
        }
    };

    // ADMIN ACTIONS
    const handleVerify = async (auth_id) => {
        await AdminService.verify(auth_id, token);
        loadData();
    };

    const handleUnverify = async (auth_id) => {
        await AdminService.unverify(auth_id, token);
        loadData();
    };

    const handleDeleteUser = async (userId) => {
        await AdminService.deleteUser(userId, token);
        setDeleteTarget(null);
        loadData();
    };

    const handleDeleteCause = async (causeId) => {
        await AdminService.deleteCause(causeId, token);
        setDeleteTarget(null);
        loadData();
    };

    // FILTERS FOR TABS
    const filtered = {
        unverifiedUsers: users.filter(u => !u.verified),
        verifiedUsers: users.filter(u => u.verified),

        unverifiedCauses: causes.filter(c => !c.verified),
        verifiedCauses: causes.filter(c => c.verified),

        allUsers: users,
        allCauses: causes
    };

    const list = filtered[activeTab] || [];

    return (
        <div className="admin-container">
            <h1>Admin Dashboard</h1>

            <AdminTabs active={activeTab} setActive={setActiveTab} />

            <div className="cards-container">
                {list.map(item => {
                    // It's a user
                    if (item.user_id) {
                        return (
                            <UserCard
                                key={item.user_id}
                                user={item}
                                onVerify={() => handleVerify(item.auth_id)}
                                onUnverify={() => handleUnverify(item.auth_id)}
                                onDelete={() => setDeleteTarget({ type: "user", id: item.user_id })}
                                onView={() => setSelectedItem(item)}
                            />
                        );
                    }

                    // It's a cause
                    if (item.cause_id) {
                        return (
                            <CauseCard
                                key={item.cause_id}
                                cause={item}
                                onClick={() => setSelectedItem(item)} // View cause details
                            />
                        );
                    }

                    return null;
                })}
            </div>

            {selectedItem && (
                <DetailsModal item={selectedItem} onClose={() => setSelectedItem(null)} />
            )}

            {deleteTarget && (
                <ConfirmDeleteModal
                    target={deleteTarget}
                    onClose={() => setDeleteTarget(null)}
                    onConfirm={() =>
                        deleteTarget.type === "user"
                            ? handleDeleteUser(deleteTarget.id)
                            : handleDeleteCause(deleteTarget.id)
                    }
                />
            )}
        </div>
    );
}