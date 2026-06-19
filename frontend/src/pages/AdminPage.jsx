import { useEffect, useState } from "react";
import api from "../services/api";

export default function AdminPage() {
  const [users, setUsers] = useState([]);
  const [stats, setStats] = useState({ channels: 0, videos: 0 });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadData() {
    setError("");
    try {
      const [usersRes, channelsRes, videosRes] = await Promise.all([
        api.get("/admin/users"),
        api.get("/admin/channels"),
        api.get("/admin/videos"),
      ]);
      setUsers(usersRes.data);
      setStats({ channels: channelsRes.data.total_channels, videos: videosRes.data.total_videos });
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to load admin data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function toggleUser(user) {
    try {
      const response = await api.patch(`/admin/users/${user.id}/status`, {
        is_active: !user.is_active,
      });
      setMessage(`Updated ${response.data.email}`);
      loadData();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to update user.");
    }
  }

  async function changePlan(user) {
    const nextPlan = user.plan === "pro" ? "free" : "pro";
    try {
      const response = await api.patch(`/admin/users/${user.id}/plan`, {
        plan: nextPlan,
      });
      setMessage(`Set ${response.data.email} to ${response.data.plan}`);
      loadData();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to change user plan.");
    }
  }

  return (
    <div>
      <h1>Admin Panel</h1>
      <div style={{ display: "flex", gap: 24, marginBottom: 24 }}>
        <section style={{ padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
          <h2>Total Channels</h2>
          <p style={{ fontSize: 32, margin: 0 }}>{stats.channels}</p>
        </section>
        <section style={{ padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
          <h2>Total Videos</h2>
          <p style={{ fontSize: 32, margin: 0 }}>{stats.videos}</p>
        </section>
      </div>
      {loading && <p>Loading admin data...</p>}
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      {message && <p style={{ color: "#16a34a" }}>{message}</p>}
      <div style={{ background: "#fff", padding: 20, borderRadius: 14, boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
        <h2>Users</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: 12 }}>Email</th>
              <th style={{ textAlign: "left", padding: 12 }}>Role</th>
              <th style={{ textAlign: "left", padding: 12 }}>Plan</th>
              <th style={{ textAlign: "left", padding: 12 }}>Status</th>
              <th style={{ textAlign: "left", padding: 12 }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} style={{ borderTop: "1px solid #e5e7eb" }}>
                <td style={{ padding: 12 }}>{user.email}</td>
                <td style={{ padding: 12 }}>{user.role}</td>
                <td style={{ padding: 12 }}>{user.plan}</td>
                <td style={{ padding: 12 }}>{user.is_active ? "Active" : "Disabled"}</td>
                <td style={{ padding: 12, display: "flex", gap: 8 }}>
                  <button
                    onClick={() => toggleUser(user)}
                    style={{ padding: "8px 10px", borderRadius: 8, border: "none", cursor: "pointer", background: "#2563eb", color: "#fff" }}
                  >
                    {user.is_active ? "Disable" : "Enable"}
                  </button>
                  <button
                    onClick={() => changePlan(user)}
                    style={{ padding: "8px 10px", borderRadius: 8, border: "none", cursor: "pointer", background: "#f59e0b", color: "#fff" }}
                  >
                    {user.plan === "pro" ? "Downgrade" : "Upgrade"}
                  </button>
                </td>
              </tr>
            ))}
            {!loading && users.length === 0 && (
              <tr>
                <td colSpan={5} style={{ padding: 12, color: "#6b7280" }}>
                  No users found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
