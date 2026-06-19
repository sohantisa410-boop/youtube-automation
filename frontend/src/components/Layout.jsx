import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { logout, isAdmin, user } = useAuth();

  const nav = [
    ["Dashboard Home", "/"],
    ["Channels Manager", "/channels"],
    ["Videos Manager", "/videos"],
    ["Scheduler", "/scheduler"],
    ["Upload Queue", "/queue"],
    ["Analytics", "/analytics"],
    ["Settings", "/settings"],
  ];

  if (isAdmin) {
    nav.push(["Admin Panel", "/admin"]);
  }

  return (
    <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", minHeight: "100vh", fontFamily: "Inter, sans-serif" }}>
      <aside style={{ background: "#111827", color: "#fff", padding: 24 }}>
        <div style={{ marginBottom: 24 }}>
          <h2 style={{ margin: 0 }}>YouTube SaaS</h2>
          <p style={{ color: "#94a3b8", marginTop: 8 }}>{user ? `Welcome, ${user.full_name}` : "Welcome creator"}</p>
        </div>
        <nav style={{ display: "grid", gap: 12 }}>
          {nav.map(([label, to]) => (
            <Link key={to} to={to} style={{ color: "#cbd5e1", textDecoration: "none" }}>
              {label}
            </Link>
          ))}
        </nav>
        <button
          onClick={logout}
          style={{ marginTop: 24, width: "100%", padding: "10px 14px", borderRadius: 8, border: "none", background: "#ef4444", color: "#fff", cursor: "pointer" }}
        >
          Logout
        </button>
      </aside>
      <main style={{ padding: 24, background: "#f8fafc" }}>
        <Outlet />
      </main>
    </div>
  );
}
