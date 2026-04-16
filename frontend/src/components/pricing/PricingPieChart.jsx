import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function PricingPieChart({ data }) {
  if (!data) return null;

  const chartData = [
    { name: "Current Price", value: data.current_price },
    { name: "Market Avg Price", value: data.market_avg_price },
    { name: "Recommended Price", value: data.recommended_price },
  ];

  const COLORS = ["#2563eb", "#f59e0b", "#16a34a"];

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-lg font-semibold mb-4">Price Distribution</h2>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            outerRadius={110}
            label
          >
            {chartData.map((_, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
