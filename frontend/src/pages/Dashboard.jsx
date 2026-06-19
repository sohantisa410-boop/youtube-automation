import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
  const [summary, setSummary] = useState({ channels: 0, videos: 0, queue: 0 });
  const [status, setStatus] = useState("checking...");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [{ data: channels }, { data: videos }, { data: queue }] = await Promise.all([
          api.get("/channels"),
          api.get("/videos"),
          api.get("/queue"),
        ]);

        setSummary({
          channels: channels.length,
          videos: videos.length,
          queue: queue.length,
        });
        setStatus("online");
      } catch (err) {
        setStatus("backend unavailable");
        setError(err?.response?.data?.detail || "Unable to load dashboard.");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {loading && <p>Loading dashboard...</p>}
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 16, marginTop: 20 }}>
        <section style={{ padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.08)" }}>
          <p style={{ margin: 0, color: "#6b7280" }}>Channels</p>
          <h2 style={{ margin: "12px 0 0" }}>{summary.channels}</h2>
        </section>
        <section style={{ padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.08)" }}>
          <p style={{ margin: 0, color: "#6b7280" }}>Videos</p>
          <h2 style={{ margin: "12px 0 0" }}>{summary.videos}</h2>
        </section>
        <section style={{ padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.08)" }}>
          <p style={{ margin: 0, color: "#6b7280" }}>Scheduled Items</p>
          <h2 style={{ margin: "12px 0 0" }}>{summary.queue}</h2>
        </section>
      </div>
      <div style={{ marginTop: 32, padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.08)" }}>
        <h2 style={{ marginBottom: 12 }}>System status</h2>
        <p style={{ margin: 0 }}>Backend status: {status}</p>
      </div>
    </div>
  );
}
