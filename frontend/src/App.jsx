import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";
import Dashboard from "./Dashboard";
import Pricing from "./pages/Pricing";
import Promotions from "./pages/Promotions";
import Inventory from "./pages/Inventory";
import LandingPage from "./LandingPage";
import Register from "./Register";
import Login from "./Login";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Landing */}
        <Route path="/" element={<LandingPage />} />

        {/* Auth */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Dashboard with Sidebar */}
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/promotions" element={<Promotions />} />
          <Route path="/inventory" element={<Inventory />} />
        </Route>

      </Routes>
    </BrowserRouter>
  );
}
