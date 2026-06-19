import { useEffect, useState } from "react";
import api from "../services/api";

export default function ChannelsPage() {
  const [channels, setChannels] = useState([]);
  const [form, setForm] = useState({ name: "", niche: "", uploads_per_day: 1, client_secret_path: "" });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchChannels() {
    try {
      const { data } = await api.get("/channels");
      setChannels(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to load channels.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchChannels();
  }, []);

  async function createChannel(e) {
    e.preventDefault();
    setError("");
    try {
      await api.post("/channels", form);
      setForm({ name: "", niche: "", uploads_per_day: 1, client_secret_path: "" });
      setMessage("Channel created successfully.");
      fetchChannels();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to create channel.");
    }
  }

  async function deleteChannel(channelId) {
    setError("");
    try {
      await api.delete(`/channels/${channelId}`);
      setMessage("Channel deleted.");
      fetchChannels();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to delete channel.");
    }
  }

  return (
    <div>
      <h1>Channels Manager</h1>
      <form onSubmit={createChannel} style={{ display: "grid", gridTemplateColumns: "1fr 1fr 150px 220px auto", gap: 10, marginBottom: 20 }}>
        <input placeholder="Channel Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <input placeholder="Niche" value={form.niche} onChange={(e) => setForm({ ...form, niche: e.target.value })} required />
        <input
          type="number"
          min={1}
          placeholder="Uploads/day"
          value={form.uploads_per_day}
          onChange={(e) => setForm({ ...form, uploads_per_day: Number(e.target.value) })}
        />
        <input
          placeholder="Client secret path"
          value={form.client_secret_path}
          onChange={(e) => setForm({ ...form, client_secret_path: e.target.value })}
        />
        <button type="submit">Create Channel</button>
      </form>
      {message && <p style={{ color: "#16a34a" }}>{message}</p>}
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      <div style={{ background: "#fff", padding: 20, borderRadius: 14, boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
        <h2>My Channels</h2>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {loading && <li>Loading channels...</li>}
          {!loading && channels.map((channel) => (
            <li key={channel.id} style={{ display: "flex", justifyContent: "space-between", padding: 14, borderBottom: "1px solid #e5e7eb" }}>
              <div>
                <strong>{channel.name}</strong>
                <p style={{ margin: "4px 0", color: "#475569" }}>
                  {channel.niche} • {channel.uploads_per_day} uploads/day
                </p>
              </div>
              <button onClick={() => deleteChannel(channel.id)} style={{ background: "#ef4444", color: "#fff", border: "none", borderRadius: 8, padding: "8px 12px", cursor: "pointer" }}>
                Delete
              </button>
            </li>
          ))}
          {!loading && channels.length === 0 && <li>No channels yet. Add your first channel.</li>}
        </ul>
      </div>
    </div>
  );
}
