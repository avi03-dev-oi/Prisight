import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { day: "Today", demand: 120 },
  { day: "t+1", demand: 135 },
  { day: "t+7", demand: 180 },
  { day: "t+30", demand: 260 },
];

export default function DemandChart() {
  return (
    <div className="bg-white rounded-xl shadow p-8 h-80 outline-none">
      <h3 className="font-semibold mb-2">Demand Forecast</h3>

      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="demand"
            stroke="#6366f1"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
