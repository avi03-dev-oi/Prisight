export default function ModelComparisonTable({ models, metrics }) {
  const sortedModels = [...models].sort((a, b) => (metrics[a]?.rmse || 0) - (metrics[b]?.rmse || 0));

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100">
        <h3 className="font-semibold text-slate-800">Model Comparison</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-5 py-3 text-left font-medium text-slate-500">Model</th>
              <th className="px-5 py-3 text-right font-medium text-slate-500">RMSE</th>
              <th className="px-5 py-3 text-right font-medium text-slate-500">MAE</th>
              <th className="px-5 py-3 text-right font-medium text-slate-500">R²</th>
              <th className="px-5 py-3 text-right font-medium text-slate-500">MAPE</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {sortedModels.map((model, idx) => {
              const m = metrics[model] || {};
              const isBest = idx === 0;
              return (
                <tr key={model} className="hover:bg-slate-50 transition-colors">
                  <td className="px-5 py-3">
                    <span className="font-medium text-slate-900">{model}</span>
                    {isBest && (
                      <span className="ml-2 px-2 py-0.5 text-xs bg-emerald-100 text-emerald-700 rounded-full">
                        Best
                      </span>
                    )}
                  </td>
                  <td className="px-5 py-3 text-right text-slate-600">{m.rmse?.toFixed(4) || "-"}</td>
                  <td className="px-5 py-3 text-right text-slate-600">{m.mae?.toFixed(4) || "-"}</td>
                  <td className="px-5 py-3 text-right text-slate-600">{m.r2_score?.toFixed(4) || "-"}</td>
                  <td className="px-5 py-3 text-right text-slate-600">{m.mape?.toFixed(2) || "-"}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}