import { useState } from "react";

import ProductModal from "./components/products/ProductModal";
import ProductTable from "./components/products/ProductTable";
import SalesUploadModal from "./components/sales/SalesUploadModal";
import SalesChart from "./components/sales/SalesChart";
import MarketModal from "./components/market/MarketModal";

export default function Dashboard() {
  const [add, setAdd] = useState(false);
  const [list, setList] = useState(false);
  const [salesModal, setSalesModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [marketModal, setMarketModal] = useState(false);

  return (
    <div className="space-y-6">
      
      {/* ACTION BUTTONS */}
      <div className="flex gap-3">
        <button
          onClick={() => setAdd(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Add Product
        </button>

        <button
          onClick={() => setList(true)}
          className="border px-4 py-2 rounded"
        >
          View Products
        </button>

        <button
          onClick={() => setSalesModal(true)}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Upload Sales
        </button>

        <button
          onClick={() => setMarketModal(true)}
          className="bg-purple-600 text-white px-4 py-2 rounded"
        >
          Market Data
        </button>
      </div>

      {/* SALES CHART */}
      {selectedProduct && (
        <SalesChart productId={selectedProduct} />
      )}

      {/* MODALS */}
      {add && <ProductModal onClose={() => setAdd(false)} refresh={() => {}} />}

      {list && (
        <ProductTable
          onClose={() => setList(false)}
          onSelectProduct={(id) => {
            setSelectedProduct(id);
            setList(false);
          }}
        />
      )}

      {salesModal && (
        <SalesUploadModal onClose={() => setSalesModal(false)} />
      )}

      {marketModal && (
        <MarketModal onClose={() => setMarketModal(false)} />
      )}
    </div>
  );
}
