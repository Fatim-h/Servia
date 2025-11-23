import axios from "axios";

const API = "/api/admin";

export default {
    getUsers: async (token) =>
        axios.get(`${API}/users`, {
            headers: { Authorization: `Bearer ${token}` },
        }),

    getCauses: async (token) =>
        axios.get(`${API}/causes`, {
            headers: { Authorization: `Bearer ${token}` },
        }),

    verify: async (auth_id, token) =>
        axios.patch(`${API}/verify/${auth_id}`, {}, {
            headers: { Authorization: `Bearer ${token}` },
        }),

    unverify: async (auth_id, token) =>
        axios.patch(`${API}/unverify/${auth_id}`, {}, {
            headers: { Authorization: `Bearer ${token}` },
        }),

    deleteUser: async (id, token) =>
        axios.delete(`${API}/delete/user/${id}`, {
            headers: { Authorization: `Bearer ${token}` },
        }),

    deleteCause: async (id, token) =>
        axios.delete(`${API}/delete/cause/${id}`, {
            headers: { Authorization: `Bearer ${token}` },
        })
};