export default function InventoryCard() {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h3 className="font-semibold mb-3">Inventory Advisor</h3>

      <p className="text-sm">Days Until Stockout</p>
      <p className="text-2xl font-bold text-red-500">6 Days</p>

      <p className="text-sm mt-3">Recommended Reorder Qty</p>
      <p className="text-xl font-bold">320 Units</p>

      <p className="text-xs text-gray-400 mt-2">
        Includes safety stock
      </p>
    </div>
  );
}
