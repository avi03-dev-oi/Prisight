import { NavLink } from "react-router-dom";

export default function Sidebar({ onLogout }) {
  const linkClass = ({ isActive }) =>
    `block px-4 py-2 rounded ${
      isActive ? "bg-indigo-600 text-white" : "text-gray-300"
    }`;

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col justify-between">
      <div>
        <h1 className="text-xl font-bold p-6">Prisight</h1>

        <nav className="space-y-2 px-3">
          <NavLink to="/dashboard" className={linkClass}>
            Dashboard
          </NavLink>
          <NavLink to="/pricing" className={linkClass}>
            Pricing
          </NavLink>
          <NavLink to="/promotions" className={linkClass}>
            Promotions
          </NavLink>
          <NavLink to="/inventory" className={linkClass}>
            Inventory
          </NavLink>
        </nav>
      </div>

      {/* Logout */}
      <button
        onClick={onLogout}
        className="m-4 bg-red-600 hover:bg-red-700 py-2 rounded"
      >
        Logout
      </button>
    </aside>
  );
}
