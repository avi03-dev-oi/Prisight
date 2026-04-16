import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

export default function Promotions() {
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState("");
  const [promoData, setPromoData] = useState(null);
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

  const analyzePromotion = async () => {
    if (!productId) return;
    setLoading(true);

    try {
      const promoRes = await axios.post(
        `http://localhost:8000/promotions/recommend/${productId}`
      );
      setPromoData(promoRes.data);

      const nlpRes = await axios.post(
        `http://localhost:8000/nlp/explain/promotion/${productId}`
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
      <h1 className="text-2xl font-bold">Promotion Intelligence</h1>

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
          onClick={analyzePromotion}
          className="bg-blue-600 text-white px-6 py-2 rounded"
        >
          Analyze Promotions
        </button>
      </div>

      {loading && <p className="text-gray-500">Analyzing promotions...</p>}

      {/* BAR CHART */}
      {promoData && (
        <div className="bg-white p-6 rounded shadow">
          <h2 className="font-semibold mb-4">Revenue Comparison</h2>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={promoData.all_simulations}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="promotion" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="revenue" fill="#2563eb" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* BEST PROMOTION */}
      {promoData && (
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Best Promotion</p>
            <p className="font-bold text-lg">{promoData.best_promotion}</p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Discount</p>
            <p className="font-bold text-lg">
              {promoData.discount_percent}%
            </p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Expected Units Sold</p>
            <p className="font-bold text-lg">
              {promoData.expected_units_sold}
            </p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <p className="text-sm text-gray-500">Expected Revenue</p>
            <p className="font-bold text-green-600 text-lg">
              ₹{promoData.expected_revenue.toLocaleString()}
            </p>
          </div>
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
