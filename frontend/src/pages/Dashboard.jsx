import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip,} from "recharts";
import api from "../api/axios";

const COLORS = ["#667eea", "#764ba2", "#f093fb", "#4facfe"];

const StatCard = ({icon, title, value, sub, color}) => (
    <div style={{
        background: "rgba(255,255,255,0.05)",
        border: "1px solid rgba(255,255,255,0.1)",
        borderRadius: "16px",
        padding: "24px",
        flex: 1,
        minWidth: "200px",
    }}>
        <div style={{display: "flex", justifyContent: "space-between", alignItems: "flex-start"}}>
            <div>
                <p style={{color: "rgba(255,255,255,0.5)", margin: "0 0 8px", fontSize: "13px"}}>{title}</p>
                <h2 style={{color: "#fff", margin: 0, fontSize: "32px", fontWeight: "700"}}>{value}</h2>
                {sub && <p style={{color: color || "#667eea", margin: "6px 0 0", fontSize: "13px"}}>{sub}</p>}
            </div>
            <div style={{
                fontSize: "28px",
                background: "rgba(255,255,255,0.08)",
                borderRadius: "12px",
                padding: "10px",
            }}>
                {icon}
            </div>
        </div>
    </div>
);

export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const res = await api.get("/api/stats/dashboard");
            setStats(res.data);
        } catch {
            navigate("/login");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    if (loading) return (
        <div style={{
            minHeight: "100vh",
            background: "linear-gradient(135deg, #1a1a2e, #16213e, #0f3460)",
            display: "flex", alignItems: "center", justifyContent: "center",
            color: "#fff", fontSize: "18px",
        }}>
            ⏳ Yuklanmoqda...
        </div>
    );

    const pieData = stats ? [
        {name: "Yod olingan", value: stats.total_memorized},
        {name: "O'rganilmoqda", value: stats.total_assigned - stats.total_memorized},
    ] : [];

    const activityData = [
        {name: "Bugun", foydalanuvchilar: stats?.new_users_today || 0, takrorlashlar: stats?.reviews_today || 0},
    ];

    return (
        <div style={{
            minHeight: "100vh",
            background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
            fontFamily: "'Segoe UI', sans-serif",
            color: "#fff",
        }}>
            {/* Header */}
            <div style={{
                background: "rgba(255,255,255,0.03)",
                borderBottom: "1px solid rgba(255,255,255,0.08)",
                padding: "16px 32px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
            }}>
                <div style={{display: "flex", alignItems: "center", gap: "12px"}}>
                    <span style={{fontSize: "28px"}}>🕌</span>
                    <div>
                        <h1 style={{margin: 0, fontSize: "20px", fontWeight: "700"}}>HifzBot</h1>
                        <p style={{margin: 0, fontSize: "12px", color: "rgba(255,255,255,0.4)"}}>Admin Panel</p>
                    </div>
                </div>
                <button
                    onClick={handleLogout}
                    style={{
                        background: "rgba(255,99,99,0.15)",
                        border: "1px solid rgba(255,99,99,0.3)",
                        borderRadius: "8px",
                        color: "#ff6363",
                        padding: "8px 16px",
                        cursor: "pointer",
                        fontSize: "14px",
                    }}
                >
                    Chiqish
                </button>
            </div>

            {/* Content */}
            <div style={{padding: "32px"}}>
                <h2 style={{margin: "0 0 24px", color: "rgba(255,255,255,0.9)"}}>📊 Dashboard</h2>

                {/* Stat cards */}
                <div style={{display: "flex", gap: "16px", flexWrap: "wrap", marginBottom: "32px"}}>
                    <StatCard icon="👥" title="Jami foydalanuvchilar" value={stats?.total_users || 0}
                              sub={`+${stats?.new_users_today || 0} bugun`} color="#4ade80"/>
                    <StatCard icon="✅" title="Faol foydalanuvchilar" value={stats?.active_users || 0}
                              sub={`${stats?.total_users ? Math.round(stats.active_users / stats.total_users * 100) : 0}% jami`}/>
                    <StatCard icon="📖" title="Jami oyatlar" value={stats?.total_ayahs || 0}
                              sub="Bazada mavjud"/>
                    <StatCard icon="🧠" title="Yod olingan" value={stats?.total_memorized || 0}
                              sub={`${stats?.reviews_today || 0} bugun takrorlangan`} color="#f093fb"/>
                </div>

                {/* Charts */}
                <div style={{display: "flex", gap: "24px", flexWrap: "wrap"}}>
                    {/* Pie chart */}
                    <div style={{
                        background: "rgba(255,255,255,0.05)",
                        border: "1px solid rgba(255,255,255,0.1)",
                        borderRadius: "16px",
                        padding: "24px",
                        flex: 1,
                        minWidth: "300px",
                    }}>
                        <h3 style={{margin: "0 0 20px", fontSize: "16px", color: "rgba(255,255,255,0.8)"}}>
                            🥧 Oyatlar holati
                        </h3>
                        <ResponsiveContainer width="100%" height={250}>
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={90}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {pieData.map((_, index) => (
                                        <Cell key={index} fill={COLORS[index]}/>
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{
                                        background: "#1a1a2e",
                                        border: "1px solid rgba(255,255,255,0.1)",
                                        borderRadius: "8px"
                                    }}
                                    labelStyle={{color: "#fff"}}
                                />
                                <Legend wrapperStyle={{color: "rgba(255,255,255,0.7)"}}/>
                            </PieChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Summary */}
                    <div style={{
                        background: "rgba(255,255,255,0.05)",
                        border: "1px solid rgba(255,255,255,0.1)",
                        borderRadius: "16px",
                        padding: "24px",
                        flex: 1,
                        minWidth: "300px",
                    }}>
                        <h3 style={{margin: "0 0 20px", fontSize: "16px", color: "rgba(255,255,255,0.8)"}}>
                            📈 Bugungi faollik
                        </h3>
                        <div style={{display: "flex", flexDirection: "column", gap: "16px"}}>
                            {[
                                {
                                    label: "Yangi foydalanuvchilar",
                                    value: stats?.new_users_today || 0,
                                    icon: "🆕",
                                    color: "#4ade80"
                                },
                                {
                                    label: "Bugun takrorlashlar",
                                    value: stats?.reviews_today || 0,
                                    icon: "🔁",
                                    color: "#667eea"
                                },
                                {
                                    label: "Jami takrorlashlar",
                                    value: stats?.total_reviews || 0,
                                    icon: "📚",
                                    color: "#f093fb"
                                },
                            ].map((item, i) => (
                                <div key={i} style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    padding: "12px 16px",
                                    background: "rgba(255,255,255,0.05)",
                                    borderRadius: "10px",
                                }}>
                  <span style={{color: "rgba(255,255,255,0.7)", fontSize: "14px"}}>
                    {item.icon} {item.label}
                  </span>
                                    <span style={{color: item.color, fontWeight: "700", fontSize: "18px"}}>
                    {item.value}
                  </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}