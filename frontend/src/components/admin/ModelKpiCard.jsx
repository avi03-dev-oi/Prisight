export default function ModelKpiCard({ title, value, suffix = "", trend, icon: Icon, color = "indigo" }) {
  const colorClasses = {
    indigo: "bg-indigo-50 border-indigo-100 text-indigo-600",
    green: "bg-emerald-50 border-emerald-100 text-emerald-600",
    amber: "bg-amber-50 border-amber-100 text-amber-600",
    rose: "bg-rose-50 border-rose-100 text-rose-600",
    violet: "bg-violet-50 border-violet-100 text-violet-600",
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 hover:shadow-md transition-all duration-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
          <p className="text-2xl font-bold text-slate-900">
            {typeof value === "number" ? value.toFixed(4) : value}
            {suffix && <span className="text-sm font-normal text-slate-400 ml-1">{suffix}</span>}
          </p>
          {trend && (
            <p className={`text-xs mt-1 ${trend >= 0 ? "text-emerald-600" : "text-rose-600"}`}>
              {trend >= 0 ? "↑" : "↓"} {Math.abs(trend)}% vs last
            </p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-lg ${colorClasses[color] || colorClasses.indigo}`}>
            <Icon size={24} />
          </div>
        )}
      </div>
    </div>
  );
}