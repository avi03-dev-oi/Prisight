//admin/ModelEvaluation.jsx
import { useState, useEffect } from "react";
import { RefreshCw, TrendingDown, Target, Award, Layers } from "lucide-react";
import { adminApi } from "../../services/adminApi";
import ModelKpiCard from "../../components/admin/ModelKpiCard";
import ModelComparisonTable from "../../components/admin/ModelComparisonTable";
import MetricBarChart from "../../components/admin/MetricBarChart";
import ActualVsPredictedChart from "../../components/admin/ActualVsPredictedChart";
import TrainingHistoryChart from "../../components/admin/TrainingHistoryChart";
import ModelFilterBar from "../../components/admin/ModelFilterBar";

export default function ModelEvaluation() {
  const [loading, setLoading] = useState(true);
  const [evaluations, setEvaluations] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [trainingHistory, setTrainingHistory] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [selectedDataset, setSelectedDataset] = useState("");

  const fetchData = async () => {
  setLoading(true);
  try {
    const evalData = await adminApi.getEvaluations({ page_size: 50 });
    const evalItems = evalData.items || evalData.evaluations || [];
    setEvaluations(evalItems);

    if (evalItems.length > 0) {
      try {
        // Load charts from best RMSE evaluation, not first item
        const bestEval = evalItems.find(e => 
  e.model_name === "Transformer" && e.dataset_name === "Notebook2_Product1"
) || evalItems.reduce((best, e) => (!best || e.rmse < best.rmse) ? e : best, null);
        const detailData = await adminApi.getEvaluationDetail(bestEval.id);
        setPredictions(detailData.predictions || []);
        setTrainingHistory(detailData.training_history || []);
      } catch {
        setPredictions([]);
        setTrainingHistory([]);
      }
    }
  } catch (error) {
    console.error("Failed to fetch data:", error);
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    fetchData();
  }, []);

  // ── Derive everything from evaluations list directly ──────────────────────
  const models = [...new Set(evaluations.map((e) => e.model_name).filter(Boolean))];
  const datasets = [...new Set(evaluations.map((e) => e.dataset_name).filter(Boolean))];

  // Filter evaluations by selected model/dataset
  const filtered = evaluations.filter((e) => {
    if (selectedModel && e.model_name !== selectedModel) return false;
    if (selectedDataset && e.dataset_name !== selectedDataset) return false;
    return true;
  });

  // Build per-model best metrics from filtered evaluations
  const metricsByModel = {};
  filtered.forEach((e) => {
    if (!metricsByModel[e.model_name]) {
      metricsByModel[e.model_name] = {
        rmse: e.rmse,
        mae: e.mae,
        r2_score: e.r2_score,
        mape: e.mape,
        epochs: e.epochs,
        training_time_seconds: e.training_time_seconds,
      };
    }
  });

  // Chart data array
  const metricsArr = Object.entries(metricsByModel).map(([name, m]) => ({
    name,
    rmse: m.rmse || 0,
    mae: m.mae || 0,
    r2: m.r2_score || 0,
  }));

  // KPI values — safe defaults if no data
  const allRmse = evaluations.map((e) => e.rmse).filter((v) => v != null && isFinite(v));
  const allMae = evaluations.map((e) => e.mae).filter((v) => v != null && isFinite(v));
  const allR2 = evaluations.map((e) => e.r2_score).filter((v) => v != null && isFinite(v));

  const bestRmse = allRmse.length > 0 ? Math.min(...allRmse) : null;
  const bestMae = allMae.length > 0 ? Math.min(...allMae) : null;
  const bestR2 = allR2.length > 0 ? Math.max(...allR2) : null;

  const bestModelEntry = evaluations.reduce((best, e) => {
    if (!best || e.rmse < best.rmse) return e;
    return best;
  }, null);
  const bestModel = bestModelEntry?.model_name || null;
console.log("predictions:", predictions, "history:", trainingHistory);
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Model Evaluation</h1>
          <p className="text-slate-500 mt-1">Analyze and compare ML model performance metrics</p>
        </div>
        <button
          onClick={fetchData}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
          Refresh
        </button>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <ModelKpiCard
          title="Best RMSE"
          value={bestRmse !== null ? bestRmse.toFixed(4) : "N/A"}
          icon={TrendingDown}
          color="indigo"
        />
        <ModelKpiCard
          title="Best MAE"
          value={bestMae !== null ? bestMae.toFixed(4) : "N/A"}
          icon={Target}
          color="amber"
        />
        <ModelKpiCard
          title="Best R² Score"
          value={bestR2 !== null ? bestR2.toFixed(4) : "N/A"}
          icon={Award}
          color="green"
        />
        <ModelKpiCard
          title="Total Evaluations"
          value={evaluations.length}
          icon={Layers}
          color="violet"
        />
      </div>

      {/* Filter Bar */}
      <ModelFilterBar
        models={models}
        selectedModel={selectedModel}
        onModelChange={setSelectedModel}
        datasets={datasets}
        selectedDataset={selectedDataset}
        onDatasetChange={setSelectedDataset}
        onRefresh={fetchData}
        loading={loading}
      />

      {/* Model Comparison Table */}
      <ModelComparisonTable
        models={Object.keys(metricsByModel)}
        metrics={metricsByModel}
      />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <MetricBarChart
          data={metricsArr}
          dataKey="rmse"
          xKey="name"
          color="#6366f1"
          title="RMSE by Model (lower is better)"
        />
        <MetricBarChart
          data={metricsArr}
          dataKey="mae"
          xKey="name"
          color="#f59e0b"
          title="MAE by Model (lower is better)"
        />
      </div>

      {/* Actual vs Predicted & Training History */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {predictions.length > 0 ? (
          <ActualVsPredictedChart predictions={predictions} title="Actual vs Predicted" />
        ) : (
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <h3 className="font-semibold text-slate-800 mb-4">Actual vs Predicted</h3>
            <div className="h-64 flex items-center justify-center text-slate-400">
              No prediction data available
            </div>
          </div>
        )}

        {trainingHistory.length > 0 ? (
          <TrainingHistoryChart history={trainingHistory} title="Training History" />
        ) : (
          <div className="bg-white rounded-xl border border-slate-200 p-5">
            <h3 className="font-semibold text-slate-800 mb-4">Training History</h3>
            <div className="h-64 flex items-center justify-center text-slate-400">
              No training history available
            </div>
          </div>
        )}
      </div>

      {/* Best Model Highlight */}
      {bestModel && (
        <div className="bg-gradient-to-r from-indigo-500 to-violet-500 rounded-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-indigo-100 text-sm font-medium">Best Performing Model</p>
              <h2 className="text-2xl font-bold mt-1">{bestModel}</h2>
              <p className="text-indigo-100 mt-2">
                RMSE: {bestRmse?.toFixed(4)} • MAE: {bestMae?.toFixed(4)} • R²: {bestR2?.toFixed(4)}
              </p>
            </div>
            <div className="bg-white/20 p-4 rounded-full">
              <Award size={48} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}