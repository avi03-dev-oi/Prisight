// frontend/src/pages/admin/ModelLeaderboard.jsx
import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { RefreshCw, Trophy, Award, TrendingDown, Target, Layers } from "lucide-react";

const API_URL = "/api/admin/tuning/leaderboard";

const MODEL_COLORS = {
  LSTM: "#6366f1",
  GRU: "#10b981",
  TRANSFORMER: "#f59e0b",
};

const DEFAULT_COLOR = "#94a3b8";

function fmt(val, decimals = 4) {
  if (val === null || val === undefined) return "—";
  return Number(val).toFixed(decimals);
}

function modelColor(name) {
  return MODEL_COLORS[name?.toUpperCase()] ?? DEFAULT_COLOR;
}

function StatCard({ label, value, icon: Icon, color = "indigo" }) {
  const colors = {
    indigo: "bg-indigo-50 text-indigo-600 border-indigo-100",
    green: "bg-emerald-50 text-emerald-600 border-emerald-100",
    amber: "bg-amber-50 text-amber-600 border-amber-100",
    violet: "bg-violet-50 text-violet-600 border-violet-100",
  };
  return (
    <div className={`rounded-xl border p-4 flex items-center gap-4 ${colors[color]}`}>
      <div className="p-2 rounded-lg bg-white/60">
        <Icon size={20} />
      </div>
      <div>
        <p className="text-xs font-medium opacity-70">{label}</p>
        <p className="text-xl font-bold">{value ?? "—"}</p>
      </div>
    </div>
  );
}

function BestModelCard({ entry }) {
  if (!entry) return null;

  const color = modelColor(entry.model_name);

  return (
    <div className="bg-gradient-to-r from-indigo-500 to-violet-500 rounded-xl p-6 text-white">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="bg-white/20 p-4 rounded-full">
            <Trophy size={40} />
          </div>
          <div>
            <p className="text-indigo-100 text-sm font-medium">Best Performing Architecture</p>
            <h2 className="text-3xl font-bold mt-1">{entry.model_name}</h2>
            <p className="text-indigo-100 mt-2">
              RMSE: {fmt(entry.best_rmse)} • MAE: {fmt(entry.best_mae)} • R²: {fmt(entry.best_r2)} • MAPE: {fmt(entry.best_mape, 2)}%
            </p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-indigo-200 text-sm">Best RMSE</p>
          <p className="text-4xl font-bold">{fmt(entry.best_rmse)}</p>
        </div>
      </div>
    </div>
  );
}

function LeaderboardTable({ entries }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">Leaderboard</h2>
        <p className="text-sm text-slate-500 mt-1">Ranked by best RMSE (lower is better)</p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-slate-50 text-left text-slate-500">
              <th className="px-6 py-3 font-medium">Rank</th>
              <th className="px-6 py-3 font-medium">Model</th>
              <th className="px-6 py-3 font-medium">RMSE</th>
              <th className="px-6 py-3 font-medium">MAE</th>
              <th className="px-6 py-3 font-medium">R²</th>
              <th className="px-6 py-3 font-medium">MAPE</th>
              <th className="px-6 py-3 font-medium">Tuned At</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry, i) => {
              const color = modelColor(entry.model_name);
              const isFirst = i === 0;

              return (
                <tr
                  key={entry.id}
                  className={`border-b border-slate-50 transition-colors ${
                    isFirst ? "bg-indigo-50/50" : "hover:bg-slate-50"
                  }`}
                >
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold ${
                        i === 0
                          ? "bg-amber-100 text-amber-700"
                          : i === 1
                          ? "bg-slate-200 text-slate-600"
                          : i === 2
                          ? "bg-orange-100 text-orange-700"
                          : "bg-slate-100 text-slate-500"
                      }`}
                    >
                      {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : i + 1}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <span
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: color }}
                      />
                      <span className="font-semibold" style={{ color }}>
                        {entry.model_name}
                      </span>
                    </div>
                  </td>
                  <td className={`px-6 py-4 font-semibold ${isFirst ? "text-indigo-600" : "text-slate-700"}`}>
                    {fmt(entry.best_rmse)}
                  </td>
                  <td className="px-6 py-4 text-slate-600">{fmt(entry.best_mae)}</td>
                  <td className="px-6 py-4 text-slate-600">{fmt(entry.best_r2)}</td>
                  <td className="px-6 py-4 text-slate-600">{fmt(entry.best_mape, 2)}%</td>
                  <td className="px-6 py-4 text-slate-400 text-xs">
                    {entry.created_at
                      ? new Date(entry.created_at + "Z").toLocaleDateString()
                      : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function RmseBarChart({ entries }) {
  const data = entries.map((e) => ({
    model: e.model_name,
    rmse: parseFloat(e.best_rmse?.toFixed(4) ?? 0),
  }));

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6">
      <h3 className="font-semibold text-slate-800 mb-4">RMSE Comparison</h3>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 4, right: 16, bottom: 4, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
          <XAxis
            dataKey="model"
            tick={{ fill: "#64748b", fontSize: 12 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#64748b", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            domain={[0, "auto"]}
          />
          <Tooltip
            cursor={{ fill: "#f1f5f9" }}
            contentStyle={{
              background: "#fff",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
              fontSize: "13px",
            }}
            formatter={(value) => [value, "RMSE"]}
          />
          <Bar dataKey="rmse" radius={[6, 6, 0, 0]} maxBarSize={80}>
            {data.map((entry) => (
              <Cell key={entry.model} fill={modelColor(entry.model)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
      <div className="bg-slate-50 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
        <Award size={32} className="text-slate-400" />
      </div>
      <h3 className="font-semibold text-slate-700 mb-2">No tuning results yet</h3>
      <p className="text-slate-500 text-sm">
        Run a hyperparameter tuning job to populate the leaderboard.
      </p>
    </div>
  );
}

function ErrorBanner({ message }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 text-sm mb-4">
      ⚠️ {message}
    </div>
  );
}

export default function ModelLeaderboard() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  async function fetchLeaderboard() {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(API_URL);
      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }
      const data = await res.json();
      setEntries(data);
    } catch (err) {
      setError(err.message ?? "Failed to load leaderboard.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const best = entries[0] ?? null;
  const bestRmse = best ? fmt(best.best_rmse) : "—";
  const bestMae = best ? fmt(best.best_mae) : "—";
  const bestR2 = best ? fmt(best.best_r2) : "—";

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Model Leaderboard</h1>
          <p className="text-slate-500 mt-1">Compare ML model performance across all tuning runs</p>
        </div>
        <button
          onClick={fetchLeaderboard}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-200 disabled:opacity-50 transition-colors"
        >
          <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
          {loading ? "Loading..." : "Refresh"}
        </button>
      </div>

      {/* Error */}
      {error && <ErrorBanner message={error} />}

      {/* Loading */}
      {loading && (
        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
          <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full mx-auto mb-4" />
          <p className="text-slate-500 text-sm">Loading leaderboard...</p>
        </div>
      )}

      {/* Content */}
      {!loading && !error && entries.length === 0 && <EmptyState />}

      {!loading && !error && entries.length > 0 && (
        <>
          {/* KPI Row */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatCard
              label="Best RMSE"
              value={bestRmse}
              icon={TrendingDown}
              color="indigo"
            />
            <StatCard
              label="Best MAE"
              value={bestMae}
              icon={Target}
              color="amber"
            />
            <StatCard
              label="Best R²"
              value={bestR2}
              icon={Award}
              color="green"
            />
            <StatCard
              label="Total Models"
              value={entries.length}
              icon={Layers}
              color="violet"
            />
          </div>

          {/* Best Model Card */}
          <BestModelCard entry={best} />

          {/* Leaderboard Table */}
          <LeaderboardTable entries={entries} />

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <RmseBarChart entries={entries} />
          </div>
        </>
      )}
    </div>
  );
}