import {useState} from "react";
import {useNavigate} from "react-router-dom";
import api from "../api/axios";

export default function Login() {
    const [adminId, setAdminId] = useState("");
    const [secret, setSecret] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        try {
            const res = await api.post("/api/auth/login", {
                admin_id: parseInt(adminId),
                secret: secret,
            });
            localStorage.setItem("token", res.data.access_token);
            navigate("/");
        } catch {
            setError("Noto'g'ri ma'lumotlar!");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            minHeight: "100vh",
            background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily: "'Segoe UI', sans-serif",
        }}>
            <div style={{
                background: "rgba(255,255,255,0.05)",
                backdropFilter: "blur(10px)",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "20px",
                padding: "40px",
                width: "100%",
                maxWidth: "400px",
            }}>
                <div style={{textAlign: "center", marginBottom: "32px"}}>
                    <div style={{fontSize: "48px", marginBottom: "8px"}}>🕌</div>
                    <h1 style={{color: "#fff", margin: 0, fontSize: "24px"}}>HifzBot</h1>
                    <p style={{color: "rgba(255,255,255,0.5)", margin: "8px 0 0"}}>Admin Panel</p>
                </div>

                <form onSubmit={handleLogin}>
                    <div style={{marginBottom: "16px"}}>
                        <label style={{
                            color: "rgba(255,255,255,0.7)",
                            fontSize: "14px",
                            display: "block",
                            marginBottom: "8px"
                        }}>
                            Telegram ID
                        </label>
                        <input
                            type="number"
                            value={adminId}
                            onChange={(e) => setAdminId(e.target.value)}
                            placeholder="7556384250"
                            style={{
                                width: "100%",
                                padding: "12px 16px",
                                background: "rgba(255,255,255,0.08)",
                                border: "1px solid rgba(255,255,255,0.15)",
                                borderRadius: "10px",
                                color: "#fff",
                                fontSize: "15px",
                                outline: "none",
                                boxSizing: "border-box",
                            }}
                        />
                    </div>

                    <div style={{marginBottom: "24px"}}>
                        <label style={{
                            color: "rgba(255,255,255,0.7)",
                            fontSize: "14px",
                            display: "block",
                            marginBottom: "8px"
                        }}>
                            Maxfiy kalit
                        </label>
                        <input
                            type="password"
                            value={secret}
                            onChange={(e) => setSecret(e.target.value)}
                            placeholder="••••••••"
                            style={{
                                width: "100%",
                                padding: "12px 16px",
                                background: "rgba(255,255,255,0.08)",
                                border: "1px solid rgba(255,255,255,0.15)",
                                borderRadius: "10px",
                                color: "#fff",
                                fontSize: "15px",
                                outline: "none",
                                boxSizing: "border-box",
                            }}
                        />
                    </div>

                    {error && (
                        <div style={{
                            background: "rgba(255,99,99,0.15)",
                            border: "1px solid rgba(255,99,99,0.3)",
                            borderRadius: "8px",
                            padding: "10px 16px",
                            color: "#ff6363",
                            fontSize: "14px",
                            marginBottom: "16px",
                        }}>
                            ❌ {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: "100%",
                            padding: "13px",
                            background: loading ? "rgba(99,179,237,0.3)" : "linear-gradient(135deg, #667eea, #764ba2)",
                            border: "none",
                            borderRadius: "10px",
                            color: "#fff",
                            fontSize: "16px",
                            fontWeight: "600",
                            cursor: loading ? "not-allowed" : "pointer",
                        }}
                    >
                        {loading ? "Kirish..." : "Kirish →"}
                    </button>
                </form>
            </div>
        </div>
    );
}