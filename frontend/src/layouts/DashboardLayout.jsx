import { Outlet, useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function DashboardLayout() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar onLogout={logout} />
      <div className="flex-1 p-6">
        <Outlet />
      </div>
    </div>
  );
}
