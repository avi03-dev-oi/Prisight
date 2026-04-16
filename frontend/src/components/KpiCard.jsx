export default function KpiCard({ title, value, subtitle }) {
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <p className="text-sm text-gray-500">{title}</p>
      <h2 className="text-2xl font-bold mt-1">{value}</h2>
      <p className="text-xs text-gray-400 mt-1">{subtitle}</p>
    </div>
  );
}
