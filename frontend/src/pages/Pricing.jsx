import { useEffect, useState } from "react";
import axios from "axios";
import PricingPieChart from "../components/pricing/PricingPieChart";

export default function Pricing() {
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState("");
  const [result, setResult] = useState(null);
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get("http://localhost:8000/products/all").then((res) => {
      setProducts(res.data.detail || []);
    });
  }, []);

  const analyzePricing = async () => {
    if (!productId) {
      alert("Select a product");
      return;
    }

    try {
      setLoading(true);

      const elasticityRes = await axios.post(
        `http://localhost:8000/elasticity/elasticity/calculate/${productId}`
      );

      const pricingRes = await axios.post(
        `http://localhost:8000/pricing/recommend/${productId}`
      );

      const nlpRes = await axios.post(
        `http://localhost:8000/nlp/explain/pricing/${productId}`
      );

      setResult({
        ...pricingRes.data,
        elasticity: elasticityRes.data.elasticity,
        interpretation: elasticityRes.data.interpretation,
      });

      setExplanation(nlpRes.data.explanation);
    } catch (err) {
      console.error(err);
      alert("Pricing analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Pricing Intelligence</h1>

      {/* Product Selector */}
      <div className="flex gap-4 items-center">
        <select
          className="border p-2 rounded w-96"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        >
          <option value="">Select Product</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} (#{p.id})
            </option>
          ))}
        </select>

        <button
          onClick={analyzePricing}
          disabled={loading}
          className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze Pricing"}
        </button>
      </div>

      {/* Results */}
      {result && (
        <>
          {/* PIE CHART */}
          <PricingPieChart data={result} />

          {/* PRICE CARDS */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded shadow">
              <p className="text-gray-500">Current Price</p>
              <p className="text-xl font-bold">₹{result.current_price}</p>
            </div>

            <div className="bg-white p-4 rounded shadow">
              <p className="text-gray-500">Market Avg Price</p>
              <p className="text-xl font-bold">₹{result.market_avg_price}</p>
            </div>

            <div className="bg-white p-4 rounded shadow">
              <p className="text-gray-500">Recommended Price</p>
              <p className="text-xl font-bold text-green-600">
                ₹{result.recommended_price}
              </p>
            </div>
          </div>

          {/* NLP + ELASTICITY */}
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-5 rounded">
            <p className="font-semibold text-lg">AI Pricing Insight</p>

            <p className="mt-2">
              <strong>Elasticity:</strong>{" "}
              {result.elasticity.toFixed(2)} —{" "}
              {result.interpretation}
            </p>

            <p className="mt-2 text-gray-700">{explanation}</p>
          </div>
        </>
      )}
    </div>
  );
}
