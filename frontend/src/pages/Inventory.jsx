import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

export default function Inventory() {
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState("");
  const [forecast, setForecast] = useState(null);
  const [nlp, setNlp] = useState(null);
  const [loading, setLoading] = useState(false);

  /* Load products */
  useEffect(() => {
    axios.get("http://localhost:8000/products/all").then((res) => {
      setProducts(res.data.detail || []);
      if (res.data.detail?.length) {
        setProductId(res.data.detail[0].id);
      }
    });
  }, []);

  const analyzeInventory = async () => {
    if (!productId) return;
    setLoading(true);

    try {
      const forecastRes = await axios.post(
        `http://localhost:8000/forecast/predict/${productId}?days=7`
      );
      setForecast(forecastRes.data);

      const nlpRes = await axios.post(
        `http://localhost:8000/nlp/explain/forecast/${productId}`
      );
      setNlp(nlpRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Inventory Intelligence</h1>

      {/* Product selector */}
      <div className="flex gap-4">
        <select
          className="border px-4 py-2 rounded w-96"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        >
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} (#{p.id})
            </option>
          ))}
        </select>

        <button
          onClick={analyzeInventory}
          className="bg-blue-600 text-white px-6 py-2 rounded"
        >
          Analyze Inventory
        </button>
      </div>

      {loading && <p className="text-gray-500">Analyzing demand forecast...</p>}

      {/* FORECAST LINE GRAPH */}
      {forecast && (
        <div className="bg-white p-6 rounded shadow">
          <h2 className="font-semibold mb-4">7-Day Demand Forecast</h2>

          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={forecast.daily_forecast}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="predicted_units"
                stroke="#2563eb"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* KPI ROW */}
      {forecast && (
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Forecast Period</p>
            <p className="font-bold text-lg">{forecast.forecast_days} Days</p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Total Predicted Demand</p>
            <p className="font-bold text-lg">
              {forecast.total_predicted_units} Units
            </p>
          </div>

          {nlp && (
            <div
              className={`p-4 rounded shadow ${
                nlp.reorder_now
                  ? "bg-red-50 border border-red-300"
                  : "bg-green-50 border border-green-300"
              }`}
            >
              <p className="text-sm text-gray-500">Reorder Status</p>
              <p
                className={`font-bold text-lg ${
                  nlp.reorder_now ? "text-red-600" : "text-green-600"
                }`}
              >
                {nlp.reorder_now ? "Reorder Required" : "Stock OK"}
              </p>
            </div>
          )}
        </div>
      )}

      {/* NLP EXPLANATION */}
      {nlp && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
          <h3 className="font-semibold mb-2">AI Explanation</h3>
          <p>{nlp.explanation}</p>
        </div>
      )}
    </div>
  );
}
