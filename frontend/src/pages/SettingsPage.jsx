import { useEffect, useState } from "react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function SettingsPage() {
  const { user, refreshUser } = useAuth();
  const [apiKeys, setApiKeys] = useState([]);
  const [provider, setProvider] = useState("internal");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadKeys() {
    try {
      const { data } = await api.get("/auth/api-keys");
      setApiKeys(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to load API keys.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadKeys();
  }, []);

  async function createKey(e) {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/api-keys", { provider });
      setApiKeys((current) => [...current, data]);
      setMessage("New API key generated. Store it securely.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to create API key.");
    }
  }

  async function removeKey(keyId) {
    setError("");
    try {
      await api.delete(`/auth/api-keys/${keyId}`);
      setApiKeys((current) => current.filter((key) => key.id !== keyId));
      setMessage("API key removed.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to delete API key.");
    }
  }

  return (
    <div>
      <h1>Settings</h1>
      <section style={{ marginBottom: 24 }}>
        <h2>Profile</h2>
        <p>Email: {user?.email}</p>
        <p>Name: {user?.full_name}</p>
        <p>Role: {user?.role}</p>
        <p>Plan: {user?.plan}</p>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>API Keys</h2>
        <form onSubmit={createKey} style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 16 }}>
          <label>
            Provider:
            <select value={provider} onChange={(e) => setProvider(e.target.value)} style={{ marginLeft: 8 }}>
              <option value="internal">Internal</option>
              <option value="youtube">YouTube</option>
              <option value="cloudinary">Cloudinary</option>
            </select>
          </label>
          <button type="submit">Create Key</button>
        </form>
        {message && <p>{message}</p>}
        {error && <p style={{ color: "#dc2626" }}>{error}</p>}
        {loading ? (
          <p>Loading API keys...</p>
        ) : apiKeys.length > 0 ? (
          <ul>
            {apiKeys.map((key) => (
              <li key={key.id} style={{ marginBottom: 8 }}>
                {key.provider} - {key.key_masked}
                <button
                  style={{ marginLeft: 12 }}
                  onClick={() => removeKey(key.id)}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No API keys yet. Generate one above.</p>
        )}
      </section>

      <section>
        <h2>Account actions</h2>
        <button onClick={refreshUser}>Refresh profile</button>
      </section>
    </div>
  );
}
