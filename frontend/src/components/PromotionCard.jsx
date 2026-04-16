export default function PromotionCard() {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h3 className="font-semibold mb-3">Best Promotion</h3>

      <p className="text-lg font-bold text-indigo-600">
        10% Discount
      </p>

      <p className="text-sm mt-2">Expected Revenue Lift</p>
      <p className="text-xl font-bold text-green-600">+18%</p>

      <p className="text-xs text-gray-400 mt-2">
        Compared across discount & bundle options
      </p>
    </div>
  );
}
