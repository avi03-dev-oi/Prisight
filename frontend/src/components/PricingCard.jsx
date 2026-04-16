export default function PricingCard() {
  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h3 className="font-semibold mb-3">Price Recommendation</h3>

      <p className="text-sm text-gray-500">Current Price</p>
      <p className="text-xl font-bold">₹499</p>

      <p className="text-sm text-gray-500 mt-3">Recommended Price</p>
      <p className="text-2xl font-bold text-green-600">₹529</p>

      <p className="text-xs text-gray-400 mt-2">
        Based on revenue maximization
      </p>
    </div>
  );
}
