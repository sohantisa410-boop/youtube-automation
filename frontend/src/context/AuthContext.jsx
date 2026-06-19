import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(!!token);

  async function fetchUser(currentToken) {
    try {
      const { data } = await api.get("/auth/me", {
        headers: currentToken ? { Authorization: `Bearer ${currentToken}` } : undefined
      });
      setUser(data);
    } catch {
      setToken(null);
      localStorage.removeItem("token");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (token) {
      fetchUser(token);
    } else {
      setLoading(false);
    }
  }, [token]);

  const value = useMemo(
    () => ({
      token,
      user,
      loading,
      isAuthenticated: !!token && !!user,
      isAdmin: user?.role === "admin",
      async login(email, password) {
        const { data } = await api.post("/auth/login", { email, password });
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
      },
      async register(payload) {
        await api.post("/auth/register", payload);
      },
      logout() {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
      },
      refreshUser: () => fetchUser(token),
    }),
    [token, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
