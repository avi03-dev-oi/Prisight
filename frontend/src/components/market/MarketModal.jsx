import { useState } from "react";
import axios from "axios";

export default function MarketModal({ onClose }) {
  const [file, setFile] = useState(null);
  const [productName, setProductName] = useState("");
  const [stats, setStats] = useState(null);

  const uploadMarketData = async () => {
    if (!file) return alert("Select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    await axios.post("http://localhost:8000/market/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    alert("Market data uploaded");
  };

  const fetchStats = async () => {
    if (!productName) return;

    const res = await axios.get(
      `http://localhost:8000/market/stats/${productName}`
    );
    setStats(res.data);
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white w-150 rounded-lg p-6 relative space-y-4">
        <button
          className="absolute top-3 right-3 text-red-500 text-xl"
          onClick={onClose}
        >
          ✕
        </button>

        <h2 className="text-xl font-semibold">Market Data</h2>

        {/* Upload */}
        <div className="border p-4 rounded space-y-2">
          <h3 className="font-medium">Upload Market CSV</h3>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button
            onClick={uploadMarketData}
            className="bg-green-600 text-white px-3 py-1 rounded"
          >
            Upload
          </button>
        </div>

        {/* Stats */}
        <div className="border p-4 rounded space-y-2">
          <h3 className="font-medium">Market Statistics</h3>

          <input
            className="border p-2 w-full rounded"
            placeholder="Product name (exact match)"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
          />

          <button
            onClick={fetchStats}
            className="bg-blue-600 text-white px-3 py-1 rounded"
          >
            Fetch Stats
          </button>

          {stats && (
            <div className="mt-3 text-sm space-y-1">
              <p>Average Price: ₹{stats.avg_price}</p>
              <p>Min Price: ₹{stats.min_price}</p>
              <p>Max Price: ₹{stats.max_price}</p>
              <p>Total Sellers: {stats.total_sellers}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
