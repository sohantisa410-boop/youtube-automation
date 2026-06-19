import { useEffect, useState } from "react";
import api from "../services/api";

export default function QueuePage() {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/queue")
      .then((res) => setQueue(res.data))
      .catch((err) => setError(err?.response?.data?.detail || "Unable to load queue."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1>Upload Queue</h1>
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      <div style={{ background: "#fff", padding: 20, borderRadius: 14, boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: 12 }}>Video ID</th>
              <th style={{ textAlign: "left", padding: 12 }}>Scheduled</th>
              <th style={{ textAlign: "left", padding: 12 }}>Status</th>
              <th style={{ textAlign: "left", padding: 12 }}>Retries</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={4} style={{ padding: 12 }}>Loading queue...</td>
              </tr>
            )}
            {!loading && queue.map((item) => (
              <tr key={item.id} style={{ borderTop: "1px solid #e5e7eb" }}>
                <td style={{ padding: 12 }}>{item.video_id}</td>
                <td style={{ padding: 12 }}>{new Date(item.scheduled_at).toLocaleString()}</td>
                <td style={{ padding: 12 }}>{item.status}</td>
                <td style={{ padding: 12 }}>{item.retries}</td>
              </tr>
            ))}
            {!loading && queue.length === 0 && (
              <tr>
                <td colSpan={4} style={{ padding: 12, color: "#6b7280" }}>
                  No scheduled uploads yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
