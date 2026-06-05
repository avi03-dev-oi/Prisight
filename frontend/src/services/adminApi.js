// Custom fetch wrapper that always sends the admin token header
const adminFetch = async (url, method = "GET", body = null) => {
  const token = localStorage.getItem("admin_token") || "";

  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Token": token,          // ✅ required by require_admin guard
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(url, options);

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `API error: ${res.status}`);
  }

  return res.json();
};

export const adminApi = {
  // Evaluations
  getEvaluations: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return adminFetch(`/api/admin/evaluations${query ? `?${query}` : ""}`);
  },
  getEvaluationDetail: (id) =>
    adminFetch(`/api/admin/evaluations/${id}`),

  // Comparison & history
  getModelComparison: () =>
    adminFetch("/api/admin/model-comparison"),
  getModelHistory: (modelName) =>
    adminFetch(`/api/admin/model-history/${modelName}`),

  // Predictions & training
  getPredictions: (evaluationId) =>
    adminFetch(`/api/admin/predictions/${evaluationId}`),
  getTrainingHistory: (evaluationId) =>
    adminFetch(`/api/admin/training-history/${evaluationId}`),

  // Names for filter dropdowns
  getModelNames: () =>
    adminFetch("/api/admin/model-names"),
  getDatasetNames: () =>
    adminFetch("/api/admin/dataset-names"),

  // Stats
  getStatsSummary: () =>
    adminFetch("/api/admin/stats/summary"),

  // Create / import
  importEvaluation: (data) =>
    adminFetch("/api/admin/evaluations", "POST", data),
  importEvaluationWithData: (data) =>
    adminFetch("/api/admin/evaluations/with-data", "POST", data),
  bulkImport: (data) =>
    adminFetch("/api/admin/bulk-import", "POST", data),

  // Delete
  deleteEvaluation: (id) =>
    adminFetch(`/api/admin/evaluations/${id}`, "DELETE"),
};