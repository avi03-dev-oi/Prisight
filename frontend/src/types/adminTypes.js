export const evaluationShape = {
  id: null,
  model_name: "",
  dataset_name: "",
  rmse: 0,
  mae: 0,
  r2_score: 0,
  mape: 0,
  created_at: "",
  training_history: null,
};

export const predictionShape = {
  id: null,
  actual: 0,
  predicted: 0,
  residual: 0,
};

export const kpiShape = {
  bestRmse: 0,
  bestMae: 0,
  bestR2: 0,
  totalEvaluations: 0,
};

export const modelComparisonShape = {
  models: [],
  metrics: {},
};