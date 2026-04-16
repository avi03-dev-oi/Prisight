import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function SalesChart({ productId }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (!productId) return;

    axios
      .get(`http://localhost:8000/sales/product_sales/${productId}`)
      .then((res) => setData(res.data))
      .catch(() => setData([]));
  }, [productId]);

  if (!productId) {
    return (
      <div className="bg-white p-6 rounded shadow text-gray-500">
        Select a product to view sales
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded shadow h-96">
      <h3 className="text-lg font-semibold mb-4">Sales Trend</h3>

      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="units_sold"
            stroke="#2563eb"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
