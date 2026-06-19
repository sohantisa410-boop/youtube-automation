import { useEffect, useState } from "react";
import api from "../services/api";

export default function VideosPage() {
  const [videos, setVideos] = useState([]);
  const [channels, setChannels] = useState([]);
  const [channelId, setChannelId] = useState("");
  const [topic, setTopic] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchVideos() {
    const { data } = await api.get("/videos");
    setVideos(data);
  }

  async function fetchChannels() {
    const { data } = await api.get("/channels");
    setChannels(data);
    if (!channelId && data.length > 0) {
      setChannelId(data[0].id);
    }
  }

  useEffect(() => {
    async function load() {
      setError("");
      try {
        await Promise.all([fetchVideos(), fetchChannels()]);
      } catch (err) {
        setError(err?.response?.data?.detail || "Unable to load videos.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function generateVideo(e) {
    e.preventDefault();
    setError("");
    try {
      await api.post("/videos/generate", { channel_id: Number(channelId), topic });
      setTopic("");
      setMessage("Video generated. Refreshing list...");
      fetchVideos();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to generate video.");
    }
  }

  async function uploadVideo(videoId) {
    setError("");
    try {
      const { data } = await api.post("/videos/upload", { video_id: videoId });
      setMessage(data.message);
      fetchVideos();
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to upload video.");
    }
  }

  return (
    <div>
      <h1>Videos Manager</h1>
      <section style={{ marginBottom: 24, padding: 20, borderRadius: 14, background: "#fff", boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
        <h2>Create new automation video</h2>
        <form onSubmit={generateVideo} style={{ display: "grid", gap: 12, maxWidth: 600 }}>
          <label>
            Channel
            <select value={channelId} onChange={(e) => setChannelId(e.target.value)} style={{ width: "100%", marginTop: 8 }}>
              {channels.map((channel) => (
                <option key={channel.id} value={channel.id}>
                  {channel.name} ({channel.niche})
                </option>
              ))}
            </select>
          </label>
          <input
            placeholder="Video topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            required
          />
          <button type="submit" style={{ width: 180, padding: "10px 14px", borderRadius: 8, border: "none", background: "#2563eb", color: "#fff", cursor: "pointer" }}>
            Generate Video
          </button>
        </form>
        {message && <p style={{ marginTop: 12, color: "#16a34a" }}>{message}</p>}
        {error && <p style={{ marginTop: 12, color: "#dc2626" }}>{error}</p>}
      </section>

      <section style={{ background: "#fff", padding: 20, borderRadius: 14, boxShadow: "0 2px 12px rgba(15, 23, 42, 0.06)" }}>
        <h2>My Videos</h2>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {loading && <li>Loading videos...</li>}
          {!loading && videos.map((video) => (
            <li key={video.id} style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 12, padding: 14, borderBottom: "1px solid #e5e7eb" }}>
              <div>
                <strong>{video.title}</strong>
                <p style={{ margin: "8px 0 0", color: "#475569" }}>{video.description}</p>
                <p style={{ margin: "4px 0 0", color: "#94a3b8" }}>Status: {video.status}</p>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                {video.status === "generated" ? (
                  <button
                    onClick={() => uploadVideo(video.id)}
                    style={{ padding: "8px 12px", borderRadius: 8, border: "none", background: "#10b981", color: "#fff", cursor: "pointer" }}
                  >
                    Upload
                  </button>
                ) : (
                  <span style={{ color: "#6b7280" }}>Ready</span>
                )}
              </div>
            </li>
          ))}
          {!loading && videos.length === 0 && <li>No automation videos yet. Create your first video.</li>}
        </ul>
      </section>
    </div>
  );
}
