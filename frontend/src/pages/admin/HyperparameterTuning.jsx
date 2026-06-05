// frontend/src/pages/admin/HyperparameterTuning.jsx
import { useState, useEffect, useRef } from "react";
import { Play, Square, RefreshCw, ChevronDown, ChevronUp, Trophy, Clock, TrendingDown } from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, BarChart, Bar, ResponsiveContainer,
} from "recharts";

const API = "http://localhost:8000";
const HEADERS = {
  "Content-Type": "application/json",
  "X-Admin-Token": localStorage.getItem("admin_token") || "",
};

async function apiFetch(path, method = "GET", body = null) {
  const res = await fetch(API + path, {
    method,
    headers: HEADERS,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── Sub-components ────────────────────────────────────────────────────────────

function StatCard({ label, value, sub, icon: Icon, color = "indigo" }) {
  const colors = {
    indigo: "bg-indigo-50 text-indigo-600 border-indigo-100",
    green:  "bg-emerald-50 text-emerald-600 border-emerald-100",
    amber:  "bg-amber-50 text-amber-600 border-amber-100",
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
        {sub && <p className="text-xs opacity-60">{sub}</p>}
      </div>
    </div>
  );
}

function ProgressBar({ value, status }) {
  const color = status === "completed" ? "bg-emerald-500"
              : status === "failed"    ? "bg-red-500"
              : status === "cancelled" ? "bg-slate-400"
              : "bg-indigo-500";
  return (
    <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
      <div
        className={`h-2 rounded-full transition-all duration-500 ${color} ${
          status === "running" ? "animate-pulse" : ""
        }`}
        style={{ width: `${value}%` }}
      />
    </div>
  );
}

function ParamBadge({ k, v }) {
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 text-xs font-mono">
      <span className="text-indigo-500">{k}</span>
      <span>=</span>
      <span>{typeof v === "number" ? (Number.isInteger(v) ? v : v.toFixed(4)) : v}</span>
    </span>
  );
}

function TrialRow({ trial, isBest }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`border rounded-lg mb-1 overflow-hidden transition-all ${isBest ? "border-indigo-300 bg-indigo-50/40" : "border-slate-200 bg-white"}`}>
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-4 py-2 text-sm hover:bg-slate-50"
      >
        <div className="flex items-center gap-3">
          {isBest && <Trophy size={14} className="text-amber-500" />}
          <span className="font-medium text-slate-700">Trial #{trial.trial_number + 1}</span>
          <span className="text-slate-400">RMSE: <span className="font-semibold text-slate-700">{trial.rmse}</span></span>
          <span className="text-slate-400">MAE: <span className="font-semibold text-slate-700">{trial.mae}</span></span>
          <span className="text-slate-400">R²: <span className="font-semibold text-slate-700">{trial.r2}</span></span>
        </div>
        {open ? <ChevronUp size={14} className="text-slate-400" /> : <ChevronDown size={14} className="text-slate-400" />}
      </button>
      {open && (
        <div className="px-4 pb-3 flex flex-wrap gap-2">
          {Object.entries(trial.params).map(([k, v]) => (
            <ParamBadge key={k} k={k} v={v} />
          ))}
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
export default function HyperparameterTuning() {
  const [modelType,  setModelType]  = useState("transformer");
  const [productId,  setProductId]  = useState(1);
  const [nTrials,    setNTrials]    = useState(20);
  const [activeJob,  setActiveJob]  = useState(null);   // job details object
  const [allJobs,    setAllJobs]    = useState([]);
  const [error,      setError]      = useState("");
  const [starting,   setStarting]   = useState(false);
  const pollRef = useRef(null);

  // ── Poll active job ───────────────────────────────────────────────────────
  useEffect(() => {
    if (activeJob && ["running"].includes(activeJob.status)) {
      pollRef.current = setInterval(async () => {
        try {
          const data = await apiFetch(`/api/admin/tuning/jobs/${activeJob.job_id}`);
          setActiveJob(data);
          if (data.status !== "running") clearInterval(pollRef.current);
        } catch {
          clearInterval(pollRef.current);
        }
      }, 2000);
    }
    return () => clearInterval(pollRef.current);
  }, [activeJob?.job_id, activeJob?.status]);

  // ── Fetch job history on mount ────────────────────────────────────────────
  useEffect(() => {
    apiFetch("/api/admin/tuning/jobs")
      .then(d => setAllJobs(d.jobs || []))
      .catch(() => {});
  }, []);

  // ── Start tuning ──────────────────────────────────────────────────────────
  const handleStart = async () => {
    setError("");
    setStarting(true);
    try {
      const res = await apiFetch("/api/admin/tuning/start", "POST", {
        model_type: modelType,
        product_id: productId,
        n_trials:   nTrials,
      });
      const jobData = await apiFetch(`/api/admin/tuning/jobs/${res.job_id}`);
      setActiveJob(jobData);
    } catch (e) {
      setError(e.message);
    } finally {
      setStarting(false);
    }
  };

  // ── Cancel ────────────────────────────────────────────────────────────────
  const handleCancel = async () => {
    if (!activeJob) return;
    await apiFetch(`/api/admin/tuning/jobs/${activeJob.job_id}`, "DELETE").catch(() => {});
    setActiveJob(j => ({ ...j, status: "cancelled" }));
  };

  // ── Chart data ────────────────────────────────────────────────────────────
  const trialChartData = (activeJob?.trials || []).map(t => ({
    trial: t.trial_number + 1,
    RMSE:  t.rmse,
    MAE:   t.mae,
  }));

  const paramChartData = activeJob?.trials?.length > 0
    ? Object.entries(
        activeJob.trials.reduce((acc, t) => {
          const lr = parseFloat(t.params.learning_rate || 0).toFixed(4);
          if (!acc[lr]) acc[lr] = { lr, count: 0, bestRmse: Infinity };
          acc[lr].count++;
          if (t.rmse < acc[lr].bestRmse) acc[lr].bestRmse = t.rmse;
          return acc;
        }, {})
      ).map(([lr, v]) => ({ lr, ...v }))
    : [];

  const isRunning = activeJob?.status === "running";

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Hyperparameter Tuning</h1>
          <p className="text-slate-500 mt-1">Auto-tune LSTM, GRU, and Transformer with Optuna</p>
        </div>
        <button
          onClick={() => apiFetch("/api/admin/tuning/jobs").then(d => setAllJobs(d.jobs || []))}
          className="flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-200"
        >
          <RefreshCw size={14} /> Refresh Jobs
        </button>
      </div>

      {/* Config + Launch */}
      <div className="bg-white rounded-xl border border-slate-200 p-6">
        <h2 className="font-semibold text-slate-800 mb-4">Configure Tuning Run</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
          {/* Model Type */}
          <div>
            <label className="text-sm font-medium text-slate-600 mb-1 block">Model</label>
            <select
              value={modelType}
              onChange={e => setModelType(e.target.value)}
              disabled={isRunning}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            >
              <option value="transformer">Transformer</option>
              <option value="lstm">LSTM</option>
              <option value="gru">GRU</option>
            </select>
          </div>

          {/* Product ID */}
          <div>
            <label className="text-sm font-medium text-slate-600 mb-1 block">Product ID</label>
            <input
              type="number" min={1} max={100}
              value={productId}
              onChange={e => setProductId(parseInt(e.target.value))}
              disabled={isRunning}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>

          {/* N Trials */}
          <div>
            <label className="text-sm font-medium text-slate-600 mb-1 block">
              Trials: <span className="text-indigo-600 font-semibold">{nTrials}</span>
            </label>
            <input
              type="range" min={5} max={50} step={5}
              value={nTrials}
              onChange={e => setNTrials(parseInt(e.target.value))}
              disabled={isRunning}
              className="w-full accent-indigo-600"
            />
            <div className="flex justify-between text-xs text-slate-400 mt-0.5">
              <span>5 (fast)</span><span>50 (thorough)</span>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">{error}</div>
        )}

        <div className="flex gap-3">
          <button
            onClick={handleStart}
            disabled={isRunning || starting}
            className="flex items-center gap-2 px-5 py-2.5 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            <Play size={16} />
            {starting ? "Starting..." : "Start Tuning"}
          </button>
          {isRunning && (
            <button
              onClick={handleCancel}
              className="flex items-center gap-2 px-5 py-2.5 bg-red-500 text-white text-sm font-medium rounded-lg hover:bg-red-600"
            >
              <Square size={16} /> Cancel
            </button>
          )}
        </div>
      </div>

      {/* Active Job */}
      {activeJob && (
        <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-semibold text-slate-800">
                {activeJob.model_type?.toUpperCase()} — Job <span className="font-mono text-indigo-600">{activeJob.job_id}</span>
              </h2>
              <p className="text-sm text-slate-500 mt-0.5">
                Status: <span className={`font-medium ${
                  activeJob.status === "completed" ? "text-emerald-600"
                  : activeJob.status === "failed"   ? "text-red-600"
                  : activeJob.status === "cancelled"? "text-slate-500"
                  : "text-indigo-600"
                }`}>{activeJob.status}</span>
                {activeJob.started_at && (
                  <span className="ml-3 text-slate-400">
                    Started {new Date(activeJob.started_at).toLocaleTimeString()}
                  </span>
                )}
              </p>
            </div>
            <span className="text-2xl font-bold text-slate-700">
              {activeJob.progress}%
            </span>
          </div>

          <ProgressBar value={activeJob.progress} status={activeJob.status} />

          {/* KPI row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <StatCard label="Best RMSE"     value={activeJob.best_value}            icon={TrendingDown} color="indigo" />
            <StatCard label="Trials Done"   value={activeJob.trials?.length ?? 0}   icon={RefreshCw}    color="violet"
              sub={`of ${activeJob.n_trials}`} />
            <StatCard label="Best Model"    value={activeJob.model_type?.toUpperCase()} icon={Trophy}    color="amber" />
            <StatCard label="Finished"      value={activeJob.finished_at
              ? new Date(activeJob.finished_at).toLocaleTimeString() : "—"}
              icon={Clock} color="green" />
          </div>

          {/* Best params */}
          {activeJob.best_params && (
            <div>
              <p className="text-sm font-medium text-slate-700 mb-2">Best Hyperparameters</p>
              <div className="flex flex-wrap gap-2">
                {Object.entries(activeJob.best_params).map(([k, v]) => (
                  <ParamBadge key={k} k={k} v={v} />
                ))}
              </div>
            </div>
          )}

          {/* RMSE over trials chart */}
          {trialChartData.length > 1 && (
            <div>
              <p className="text-sm font-medium text-slate-700 mb-2">RMSE per Trial</p>
              <LineChart width={700} height={220} data={trialChartData}
                margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="trial" tick={{ fontSize: 11 }} label={{ value: "Trial", position: "insideBottom", offset: -2 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="RMSE" stroke="#6366f1" dot={false} strokeWidth={2} />
                <Line type="monotone" dataKey="MAE"  stroke="#f59e0b" dot={false} strokeWidth={2} strokeDasharray="4 4" />
              </LineChart>
            </div>
          )}

          {/* Trial list */}
          {activeJob.trials?.length > 0 && (
            <div>
              <p className="text-sm font-medium text-slate-700 mb-2">
                All Trials ({activeJob.trials.length})
              </p>
              <div className="max-h-80 overflow-y-auto pr-1">
                {[...activeJob.trials]
                  .sort((a, b) => a.rmse - b.rmse)
                  .map(t => (
                    <TrialRow
                      key={t.trial_number}
                      trial={t}
                      isBest={t.rmse === activeJob.best_value}
                    />
                  ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Past Jobs */}
      {allJobs.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 p-6">
          <h2 className="font-semibold text-slate-800 mb-4">Past Tuning Jobs</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500 border-b border-slate-100">
                  <th className="pb-2 pr-4">Job ID</th>
                  <th className="pb-2 pr-4">Model</th>
                  <th className="pb-2 pr-4">Status</th>
                  <th className="pb-2 pr-4">Trials</th>
                  <th className="pb-2 pr-4">Best RMSE</th>
                  <th className="pb-2">Started</th>
                </tr>
              </thead>
              <tbody>
                {allJobs.map(j => (
                  <tr
                    key={j.job_id}
                    onClick={() => apiFetch(`/api/admin/tuning/jobs/${j.job_id}`).then(setActiveJob)}
                    className="border-b border-slate-50 hover:bg-slate-50 cursor-pointer"
                  >
                    <td className="py-2 pr-4 font-mono text-indigo-600">{j.job_id}</td>
                    <td className="py-2 pr-4 font-medium">{j.model_type?.toUpperCase()}</td>
                    <td className="py-2 pr-4">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        j.status === "completed" ? "bg-emerald-100 text-emerald-700"
                        : j.status === "failed"   ? "bg-red-100 text-red-700"
                        : j.status === "running"  ? "bg-indigo-100 text-indigo-700"
                        : "bg-slate-100 text-slate-600"
                      }`}>
                        {j.status}
                      </span>
                    </td>
                    <td className="py-2 pr-4">{j.n_trials}</td>
                    <td className="py-2 pr-4 font-semibold">{j.best_value ?? "—"}</td>
                    <td className="py-2 text-slate-400">
                      {j.started_at ? new Date(j.started_at).toLocaleTimeString() : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}