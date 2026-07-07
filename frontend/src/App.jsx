import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function PrivateRoute({children}) {
    const token = localStorage.getItem("token");
    return token ? children : <Navigate to="/login"/>;
}

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login/>}/>
                <Route path="/" element={
                    <PrivateRoute>
                        <Dashboard/>
                    </PrivateRoute>
                }/>
            </Routes>
        </BrowserRouter>
    );
}