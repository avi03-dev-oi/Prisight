import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

export default function ActualVsPredictedChart({ predictions, title }) {
  if (!predictions || predictions.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-5">
        <h3 className="font-semibold text-slate-800 mb-4">{title || "Actual vs Predicted"}</h3>
        <div className="h-64 flex items-center justify-center text-slate-400">No prediction data available</div>
      </div>
    );
  }

  const data = predictions.map((p) => ({
    timestep: p.timestep,
    Actual: Number(p.actual_value),
    Predicted: Number(p.predicted_value),
  }));

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5">
      <h3 className="font-semibold text-slate-800 mb-4">{title || "Actual vs Predicted"}</h3>
      <LineChart width={500} height={260} data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis dataKey="timestep" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="Actual" stroke="#6366f1" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="Predicted" stroke="#f59e0b" dot={false} strokeWidth={2} strokeDasharray="5 5" />
      </LineChart>
    </div>
  );
}