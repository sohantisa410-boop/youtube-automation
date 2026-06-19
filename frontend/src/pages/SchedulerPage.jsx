import { useEffect, useState } from "react";
import api from "../services/api";

export default function SchedulerPage() {
  const [videos, setVideos] = useState([]);
  const [videoId, setVideoId] = useState("");
  const [scheduledAt, setScheduledAt] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadVideos() {
    const { data } = await api.get("/videos");
    const generatedVideos = data.filter((video) => video.status === "generated");
    setVideos(generatedVideos);
    if (data.length > 0 && !videoId) {
      setVideoId(generatedVideos[0]?.id || "");
    }
  }

  useEffect(() => {
    async function load() {
      setError("");
      try {
        await loadVideos();
      } catch (err) {
        setError(err?.response?.data?.detail || "Unable to load schedulable videos.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function handleSchedule(e) {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/schedule", {
        video_id: Number(videoId),
        scheduled_at: scheduledAt,
      });
      setMessage(data.message);
      await loadVideos();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to schedule video.");
    }
  }

  return (
    <div>
      <h1>Scheduler</h1>
      <form onSubmit={handleSchedule} style={{ display: "grid", gap: 12, maxWidth: 480 }}>
        <label>
          Select video
          <select value={videoId} onChange={(e) => setVideoId(e.target.value)} style={{ width: "100%", marginTop: 8 }} required>
            <option value="">Choose video</option>
            {videos.map((video) => (
              <option key={video.id} value={video.id}>
                {video.title} ({video.status})
              </option>
            ))}
          </select>
        </label>
        <label>
          Schedule date/time
          <input
            type="datetime-local"
            value={scheduledAt}
            onChange={(e) => setScheduledAt(e.target.value)}
            required
            style={{ width: "100%", marginTop: 8 }}
          />
        </label>
        <button type="submit" style={{ width: 180, padding: "10px 14px", borderRadius: 8, border: "none", background: "#2563eb", color: "#fff", cursor: "pointer" }}>
          Schedule
        </button>
      </form>
      {loading && <p style={{ marginTop: 16 }}>Loading videos...</p>}
      {!loading && videos.length === 0 && <p style={{ marginTop: 16, color: "#6b7280" }}>No generated videos are ready to schedule.</p>}
      {message && <p style={{ marginTop: 16, color: "#16a34a" }}>{message}</p>}
      {error && <p style={{ marginTop: 16, color: "#dc2626" }}>{error}</p>}
    </div>
  );
}
