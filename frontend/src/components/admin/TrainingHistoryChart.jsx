import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

export default function TrainingHistoryChart({ history, title }) {
  if (!history || history.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-800 mb-4">{title || "Training History"}</h3>
        <div className="h-64 flex items-center justify-center text-slate-400">No training history available</div>
      </div>
    );
  }

  const data = history.map((h) => ({
    epoch: h.epoch,
    "Train Loss": Number(h.loss),
    "Val Loss": Number(h.val_loss),
  }));

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5">
      <h3 className="font-semibold text-slate-800 mb-4">{title || "Training History"}</h3>
      <LineChart width={500} height={260} data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis dataKey="epoch" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => v.toFixed(3)} />
        <Tooltip formatter={(v) => Number(v).toFixed(4)} />
        <Legend />
        <Line type="monotone" dataKey="Train Loss" stroke="#6366f1" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="Val Loss" stroke="#ef4444" dot={false} strokeWidth={2} strokeDasharray="5 5" />
      </LineChart>
    </div>
  );
}