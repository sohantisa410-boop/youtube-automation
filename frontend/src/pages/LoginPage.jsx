import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      if (isRegister) {
        await register({ email, password, full_name: fullName });
      }
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to complete request");
    }
  }

  return (
    <div style={{ maxWidth: 420, margin: "80px auto", padding: 24, border: "1px solid #e2e8f0", borderRadius: 12, background: "#fff" }}>
      <h2 style={{ marginBottom: 20 }}>{isRegister ? "Create account" : "Sign in"}</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 14 }}>
        {isRegister && (
          <input
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
        )}
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" style={{ padding: "10px 14px", borderRadius: 8, background: "#2563eb", color: "#fff", border: "none" }}>
          {isRegister ? "Register" : "Login"}
        </button>
      </form>
      {error && <p style={{ marginTop: 12, color: "#dc2626" }}>{error}</p>}
      <button
        type="button"
        style={{ marginTop: 16, background: "transparent", border: "none", color: "#2563eb", cursor: "pointer" }}
        onClick={() => {
          setIsRegister((current) => !current);
          setError("");
        }}
      >
        {isRegister ? "Already have an account? Login" : "Create an account"}
      </button>
    </div>
  );
}
