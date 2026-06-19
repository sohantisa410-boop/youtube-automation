import { useEffect, useState } from "react";
import api from "../services/api";

export default function AnalyticsPage() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const { data } = await api.get("/analytics/summary");
        setSummary(data);
      } catch (err) {
        setError(err?.response?.data?.detail || "Unable to load analytics.");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return (
    <div>
      <h1>Analytics</h1>
      {loading && <p>Loading analytics...</p>}
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      {summary && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 16, marginTop: 20 }}>
          {[
            ["Channels", summary.channels],
            ["Videos", summary.videos],
            ["Scheduled", summary.scheduled],
            ["Views", summary.views],
            ["Likes", summary.likes],
            ["Comments", summary.comments],
          ].map(([label, value]) => (
            <section key={label} style={{ padding: 20, borderRadius: 8, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
              <p style={{ margin: 0, color: "#6b7280" }}>{label}</p>
              <h2 style={{ margin: "12px 0 0" }}>{value}</h2>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}
