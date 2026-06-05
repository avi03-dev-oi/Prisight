#!/usr/bin/env python
# coding: utf-8

# # PRISIGHT: Comparative Deep Learning Analysis for Retail Demand Forecasting  
# ## LSTM vs GRU vs 1D CNN-LSTM vs 1D CNN-GRU
# 
# ### Final Year MCA Project Extension and Analytical Study
# 
# **Made By:** Avinandan Bhattacharjee  
# **Program:** MCA 2026, Techno India University  
# **Under the Guidance of:** Dr. Jayanta Datta, Professor Techno India University.
# 
# ---
# 
# # 1. Introduction
# 
# This notebook is an extension and analytical enhancement of the main *Project Prisight* forecasting pipeline.  
# The primary objective of this implementation is to perform a comparative deep learning analysis between:
# 
# - Long Short-Term Memory (LSTM)
# - Gated Recurrent Unit (GRU)
# - 1D CNN + LSTM Hybrid Network
# - 1D CNN + GRU Hybrid Network
# 
# for retail sales demand forecasting using sequential time-series data.
# 
# The notebook evaluates the capability of recurrent and hybrid neural architectures in learning:
# 
# - Seasonal demand behavior
# - Weekly sales patterns
# - Trend continuation
# - Discount-driven fluctuations
# - Sequential forecasting dependencies
# 
# The study also evaluates architectural efficiency, forecasting stability, training behavior, and prediction realism.
# 
# ---
# 
# # 2. Objectives of This Notebook
# 
# The notebook is designed to:
# 
# 1. Extend the forecasting implementation used in Project Prisight
# 2. Compare recurrent neural network architectures
# 3. Evaluate hybrid CNN-RNN approaches
# 4. Analyze model behavior on long sequential sales data
# 5. Study forecasting consistency across architectures
# 6. Compare prediction quality using multiple evaluation metrics
# 7. Generate future demand forecasts using rolling-window prediction
# 
# ---
# 
# # 3. Dataset Overview
# 
# The dataset used in this implementation is a synthetic retail demand dataset generated for sequential forecasting analysis.
# 
# The generated dataset includes:
# 
# - Product-wise sales history
# - Daily demand records
# - Seasonal variations
# - Weekend demand spikes
# - Discount-driven sales influence
# - Price fluctuation behavior
# - Rolling statistical features
# 
# The dataset spans long-term daily observations to support sequence learning.
# 
# ---
# 
# # 4. Major Features Used
# 
# The forecasting models use engineered temporal and business features including:
# 
# | Feature Name | Purpose |
# |---|---|
# | `units_sold` | Target demand variable |
# | `lag_1` | Previous day sales |
# | `lag_7` | Previous week sales |
# | `rolling_avg_7` | Weekly rolling demand average |
# | `price_ratio` | Selling vs market price behavior |
# | `discount_percent` | Promotional effect |
# | `discount_effect` | Elasticity-based demand variation |
# | `is_weekend` | Weekend demand indication |
# | `weekday_sin`, `weekday_cos` | Cyclic weekday representation |
# | `month_sin`, `month_cos` | Cyclic seasonal encoding |
# | `demand_trend` | Rolling sales momentum |
# 
# ---
# 
# # 5. Notebook Structure
# 
# ---
# 
# ## Part 1 — Library Import and Environment Setup
# 
# This section imports all required libraries and initializes the forecasting environment.
# 
# ### Major Libraries Used
# 
# ```python
# numpy
# pandas
# matplotlib
# tensorflow
# keras
# sklearn
# ```
# 
# ### Major Functions Used
# 
# ```python
# train_test_split()
# MinMaxScaler()
# StandardScaler()
# EarlyStopping()
# Sequential()
# ```
# 
# ---
# 
# ## Part 2 — Synthetic Retail Demand Data Generation
# 
# This section generates sequential retail sales data with:
# 
# - seasonality
# - trends
# - discount effects
# - weekend spikes
# - pricing influence
# 
# ### Important Functions
# 
# ```python
# generate_synthetic_sales_data()
# np.sin()
# np.random.normal()
# ```
# 
# ### Purpose
# 
# To create realistic time-series behavior suitable for sequence forecasting.
# 
# ---
# 
# ## Part 3 — Feature Engineering and Sequence Preparation
# 
# This section prepares the dataset for recurrent neural network training.
# 
# ### Operations Performed
# 
# - Lag feature generation
# - Rolling statistics
# - Cyclic encoding
# - Scaling
# - Window sequence generation
# 
# ### Important Functions
# 
# ```python
# create_sequences()
# fit_transform()
# transform()
# ```
# 
# ### Important Parameters
# 
# ```python
# WINDOW_SIZE = 30
# TRAIN_SPLIT = 0.8
# ```
# 
# ---
# 
# ## Part 4 — LSTM Model Implementation
# 
# This section builds and trains the standalone LSTM forecasting architecture.
# 
# ### Architecture Overview
# 
# ```text
# LSTM → Dropout → LSTM → Dense → Dense
# ```
# 
# ### Important Layers Used
# 
# ```python
# LSTM()
# Dropout()
# Dense()
# ```
# 
# ### Training Parameters
# 
# | Parameter | Value |
# |---|---|
# | Optimizer | Adam |
# | Loss Function | MSE |
# | Epochs | 300 |
# | Batch Size | 16 |
# | Validation Split | 0.2 |
# 
# ### Purpose
# 
# To capture long-term sequential dependencies in demand forecasting.
# 
# ---
# 
# ## Part 5 — GRU Model Implementation
# 
# This section implements the GRU-based forecasting network.
# 
# ### Architecture Overview
# 
# ```text
# GRU → Dropout → GRU → Dense → Dense
# ```
# 
# ### Important Layers Used
# 
# ```python
# GRU()
# Dropout()
# Dense()
# ```
# 
# ### Purpose
# 
# To compare GRU efficiency against LSTM in sequential forecasting.
# 
# ---
# 
# ## Part 6 — 1D CNN + LSTM Hybrid Model
# 
# This section introduces convolutional feature extraction before recurrent learning.
# 
# ### Architecture Overview
# 
# ```text
# Conv1D → BatchNormalization → MaxPooling1D
#         → LSTM Stack → Dense Layers
# ```
# 
# ### Important Layers Used
# 
# ```python
# Conv1D()
# BatchNormalization()
# MaxPooling1D()
# LSTM()
# ```
# 
# ### Purpose
# 
# To extract local temporal patterns before long-sequence learning.
# 
# ---
# 
# ## Part 7 — 1D CNN + GRU Hybrid Model
# 
# This section implements the CNN-GRU hybrid forecasting architecture.
# 
# ### Architecture Overview
# 
# ```text
# Conv1D → BatchNormalization → MaxPooling1D
#         → GRU Stack → Dense Layers
# ```
# 
# ### Purpose
# 
# To evaluate lightweight recurrent learning combined with convolutional temporal extraction.
# 
# ---
# 
# ## Part 8 — Model Evaluation and Comparative Analysis
# 
# This section evaluates all four architectures using forecasting metrics and visualization techniques.
# 
# ### Evaluation Metrics Used
# 
# | Metric | Purpose |
# |---|---|
# | RMSE | Measures prediction error magnitude |
# | MAE | Measures average absolute error |
# | R² Score | Measures prediction fit quality |
# | MAPE | Measures percentage forecasting error |
# 
# ### Visualization Performed
# 
# - Actual vs Predicted Curves
# - Residual Analysis
# - Scatter Plots
# - Forecast Overlays
# - Multi-model Comparison Graphs
# 
# ---
# 
# ## Part 9 — Future Forecasting
# 
# This section performs rolling-window future demand prediction.
# 
# ### Forecast Horizon
# 
# ```python
# 7-Day Forecasting
# ```
# 
# ### Important Functions
# 
# ```python
# forecast_future()
# inverse_transform()
# ```
# 
# ### Purpose
# 
# To evaluate sequential forecasting continuity beyond observed data.
# 
# ---
# 
# # 6. Important Deep Learning Parameters
# 
# | Parameter | Value |
# |---|---|
# | Window Size | 30 |
# | Optimizer | Adam |
# | Loss Function | Mean Squared Error |
# | Epochs | 300 |
# | Batch Size | 16 |
# | Dropout | 0.2 |
# | Learning Rate | 0.001 |
# 
# ---
# 
# # 7. Logical Comparison Between Architectures
# 
# | Model | Advantages | Drawbacks |
# |---|---|---|
# | LSTM | Strong long-term memory learning | Higher computational cost |
# | GRU | Faster training and fewer parameters | Slightly weaker long-term dependency handling |
# | 1D CNN + LSTM | Better temporal feature extraction with deep sequence learning | Higher complexity and training time |
# | 1D CNN + GRU | Efficient hybrid architecture with reduced parameter load | Can underperform on highly complex long-term sequences |
# 
# ---
# 
# # 8. Comparative Architectural Analysis
# 
# | Feature | LSTM | GRU | CNN-LSTM | CNN-GRU |
# |---|---|---|---|---|
# | Sequential Learning | Excellent | Very Good | Excellent | Very Good |
# | Computational Cost | High | Medium | Very High | High |
# | Training Speed | Slower | Faster | Slower | Medium |
# | Long-Term Dependency Handling | Strong | Moderate-Strong | Strong | Moderate |
# | Temporal Pattern Extraction | Moderate | Moderate | Excellent | Excellent |
# | Parameter Count | High | Lower | Very High | High |
# | Forecast Stability | High | High | Moderate-High | Moderate |
# 
# ---
# 
# # 9. Key Functions Used in the Notebook
# 
# | Function | Purpose |
# |---|---|
# | `create_sequences()` | Converts time-series into sequential windows |
# | `build_lstm_model()` | Creates LSTM forecasting architecture |
# | `build_gru_model()` | Creates GRU forecasting architecture |
# | `forecast_future()` | Generates rolling future predictions |
# | `fit_transform()` | Feature scaling |
# | `inverse_transform()` | Converts scaled predictions back |
# | `EarlyStopping()` | Prevents overfitting |
# | `model.fit()` | Model training |
# | `model.predict()` | Forecast generation |
# 
# ---
# 
# # 10. Observations from Comparative Study
# 
# - LSTM demonstrates strong long-term sequential learning capability.
# - GRU achieves faster convergence with fewer trainable parameters.
# - CNN-based hybrids improve local temporal feature extraction.
# - Hybrid architectures show improved learning of short-term demand fluctuations.
# - Forecast realism improves significantly with longer sequential windows and engineered temporal features.
# - Cyclic encoding improves weekday and seasonal continuity learning.
# 
# ---
# 
# # 11. Conclusion
# 
# This notebook serves as a comparative deep learning extension of Project Prisight for retail demand forecasting analysis.
# 
# The implementation demonstrates:
# 
# - Sequential time-series forecasting
# - Recurrent neural network modeling
# - Hybrid CNN-RNN architectures
# - Temporal feature engineering
# - Forecast evaluation and comparison
# 
# The study provides a practical analytical comparison between:
# 
# - LSTM
# - GRU
# - 1D CNN-LSTM
# - 1D CNN-GRU
# 
# for intelligent retail sales demand forecasting within the Prisight ecosystem.
# 
# ---

# In[1]:


get_ipython().system('pip install tensorflow numpy pandas scikit-learn matplotlib seaborn -q')


# ---
# # ═══════════════════════════════════════
# # PART 1 — LSTM MODEL
# # ═══════════════════════════════════════

# ## 1. Setup and Imports

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time, json, pickle, os, warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    LSTM, GRU, Dense, Dropout, Conv1D, MaxPooling1D, BatchNormalization
)
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

np.random.seed(42)
tf.random.set_seed(42)
print('Libraries imported successfully!')
print(f'TensorFlow version: {tf.__version__}')


# ## 2. Generate Dataset

# In[3]:


def generate_test_dataset(n_products=4, n_days=500, start_date='2024-01-01'):
    """
    v4 data generation — key changes over v3:
    - n_days=500  → more training sequences
    - variance 3 → 1.5  (better signal-to-noise ratio)
    - weekend effect 1.35 → 1.70  (larger, clearly learnable pattern)
    - seasonality amplitude 0.25 → 0.40  (more pronounced)
    - elasticity raised (discount has clearer effect on demand)
    - sin/cos encoding for weekday and month added at generation time
    """
    product_configs = {
        1: {'base_price': 11999, 'base_demand': 12, 'variance': 1.5, 'elasticity': 1.2},
        2: {'base_price':   699, 'base_demand':  6, 'variance': 0.8, 'elasticity': 1.8},
        3: {'base_price':  2499, 'base_demand':  4, 'variance': 0.7, 'elasticity': 1.0},
        4: {'base_price':  6799, 'base_demand': 10, 'variance': 1.2, 'elasticity': 1.4},
    }
    dates = pd.date_range(start=start_date, periods=n_days, freq='D')
    all_records = []

    for product_id, config in product_configs.items():
        for i, date in enumerate(dates):
            weekday = date.weekday(); month = date.month
            selling_price    = config['base_price'] * np.random.uniform(0.97, 1.03)
            market_avg_price = config['base_price'] * np.random.uniform(0.93, 1.07)
            discount_percent = np.random.uniform(0, 30)
            is_weekend       = 1 if weekday >= 5 else 0
            weekday_effect   = 1.70 if is_weekend else 1.0
            monthly_season   = 1.0 + 0.40 * np.sin((month - 3) * np.pi / 6)
            trend            = 1.0 + (i / n_days) * 0.20
            discount_effect  = 1.0 + config['elasticity'] * (discount_percent / 100)
            price_ratio      = np.clip(market_avg_price / selling_price, 0.85, 1.20)
            base = config['base_demand'] * weekday_effect * monthly_season * trend * discount_effect * price_ratio
            noise = np.random.normal(0, config['variance'])
            units_sold = max(1, int(base + noise))
            all_records.append({
                'product_id': product_id, 'date': date,
                'units_sold': units_sold,
                'selling_price': round(selling_price, 2),
                'market_avg_price': round(market_avg_price, 2),
                'discount_percent': round(discount_percent, 2),
                'weekday': weekday, 'month': month, 'is_weekend': is_weekend,
                'price_ratio': round(price_ratio, 4),
                'discount_effect': round(discount_effect, 4),
                # Cyclic encoding — fixes continuity break in raw int encoding
                'weekday_sin': np.sin(2*np.pi*weekday/7),
                'weekday_cos': np.cos(2*np.pi*weekday/7),
                'month_sin':   np.sin(2*np.pi*(month-1)/12),
                'month_cos':   np.cos(2*np.pi*(month-1)/12),
            })

    df = pd.DataFrame(all_records)

    for pid in product_configs:
        mask = df['product_id'] == pid
        s = df.loc[mask, 'units_sold']
        df.loc[mask, 'rolling_avg_7']  = s.rolling(7,  min_periods=1).mean()
        df.loc[mask, 'rolling_avg_14'] = s.rolling(14, min_periods=1).mean()
        df.loc[mask, 'rolling_avg_30'] = s.rolling(30, min_periods=1).mean()
        df.loc[mask, 'lag_1']          = s.shift(1).fillna(s.mean())
        df.loc[mask, 'lag_7']          = s.shift(7).fillna(s.mean())
        df.loc[mask, 'demand_trend']   = (
            s.rolling(7, min_periods=1).mean()
            - s.rolling(14, min_periods=2).mean()
        ).fillna(0)
    return df

df = generate_test_dataset(n_products=4, n_days=500, start_date='2024-01-01')
df.to_csv('lstm_gru_test_dataset.csv', index=False)

print('='*60)
print('DATASET GENERATED — 500 days × 4 products')
print('='*60)
print(f'Shape       : {df.shape}')
print(f'Date range  : {df["date"].min().date()} → {df["date"].max().date()}')
p1 = df[df['product_id']==1]
print(f'\nProduct 1 units_sold stats:')
print(f'  mean={p1["units_sold"].mean():.1f}, std={p1["units_sold"].std():.1f}, '
      f'min={p1["units_sold"].min()}, max={p1["units_sold"].max()}')
print(f'  Weekend avg : {p1[p1["is_weekend"]==1]["units_sold"].mean():.1f}')
print(f'  Weekday avg : {p1[p1["is_weekend"]==0]["units_sold"].mean():.1f}')
df.head(8)


# ## 3. Data Exploration

# In[4]:


print('DATASET STATISTICS')
print('='*60)
print(df.describe())
print('\nMissing values:')
print(df.isnull().sum())
print('\nAverage units sold by product:')
print(df.groupby('product_id')['units_sold'].agg(['mean','std','min','max']))


# In[5]:


fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax1 = axes[0, 0]
for pid in df['product_id'].unique():
    pdata = df[df['product_id']==pid]
    ax1.plot(pdata['date'], pdata['units_sold'], label=f'Product {pid}', alpha=0.8)
ax1.set_title('Daily Units Sold Over Time'); ax1.set_xlabel('Date'); ax1.set_ylabel('Units Sold')
ax1.legend(); ax1.tick_params(axis='x', rotation=45)

ax2 = axes[0, 1]
for pid in df['product_id'].unique():
    ax2.hist(df[df['product_id']==pid]['units_sold'], alpha=0.5, label=f'Product {pid}', bins=15)
ax2.set_title('Distribution of Units Sold by Product')
ax2.set_xlabel('Units Sold'); ax2.set_ylabel('Frequency'); ax2.legend()

ax3 = axes[1, 0]
weekday_avg = df.groupby('weekday')['units_sold'].mean()
ax3.bar(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], weekday_avg.values, color='steelblue')
ax3.set_title('Average Sales by Day of Week'); ax3.set_xlabel('Day'); ax3.set_ylabel('Avg Units Sold')

ax4 = axes[1, 1]
p1 = df[df['product_id']==1].copy()
ax4.plot(p1['date'], p1['units_sold'], label='Daily Sales', alpha=0.6)
ax4.plot(p1['date'], p1['rolling_avg_7'],  label='7-day Avg',  linewidth=2)
ax4.plot(p1['date'], p1['rolling_avg_14'], label='14-day Avg', linewidth=2)
ax4.set_title('Product 1: Rolling Averages')
ax4.set_xlabel('Date'); ax4.set_ylabel('Units Sold')
ax4.legend(); ax4.tick_params(axis='x', rotation=45)

plt.suptitle('LSTM — Data Exploration', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('lstm_data_exploration.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved 'lstm_data_exploration.png'")


# ## 4. LSTM Model Architecture
# 
# **v4 architecture:**
# - 3 stacked LSTM layers: 128 → 64 → 32
# - L2 regularisation (1e-4) on all LSTM layers
# - Dense head: 64 → 32 → 1
# - Loss: **MSE** (not Huber — MSE penalises prediction-range collapse more strongly)
# - Window: **30 days**, Features: **16** (including sin/cos cyclic encoding)
# - Scaler fitted **on training data only** to prevent scale leakage
# 

# In[6]:


def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=input_shape,
             kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        LSTM(64, return_sequences=True,
             kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        LSTM(32, return_sequences=False,
             kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model

print('LSTM MODEL ARCHITECTURE')
print('='*60)
_preview = build_lstm_model(input_shape=(30, 16))
_preview.summary()


# ## 5. Data Preparation

# In[7]:


def create_sequence_dataset(df, feature_cols, target_col, window_size=30, product_id=None):
    data = df[df['product_id']==product_id].copy() if product_id else df.copy()
    data = data.sort_values('date').reset_index(drop=True)
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[feature_cols].iloc[i:i+window_size].values)
        y.append(data[target_col].iloc[i+window_size])
    return np.array(X), np.array(y), data

FEATURE_COLS = [
    'selling_price', 'market_avg_price', 'discount_percent',
    'rolling_avg_7', 'rolling_avg_14', 'rolling_avg_30',
    'is_weekend', 'price_ratio', 'discount_effect',
    'lag_1', 'lag_7', 'demand_trend',
    'weekday_sin', 'weekday_cos', 'month_sin', 'month_cos'
]
TARGET_COL  = 'units_sold'
WINDOW_SIZE = 30

X, y, product_df = create_sequence_dataset(df, FEATURE_COLS, TARGET_COL, WINDOW_SIZE, product_id=1)

print('LSTM DATASET PREPARED')
print('='*60)
print(f'Features ({len(FEATURE_COLS)}): {FEATURE_COLS}')
print(f'Window size     : {WINDOW_SIZE} days')
print(f'X shape         : {X.shape}')
print(f'Target mean/std : {y.mean():.2f} / {y.std():.2f}  (min {y.min()}, max {y.max()})')


# In[8]:


n_samples, n_timesteps, n_features = X.shape
train_size = int(len(X) * 0.8)

X_train_raw, X_test_raw = X[:train_size], X[train_size:]
y_train_raw, y_test_raw = y[:train_size], y[train_size:]
y_test_original = y[train_size:]

# CRITICAL FIX: fit scalers on TRAINING data only — no leakage from test set
lstm_scaler_X = MinMaxScaler()
lstm_scaler_y = MinMaxScaler()

X_train = lstm_scaler_X.fit_transform(X_train_raw.reshape(-1, n_features)).reshape(X_train_raw.shape)
X_test  = lstm_scaler_X.transform(X_test_raw.reshape(-1, n_features)).reshape(X_test_raw.shape)
y_train = lstm_scaler_y.fit_transform(y_train_raw.reshape(-1, 1)).flatten()
y_test  = lstm_scaler_y.transform(y_test_raw.reshape(-1, 1)).flatten()

print('DATA SPLIT (LSTM — no scale leakage)')
print('='*60)
print(f'Training samples : {len(X_train)}')
print(f'Testing  samples : {len(X_test)}')
print(f'Scaler fitted on training data only ✓')


# ## 6. LSTM Training  *(all 150 epochs run)*

# In[9]:


print('TRAINING LSTM MODEL')
print('='*60)

lstm_early_stop = EarlyStopping(monitor='val_loss', patience=25,
                                restore_best_weights=True, verbose=1)
lstm_reduce_lr  = ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                    patience=10, min_lr=1e-6, verbose=1)

lstm_model  = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
lstm_params = lstm_model.count_params()

# Gaussian noise augmentation (small — preserves signal while improving generalisation)
X_train_aug = X_train + 0.005 * np.random.randn(*X_train.shape)

lstm_start_time = time.time()
lstm_history = lstm_model.fit(
    X_train_aug, y_train,
    epochs=300,
    batch_size=32,
    validation_split=0.15,
    callbacks=[lstm_early_stop, lstm_reduce_lr],
    verbose=1
)
lstm_training_time = time.time() - lstm_start_time
lstm_epochs_run    = len(lstm_history.history['loss'])

print(f'\nLSTM Training Time : {lstm_training_time:.2f} seconds')
print(f'Epochs completed   : {lstm_epochs_run} / 300')


# In[10]:


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(lstm_history.history['loss'],     label='Train Loss',  linewidth=2)
axes[0].plot(lstm_history.history['val_loss'], label='Val Loss',    linewidth=2)
axes[0].set_title('LSTM — Loss Over Epochs')
axes[0].set_xlabel('Epoch'); axes[0].set_ylabel('Loss (MSE)')
axes[0].legend(); axes[0].grid(True, alpha=0.3)

axes[1].plot(lstm_history.history['mae'],     label='Train MAE', linewidth=2)
axes[1].plot(lstm_history.history['val_mae'], label='Val MAE',   linewidth=2)
axes[1].set_title('LSTM — MAE Over Epochs')
axes[1].set_xlabel('Epoch'); axes[1].set_ylabel('MAE')
axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('lstm_training_history.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Best val_loss : {min(lstm_history.history['val_loss']):.4f}")
print(f"Best val_mae  : {min(lstm_history.history['val_mae']):.4f}")


# ## 7. LSTM Evaluation

# In[11]:


y_pred_lstm_scaled   = lstm_model.predict(X_test, verbose=0).flatten()
y_pred_lstm_original = lstm_scaler_y.inverse_transform(y_pred_lstm_scaled.reshape(-1,1)).flatten()

lstm_mse  = mean_squared_error(y_test_original, y_pred_lstm_original)
lstm_rmse = np.sqrt(lstm_mse)
lstm_mae  = mean_absolute_error(y_test_original, y_pred_lstm_original)
lstm_r2   = r2_score(y_test_original, y_pred_lstm_original)
lstm_mape = np.mean(np.abs((y_test_original - y_pred_lstm_original) / y_test_original)) * 100
lstm_params = lstm_model.count_params()

print('LSTM MODEL EVALUATION RESULTS')
print('='*60)
print(f'MSE  : {lstm_mse:.4f}')
print(f'RMSE : {lstm_rmse:.4f}')
print(f'MAE  : {lstm_mae:.4f}')
print(f'R2   : {lstm_r2:.4f}')
print(f'MAPE : {lstm_mape:.2f}%')
print(f'Parameters : {lstm_params:,}')
print(f'Epochs run : {lstm_epochs_run}')
print(f'Training time : {lstm_training_time:.2f}s')
print()
interp = 'Excellent' if lstm_r2 > 0.8 else ('Good' if lstm_r2 > 0.6 else 'Moderate')
print(f'Interpretation: R2={lstm_r2:.3f} → {interp} model fit')


# In[12]:


residuals_lstm = y_test_original - y_pred_lstm_original
test_idx       = range(len(y_test_original))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Scatter
axes[0,0].scatter(y_test_original, y_pred_lstm_original, alpha=0.6, edgecolors='black', lw=0.5)
lims = [y_test_original.min(), y_test_original.max()]
axes[0,0].plot(lims, lims, 'r--', lw=2, label='Perfect')
axes[0,0].set_xlabel('Actual'); axes[0,0].set_ylabel('Predicted')
axes[0,0].set_title(f'LSTM — Predicted vs Actual  (R²={lstm_r2:.4f})')
axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)

# Residuals histogram
axes[0,1].hist(residuals_lstm, bins=20, edgecolor='black', alpha=0.7)
axes[0,1].axvline(x=0, color='red', linestyle='--', lw=2)
axes[0,1].set_title(f'LSTM — Residual Distribution  (mean={residuals_lstm.mean():.2f})')
axes[0,1].set_xlabel('Residual'); axes[0,1].set_ylabel('Freq'); axes[0,1].grid(True, alpha=0.3)

# Time series
axes[1,0].plot(test_idx, y_test_original,    'b-',  label='Actual',    lw=2, alpha=0.8)
axes[1,0].plot(test_idx, y_pred_lstm_original,'r--', label='LSTM Pred', lw=2, alpha=0.8)
axes[1,0].fill_between(test_idx, y_test_original, y_pred_lstm_original, alpha=0.15, color='gray')
axes[1,0].set_xlabel('Test Sample'); axes[1,0].set_ylabel('Units Sold')
axes[1,0].set_title('LSTM — Actual vs Predicted on Test Set')
axes[1,0].legend(); axes[1,0].grid(True, alpha=0.3)

# Residuals over time
axes[1,1].plot(test_idx, residuals_lstm, 'g-', lw=1.5)
axes[1,1].axhline(y=0,                   color='red',    linestyle='--', lw=2)
axes[1,1].axhline(y= residuals_lstm.std(),color='orange', linestyle=':',  lw=1.5, label=f'+1σ ({residuals_lstm.std():.2f})')
axes[1,1].axhline(y=-residuals_lstm.std(),color='orange', linestyle=':',  lw=1.5, label='-1σ')
axes[1,1].set_title('LSTM — Residuals Over Time')
axes[1,1].set_xlabel('Test Sample'); axes[1,1].set_ylabel('Residual')
axes[1,1].legend(); axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('lstm_evaluation.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 8. LSTM — Forecasting Future Sales

# In[13]:


def forecast_future(model, last_window_scaled, scaler_X, scaler_y,
                     feature_cols, n_days=7):
    """
    Iteratively forecast n_days ahead.
    Each predicted value is inverse-scaled, then the window slides forward
    by replacing the oldest timestep with a copy of the latest timestep
    updated with the new predicted units_sold (via the scaler).
    This ensures the rolling-average features in subsequent steps
    reflect the predicted demand rather than stale historical values.
    """
    predictions     = []
    current_window  = last_window_scaled.copy()  # shape (1, window, n_features)
    units_sold_idx  = feature_cols.index('rolling_avg_7')   # proxy feature to update

    for _ in range(n_days):
        pred_scaled   = model.predict(current_window, verbose=0)[0][0]
        pred_original = scaler_y.inverse_transform([[pred_scaled]])[0][0]
        predictions.append(round(float(pred_original), 2))

        # Build the next step: copy the last timestep and update rolling avg feature
        new_step = current_window[0, -1, :].copy()           # shape (n_features,)
        # Scale the predicted value back into feature space for rolling_avg_7
        dummy = current_window[0, -1, :].copy().reshape(1, -1)
        dummy[0, units_sold_idx] = pred_scaled               # inject scaled prediction
        new_step = dummy[0]

        # Slide window: drop oldest, append new step
        current_window = np.concatenate(
            [current_window[:, 1:, :], new_step.reshape(1, 1, -1)], axis=1
        )

    return predictions


lstm_forecasts = forecast_future(
    lstm_model, X_test[-1:].copy(),
    lstm_scaler_X, lstm_scaler_y,
    FEATURE_COLS, n_days=7
)

print('='*60)
print('LSTM — 7-DAY SALES FORECAST')
print('='*60)
for i, f in enumerate(lstm_forecasts, 1):
    print(f'  Day {i}: {f:.0f} units')
print(f'\nTotal 7-day : {sum(lstm_forecasts):.0f} units')
print(f'Daily avg   : {np.mean(lstm_forecasts):.1f} units')


# In[14]:


hist_days   = 14
recent_sales = product_df['units_sold'].iloc[-hist_days:].values
recent_dates = pd.date_range(end=product_df['date'].max(), periods=hist_days)
future_dates = pd.date_range(start=product_df['date'].max()+pd.Timedelta(days=1), periods=7)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(recent_dates, recent_sales, 'b-o', lw=2, label='Historical Sales', ms=6)
ax.plot(future_dates, lstm_forecasts, 'r--s', lw=2, label='LSTM Forecast', ms=8)
fstd = np.std(lstm_forecasts)
ax.fill_between(future_dates, [f-fstd for f in lstm_forecasts],
                              [f+fstd for f in lstm_forecasts],
                              alpha=0.2, color='red', label='±1 Std Dev')
ax.axvline(x=product_df['date'].max(), color='gray', linestyle=':', lw=2, alpha=0.7, label='Forecast Start')
ax.set_title('LSTM Sales Forecast — Product 1 (Next 7 Days)', fontsize=13)
ax.set_xlabel('Date'); ax.set_ylabel('Units Sold')
ax.legend(); ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('lstm_forecast.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 9. LSTM — Cross-Product Training

# In[15]:


lstm_results = []

for pid in df['product_id'].unique():
    print(f"\n{'='*60}")
    print(f'Training LSTM for Product {pid}')
    print('='*60)

    Xp, yp, _ = create_sequence_dataset(df, FEATURE_COLS, TARGET_COL, WINDOW_SIZE, pid)
    ns, nt, nf = Xp.shape
    tr = int(ns * 0.8)
    sX = MinMaxScaler(); sy = MinMaxScaler()
    # Fit on train only
    Xtr = sX.fit_transform(Xp[:tr].reshape(-1,nf)).reshape(Xp[:tr].shape)
    Xte = sX.transform(Xp[tr:].reshape(-1,nf)).reshape(Xp[tr:].shape)
    ytr = sy.fit_transform(yp[:tr].reshape(-1,1)).flatten()
    yte_orig = yp[tr:]

    Xtr_aug = Xtr + 0.005*np.random.randn(*Xtr.shape)
    mp = build_lstm_model((nt, nf))
    mp.fit(Xtr_aug, ytr, epochs=300, batch_size=32, validation_split=0.15,
           callbacks=[EarlyStopping(patience=25,restore_best_weights=True),
                      ReduceLROnPlateau(factor=0.5,patience=10,min_lr=1e-6)], verbose=0)

    yhat = sy.inverse_transform(mp.predict(Xte,verbose=0).reshape(-1,1)).flatten()
    rmse_p = np.sqrt(mean_squared_error(yte_orig, yhat))
    mae_p  = mean_absolute_error(yte_orig, yhat)
    r2_p   = r2_score(yte_orig, yhat)
    mape_p = np.mean(np.abs((yte_orig-yhat)/yte_orig))*100

    lstm_results.append({'Product ID':pid,'RMSE':rmse_p,'MAE':mae_p,'R2':r2_p,'MAPE':mape_p})
    print(f'RMSE: {rmse_p:.2f} | MAE: {mae_p:.2f} | R2: {r2_p:.3f} | MAPE: {mape_p:.1f}%')

lstm_results_df = pd.DataFrame(lstm_results)
print('\n'+'='*60)
print('LSTM — CROSS-PRODUCT RESULTS')
print('='*60)
print(lstm_results_df.to_string(index=False))
print(f'\nLSTM Average R2: {lstm_results_df["R2"].mean():.4f}')


# In[16]:


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
products = lstm_results_df['Product ID'].values
xlabels  = [f'P{p}' for p in products]

axes[0].bar(xlabels, lstm_results_df['RMSE'], color='steelblue')
axes[0].set_title('LSTM RMSE by Product (Lower=Better)')
axes[0].set_ylabel('RMSE')

axes[1].bar(xlabels, lstm_results_df['R2'], color='seagreen')
axes[1].axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='Good (0.8)')
axes[1].set_title('LSTM R2 by Product (Higher=Better)')
axes[1].set_ylabel('R2'); axes[1].legend()

axes[2].bar(xlabels, lstm_results_df['MAPE'], color='coral')
axes[2].set_title('LSTM MAPE by Product (Lower=Better)')
axes[2].set_ylabel('MAPE (%)')

plt.suptitle('LSTM — Cross-Product Performance', fontweight='bold')
plt.tight_layout()
plt.savefig('lstm_product_comparison.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 10. LSTM Efficiency Summary

# In[17]:


print('='*70)
print('LSTM MODEL EFFICIENCY SUMMARY')
print('='*70)
print('ARCHITECTURE:')
print(f'  Input          : {X_train.shape[1]} timesteps × {X_train.shape[2]} features')
print( '  Layer 1        : LSTM(64) + Dropout(0.2)')
print( '  Layer 2        : LSTM(32) + Dropout(0.2)')
print( '  Dense          : Dense(16, relu) → Dense(1)')
print( '  Optimizer      : Adam(lr=0.001)  |  Loss: MSE')
print(f'  Parameters     : {lstm_params:,}')
print()
print('TRAINING:')
print(f'  Train samples  : {len(X_train)}')
print( '  Val split      : 15%  |  Batch size: 8')
print(f'  Max epochs     : 150')
print(f'  Epochs run     : {lstm_epochs_run}')
print( '  EarlyStopping  : patience=20')
print( '  ReduceLR       : factor=0.5, patience=7')
print(f'  Training time  : {lstm_training_time:.2f}s')
print()
print('TEST PERFORMANCE (Product 1):')
print(f'  MSE  : {lstm_mse:.4f}')
print(f'  RMSE : {lstm_rmse:.2f} units')
print(f'  MAE  : {lstm_mae:.2f} units')
print(f'  R2   : {lstm_r2:.4f}')
print(f'  MAPE : {lstm_mape:.2f}%')
print()
print('AVERAGE CROSS-PRODUCT:')
print(f'  RMSE : {lstm_results_df["RMSE"].mean():.2f}')
print(f'  MAE  : {lstm_results_df["MAE"].mean():.2f}')
print(f'  R2   : {lstm_results_df["R2"].mean():.4f}')
print(f'  MAPE : {lstm_results_df["MAPE"].mean():.2f}%')
print('='*70)


# ## 11. Save LSTM Artifacts

# In[18]:


os.makedirs('lstm_artifacts', exist_ok=True)
lstm_model.save('lstm_artifacts/lstm_model.keras')
with open('lstm_artifacts/scaler_X.pkl', 'wb') as f: pickle.dump(lstm_scaler_X, f)
with open('lstm_artifacts/scaler_y.pkl', 'wb') as f: pickle.dump(lstm_scaler_y, f)
with open('lstm_artifacts/config.json', 'w') as f:
    json.dump({'feature_cols': FEATURE_COLS, 'target_col': TARGET_COL,
               'window_size': WINDOW_SIZE,
               'input_shape': [X_train.shape[1], X_train.shape[2]]}, f, indent=2)
lstm_results_df.to_csv('lstm_artifacts/model_results.csv', index=False)
print('LSTM artifacts saved:')
for f in os.listdir('lstm_artifacts'): print(f'  {f}')


# ---
# # ═══════════════════════════════════════
# # PART 2 — GRU MODEL
# # ═══════════════════════════════════════
# 
# **Why GRU?**
# - Uses **reset** and **update** gates (vs LSTM's input/forget/output gates)
# - Fewer parameters than LSTM — often trains faster
# - Competitive accuracy on shorter sequences
# - Trade-off: slightly less expressive than LSTM on long-range dependencies

# ## 12. GRU Model Architecture
# 
# **GRU Hyperparameters (deliberately different from LSTM):**
# - Layer 1: **GRU(128)** + Dropout(**0.3**)
# - Layer 2: **GRU(64)** + Dropout(**0.3**)
# - Dense(**32**, relu) → Dense(**16**, relu) → Dense(1)
# - Optimizer: Adam(lr=**0.0005**) | Loss: MSE
# - Epochs: **200** | Batch size: **16** | EarlyStopping patience: **25**

# In[19]:


def build_gru_model(input_shape):
    model = Sequential([
        GRU(128, return_sequences=True, input_shape=input_shape,
            kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        GRU(64, return_sequences=True,
            kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        GRU(32, return_sequences=False,
            kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model

print('build_gru_model() defined.')
print('Run the data-prep cell below first, then architecture summary will print automatically.')


# ## 13. GRU Data Preparation
# 
# Same dataset, same split — independent scalers to keep both models completely separate.

# In[20]:


# ── GRU Data Preparation (independent scalers, no leakage) ──
gru_scaler_X = MinMaxScaler()
gru_scaler_y = MinMaxScaler()

Xg, yg, product_df_gru = create_sequence_dataset(
    df, FEATURE_COLS, TARGET_COL, WINDOW_SIZE, product_id=1)
ng_samples, ng_timesteps, ng_features = Xg.shape

gru_train_size           = int(len(Xg) * 0.8)
Xg_train_raw, Xg_test_raw = Xg[:gru_train_size], Xg[gru_train_size:]
yg_train_raw, yg_test_raw = yg[:gru_train_size], yg[gru_train_size:]
yg_test_original          = yg[gru_train_size:]

# Fit scalers on TRAINING data only
Xg_train = gru_scaler_X.fit_transform(
    Xg_train_raw.reshape(-1, ng_features)).reshape(Xg_train_raw.shape)
Xg_test  = gru_scaler_X.transform(
    Xg_test_raw.reshape(-1, ng_features)).reshape(Xg_test_raw.shape)
yg_train = gru_scaler_y.fit_transform(yg_train_raw.reshape(-1, 1)).flatten()
yg_test  = gru_scaler_y.transform(yg_test_raw.reshape(-1, 1)).flatten()

print('DATA SPLIT (GRU — independent scaler, no leakage)')
print('='*60)
print(f'Training samples : {len(Xg_train)}')
print(f'Testing  samples : {len(Xg_test)}')
print(f'Input shape      : {Xg_train.shape}')

# ── GRU Model Architecture (instantiated here so Xg_train exists) ──
print('\nGRU MODEL ARCHITECTURE')
print('='*60)
gru_model  = build_gru_model(input_shape=(Xg_train.shape[1], Xg_train.shape[2]))
gru_params = gru_model.count_params()
gru_model.summary()
print(f'\nLSTM params: {lstm_params:,}  |  GRU params: {gru_params:,}')


# ## 14. GRU Training  *(all 200 epochs run)*

# In[21]:


print('TRAINING GRU MODEL')
print('='*60)

gru_early_stop = EarlyStopping(monitor='val_loss', patience=25,
                                restore_best_weights=True, verbose=1)
gru_reduce_lr  = ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                    patience=10, min_lr=1e-7, verbose=1)

gru_model = build_gru_model(input_shape=(Xg_train.shape[1], Xg_train.shape[2]))

Xg_train_aug = Xg_train + 0.005 * np.random.randn(*Xg_train.shape)

gru_start_time = time.time()
gru_history = gru_model.fit(
    Xg_train_aug, yg_train,
    epochs=300,
    batch_size=32,
    validation_split=0.15,
    callbacks=[gru_early_stop, gru_reduce_lr],
    verbose=1
)
gru_training_time = time.time() - gru_start_time
gru_epochs_run    = len(gru_history.history['loss'])

print(f'\nGRU Training Time : {gru_training_time:.2f} seconds')
print(f'Epochs completed  : {gru_epochs_run} / 300')


# In[22]:


fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(gru_history.history['loss'],     label='Train Loss', linewidth=2, color='darkorange')
axes[0].plot(gru_history.history['val_loss'], label='Val Loss',   linewidth=2, color='orangered')
axes[0].set_title('GRU — Loss Over Epochs')
axes[0].set_xlabel('Epoch'); axes[0].set_ylabel('Loss (MSE)')
axes[0].legend(); axes[0].grid(True, alpha=0.3)

axes[1].plot(gru_history.history['mae'],     label='Train MAE', linewidth=2, color='darkorange')
axes[1].plot(gru_history.history['val_mae'], label='Val MAE',   linewidth=2, color='orangered')
axes[1].set_title('GRU — MAE Over Epochs')
axes[1].set_xlabel('Epoch'); axes[1].set_ylabel('MAE')
axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('gru_training_history.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Best val_loss : {min(gru_history.history['val_loss']):.4f}")
print(f"Best val_mae  : {min(gru_history.history['val_mae']):.4f}")


# ## 15. GRU Evaluation

# In[23]:


y_pred_gru_scaled   = gru_model.predict(Xg_test, verbose=0).flatten()
y_pred_gru_original = gru_scaler_y.inverse_transform(y_pred_gru_scaled.reshape(-1,1)).flatten()

gru_mse  = mean_squared_error(yg_test_original, y_pred_gru_original)
gru_rmse = np.sqrt(gru_mse)
gru_mae  = mean_absolute_error(yg_test_original, y_pred_gru_original)
gru_r2   = r2_score(yg_test_original, y_pred_gru_original)
gru_mape = np.mean(np.abs((yg_test_original - y_pred_gru_original) / yg_test_original)) * 100

print('GRU MODEL EVALUATION RESULTS')
print('='*60)
print(f'MSE  : {gru_mse:.4f}')
print(f'RMSE : {gru_rmse:.4f}')
print(f'MAE  : {gru_mae:.4f}')
print(f'R2   : {gru_r2:.4f}')
print(f'MAPE : {gru_mape:.2f}%')
print(f'Parameters    : {gru_params:,}')
print(f'Epochs run    : {gru_epochs_run}')
print(f'Training time : {gru_training_time:.2f}s')
print()
interp = 'Excellent' if gru_r2 > 0.8 else ('Good' if gru_r2 > 0.6 else 'Moderate')
print(f'Interpretation: R2={gru_r2:.3f} → {interp} model fit')


# In[24]:


residuals_gru = yg_test_original - y_pred_gru_original
gru_test_idx  = range(len(yg_test_original))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].scatter(yg_test_original, y_pred_gru_original, alpha=0.6, edgecolors='black', lw=0.5, color='darkorange')
lims = [yg_test_original.min(), yg_test_original.max()]
axes[0,0].plot(lims, lims, 'b--', lw=2, label='Perfect')
axes[0,0].set_xlabel('Actual'); axes[0,0].set_ylabel('Predicted')
axes[0,0].set_title(f'GRU — Predicted vs Actual  (R²={gru_r2:.4f})')
axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)

axes[0,1].hist(residuals_gru, bins=20, edgecolor='black', alpha=0.7, color='darkorange')
axes[0,1].axvline(x=0, color='blue', linestyle='--', lw=2)
axes[0,1].set_title(f'GRU — Residual Distribution  (mean={residuals_gru.mean():.2f})')
axes[0,1].set_xlabel('Residual'); axes[0,1].set_ylabel('Freq'); axes[0,1].grid(True, alpha=0.3)

axes[1,0].plot(gru_test_idx, yg_test_original,   'b-',  label='Actual',   lw=2, alpha=0.8)
axes[1,0].plot(gru_test_idx, y_pred_gru_original, 'r--', label='GRU Pred', lw=2, alpha=0.8)
axes[1,0].fill_between(gru_test_idx, yg_test_original, y_pred_gru_original, alpha=0.15, color='gray')
axes[1,0].set_title('GRU — Actual vs Predicted on Test Set')
axes[1,0].set_xlabel('Test Sample'); axes[1,0].set_ylabel('Units Sold')
axes[1,0].legend(); axes[1,0].grid(True, alpha=0.3)

axes[1,1].plot(gru_test_idx, residuals_gru, color='darkorange', lw=1.5)
axes[1,1].axhline(y=0,                    color='blue',   linestyle='--', lw=2)
axes[1,1].axhline(y= residuals_gru.std(), color='orange', linestyle=':',  lw=1.5, label=f'+1σ ({residuals_gru.std():.2f})')
axes[1,1].axhline(y=-residuals_gru.std(), color='orange', linestyle=':',  lw=1.5, label='-1σ')
axes[1,1].set_title('GRU — Residuals Over Time')
axes[1,1].set_xlabel('Test Sample'); axes[1,1].set_ylabel('Residual')
axes[1,1].legend(); axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('gru_evaluation.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 16. GRU — Forecasting Future Sales

# In[25]:


gru_forecasts = forecast_future(
    gru_model, Xg_test[-1:].copy(),
    gru_scaler_X, gru_scaler_y,
    FEATURE_COLS, n_days=7
)

print('='*60)
print('GRU — 7-DAY SALES FORECAST')
print('='*60)
for i, f in enumerate(gru_forecasts, 1):
    print(f'  Day {i}: {f:.0f} units')
print(f'\nTotal 7-day : {sum(gru_forecasts):.0f} units')
print(f'Daily avg   : {np.mean(gru_forecasts):.1f} units')


# In[26]:


future_dates_gru = pd.date_range(start=product_df_gru['date'].max()+pd.Timedelta(days=1), periods=7)
recent_dates_gru = pd.date_range(end=product_df_gru['date'].max(), periods=14)
recent_sales_gru = product_df_gru['units_sold'].iloc[-14:].values

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(recent_dates_gru, recent_sales_gru, 'b-o', lw=2, label='Historical Sales', ms=6)
ax.plot(future_dates_gru, gru_forecasts, 'r--D', lw=2, label='GRU Forecast', ms=8, color='darkorange')
gfstd = np.std(gru_forecasts)
ax.fill_between(future_dates_gru, [f-gfstd for f in gru_forecasts],
                                   [f+gfstd for f in gru_forecasts],
                                   alpha=0.2, color='darkorange', label='±1 Std Dev')
ax.axvline(x=product_df_gru['date'].max(), color='gray', linestyle=':', lw=2, alpha=0.7, label='Forecast Start')
ax.set_title('GRU Sales Forecast — Product 1 (Next 7 Days)', fontsize=13)
ax.set_xlabel('Date'); ax.set_ylabel('Units Sold')
ax.legend(); ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('gru_forecast.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 17. GRU — Cross-Product Training

# In[27]:


gru_results = []

for pid in df['product_id'].unique():
    print(f"\n{'='*60}")
    print(f'Training GRU for Product {pid}')
    print('='*60)

    Xp, yp, _ = create_sequence_dataset(df, FEATURE_COLS, TARGET_COL, WINDOW_SIZE, pid)
    ns, nt, nf = Xp.shape
    tr = int(ns * 0.8)
    sX = MinMaxScaler(); sy = MinMaxScaler()
    Xtr = sX.fit_transform(Xp[:tr].reshape(-1,nf)).reshape(Xp[:tr].shape)
    Xte = sX.transform(Xp[tr:].reshape(-1,nf)).reshape(Xp[tr:].shape)
    ytr = sy.fit_transform(yp[:tr].reshape(-1,1)).flatten()
    yte_orig = yp[tr:]

    Xtr_aug = Xtr + 0.005*np.random.randn(*Xtr.shape)
    mp = build_gru_model((nt, nf))
    mp.fit(Xtr_aug, ytr, epochs=300, batch_size=32, validation_split=0.15,
           callbacks=[EarlyStopping(patience=25,restore_best_weights=True),
                      ReduceLROnPlateau(factor=0.5,patience=10,min_lr=1e-7)], verbose=0)

    yhat = sy.inverse_transform(mp.predict(Xte,verbose=0).reshape(-1,1)).flatten()
    rmse_p = np.sqrt(mean_squared_error(yte_orig, yhat))
    mae_p  = mean_absolute_error(yte_orig, yhat)
    r2_p   = r2_score(yte_orig, yhat)
    mape_p = np.mean(np.abs((yte_orig-yhat)/yte_orig))*100

    gru_results.append({'Product ID':pid,'RMSE':rmse_p,'MAE':mae_p,'R2':r2_p,'MAPE':mape_p})
    print(f'RMSE: {rmse_p:.2f} | MAE: {mae_p:.2f} | R2: {r2_p:.3f} | MAPE: {mape_p:.1f}%')

gru_results_df = pd.DataFrame(gru_results)
print('\n'+'='*60)
print('GRU — CROSS-PRODUCT RESULTS')
print('='*60)
print(gru_results_df.to_string(index=False))
print(f'\nGRU Average R2: {gru_results_df["R2"].mean():.4f}')


# In[28]:


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
products = gru_results_df['Product ID'].values
xlabels  = [f'P{p}' for p in products]

axes[0].bar(xlabels, gru_results_df['RMSE'], color='darkorange')
axes[0].set_title('GRU RMSE by Product (Lower=Better)')
axes[0].set_ylabel('RMSE')

axes[1].bar(xlabels, gru_results_df['R2'], color='chocolate')
axes[1].axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='Good (0.8)')
axes[1].set_title('GRU R2 by Product (Higher=Better)')
axes[1].set_ylabel('R2'); axes[1].legend()

axes[2].bar(xlabels, gru_results_df['MAPE'], color='peru')
axes[2].set_title('GRU MAPE by Product (Lower=Better)')
axes[2].set_ylabel('MAPE (%)')

plt.suptitle('GRU — Cross-Product Performance', fontweight='bold')
plt.tight_layout()
plt.savefig('gru_product_comparison.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 18. GRU Efficiency Summary

# In[29]:


print('='*70)
print('GRU MODEL EFFICIENCY SUMMARY')
print('='*70)
print('ARCHITECTURE:')
print(f'  Input          : {Xg_train.shape[1]} timesteps × {Xg_train.shape[2]} features')
print( '  Layer 1        : GRU(128) + Dropout(0.3)')
print( '  Layer 2        : GRU(64)  + Dropout(0.3)')
print( '  Dense          : Dense(32, relu) → Dense(16, relu) → Dense(1)')
print( '  Optimizer      : Adam(lr=0.0005)  |  Loss: MSE')
print(f'  Parameters     : {gru_params:,}')
print()
print('TRAINING:')
print(f'  Train samples  : {len(Xg_train)}')
print( '  Val split      : 15%  |  Batch size: 16')
print(f'  Max epochs     : 200')
print(f'  Epochs run     : {gru_epochs_run}')
print( '  EarlyStopping  : patience=25')
print( '  ReduceLR       : factor=0.5, patience=10')
print(f'  Training time  : {gru_training_time:.2f}s')
print()
print('TEST PERFORMANCE (Product 1):')
print(f'  MSE  : {gru_mse:.4f}')
print(f'  RMSE : {gru_rmse:.2f} units')
print(f'  MAE  : {gru_mae:.2f} units')
print(f'  R2   : {gru_r2:.4f}')
print(f'  MAPE : {gru_mape:.2f}%')
print()
print('AVERAGE CROSS-PRODUCT:')
print(f'  RMSE : {gru_results_df["RMSE"].mean():.2f}')
print(f'  MAE  : {gru_results_df["MAE"].mean():.2f}')
print(f'  R2   : {gru_results_df["R2"].mean():.4f}')
print(f'  MAPE : {gru_results_df["MAPE"].mean():.2f}%')
print('='*70)


# ## 19. Save GRU Artifacts

# In[30]:


os.makedirs('gru_artifacts', exist_ok=True)
gru_model.save('gru_artifacts/gru_model.keras')
with open('gru_artifacts/scaler_X.pkl', 'wb') as f: pickle.dump(gru_scaler_X, f)
with open('gru_artifacts/scaler_y.pkl', 'wb') as f: pickle.dump(gru_scaler_y, f)
with open('gru_artifacts/config.json', 'w') as f:
    json.dump({'feature_cols': FEATURE_COLS, 'target_col': TARGET_COL,
               'window_size': WINDOW_SIZE,
               'input_shape': [Xg_train.shape[1], Xg_train.shape[2]]}, f, indent=2)
gru_results_df.to_csv('gru_artifacts/model_results.csv', index=False)
print('GRU artifacts saved:')
for f in os.listdir('gru_artifacts'): print(f'  {f}')


# ---
# # ═══════════════════════════════════════
# # PART 3 — LSTM vs GRU COMPARISON
# # ═══════════════════════════════════════

# ## 20. Hyperparameter Comparison Table

# In[31]:


hparam_df = pd.DataFrame({
    'Hyperparameter': [
        'Architecture', 'Gate Mechanism', 'Layer 1', 'Layer 2', 'Dense Layers',
        'Dropout', 'Learning Rate', 'Batch Size', 'Max Epochs',
        'EarlyStopping Patience', 'ReduceLR Patience', 'Parameters'
    ],
    'LSTM': [
        'Unidirectional LSTM', '3 gates (input/forget/output)', 'LSTM(64)', 'LSTM(32)', 'Dense(16)→Dense(1)',
        '0.2', '0.001', '8', '150',
        '20', '7', f'{lstm_params:,}'
    ],
    'GRU': [
        'Unidirectional GRU', '2 gates (reset/update)', 'GRU(128)', 'GRU(64)', 'Dense(32)→Dense(16)→Dense(1)',
        '0.3', '0.0005', '16', '200',
        '25', '10', f'{gru_params:,}'
    ]
})

print('HYPERPARAMETER COMPARISON')
print('='*75)
print(hparam_df.to_string(index=False))


# ## 21. Epochs Comparison (Training Curves Side-by-Side)

# In[32]:


fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Loss
ax = axes[0]
ax.plot(lstm_history.history['loss'],     'b-',  label='LSTM Train Loss',  lw=2)
ax.plot(lstm_history.history['val_loss'], 'b--', label='LSTM Val Loss',    lw=2, alpha=0.7)
ax.plot(gru_history.history['loss'],      'r-',  label='GRU Train Loss',   lw=2)
ax.plot(gru_history.history['val_loss'],  'r--', label='GRU Val Loss',     lw=2, alpha=0.7)
ax.axvline(x=lstm_epochs_run-1, color='blue', linestyle=':', alpha=0.5, label=f'LSTM stopped @ {lstm_epochs_run}')
ax.axvline(x=gru_epochs_run-1,  color='red',  linestyle=':', alpha=0.5, label=f'GRU stopped @ {gru_epochs_run}')
ax.set_title('Training & Validation Loss — Both Models')
ax.set_xlabel('Epoch'); ax.set_ylabel('Loss (MSE)')
ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

# MAE
ax2 = axes[1]
ax2.plot(lstm_history.history['mae'],     'b-',  label='LSTM Train MAE',  lw=2)
ax2.plot(lstm_history.history['val_mae'], 'b--', label='LSTM Val MAE',    lw=2, alpha=0.7)
ax2.plot(gru_history.history['mae'],      'r-',  label='GRU Train MAE',   lw=2)
ax2.plot(gru_history.history['val_mae'],  'r--', label='GRU Val MAE',     lw=2, alpha=0.7)
ax2.set_title('Training & Validation MAE — Both Models')
ax2.set_xlabel('Epoch'); ax2.set_ylabel('MAE')
ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)

print(f'LSTM  max epochs: 150  |  epochs actually run: {lstm_epochs_run}')
print(f'GRU   max epochs: 200  |  epochs actually run: {gru_epochs_run}')

plt.tight_layout()
plt.savefig('comparison_training_curves.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 22. Full Metrics Comparison Table

# In[33]:


def better(lstm_val, gru_val, higher_is_better=False):
    if higher_is_better:
        return 'GRU ✓' if gru_val > lstm_val else 'LSTM ✓'
    return 'GRU ✓' if gru_val < lstm_val else 'LSTM ✓'

metrics_df = pd.DataFrame({
    'Metric': ['MSE','RMSE','MAE','R2 Score','MAPE (%)',
               'Epochs Run','Max Epochs','Batch Size','Learning Rate',
               'Training Time (s)','Parameters'],
    'LSTM': [f'{lstm_mse:.4f}', f'{lstm_rmse:.4f}', f'{lstm_mae:.4f}',
             f'{lstm_r2:.4f}', f'{lstm_mape:.2f}',
             lstm_epochs_run, 150, 8, '0.001',
             f'{lstm_training_time:.2f}', f'{lstm_params:,}'],
    'GRU':  [f'{gru_mse:.4f}',  f'{gru_rmse:.4f}',  f'{gru_mae:.4f}',
             f'{gru_r2:.4f}',  f'{gru_mape:.2f}',
             gru_epochs_run, 200, 16, '0.0005',
             f'{gru_training_time:.2f}', f'{gru_params:,}'],
    'Winner': [
        better(lstm_mse,  gru_mse),
        better(lstm_rmse, gru_rmse),
        better(lstm_mae,  gru_mae),
        better(lstm_r2,   gru_r2,  higher_is_better=True),
        better(lstm_mape, gru_mape),
        'N/A','N/A','N/A','N/A',
        better(lstm_training_time, gru_training_time),
        better(lstm_params, gru_params)
    ]
})

print('='*75)
print('LSTM vs GRU — FULL METRICS COMPARISON (Product 1)')
print('='*75)
print(metrics_df.to_string(index=False))


# ## 23. Visual Comparison — Error Metrics, R2, Predictions

# In[34]:


fig, axes = plt.subplots(2, 3, figsize=(18, 12))

colors = ['steelblue', 'darkorange']
models = ['LSTM', 'GRU']

# 1. Error metrics bar chart
ax1 = axes[0,0]
metrics_names = ['MSE','RMSE','MAE']
lstm_vals  = [lstm_mse,  lstm_rmse,  lstm_mae]
gru_vals   = [gru_mse,   gru_rmse,   gru_mae]
x = np.arange(len(metrics_names)); w = 0.35
ax1.bar(x-w/2, lstm_vals, w, label='LSTM', color='steelblue')
ax1.bar(x+w/2, gru_vals,  w, label='GRU',  color='darkorange')
ax1.set_title('Error Metrics (Lower = Better)')
ax1.set_xticks(x); ax1.set_xticklabels(metrics_names)
ax1.legend(); ax1.grid(True, alpha=0.3, axis='y')

# 2. R2 comparison
ax2 = axes[0,1]
bars = ax2.bar(models, [lstm_r2, gru_r2], color=colors, edgecolor='black')
ax2.axhline(y=0.6, color='green',     linestyle='--', alpha=0.7, label='Good (0.6)')
ax2.axhline(y=0.8, color='darkgreen', linestyle='--', alpha=0.7, label='Excellent (0.8)')
ax2.set_title('R2 Score (Higher = Better)')
ax2.legend(); ax2.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, [lstm_r2, gru_r2]):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01, f'{val:.4f}',
             ha='center', va='bottom', fontweight='bold')

# 3. MAPE comparison
ax3 = axes[0,2]
bars = ax3.bar(models, [lstm_mape, gru_mape], color=colors, edgecolor='black')
ax3.set_title('MAPE % (Lower = Better)')
ax3.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, [lstm_mape, gru_mape]):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{val:.1f}%',
             ha='center', va='bottom', fontweight='bold')

# 4. LSTM scatter
ax4 = axes[1,0]
ax4.scatter(y_test_original, y_pred_lstm_original, alpha=0.6, edgecolors='black', lw=0.5, color='steelblue')
lims = [min(y_test_original.min(), y_pred_lstm_original.min()),
        max(y_test_original.max(), y_pred_lstm_original.max())]
ax4.plot(lims, lims, 'r--', lw=2, label='Perfect')
ax4.set_title(f'LSTM  Predicted vs Actual  (R²={lstm_r2:.4f})')
ax4.set_xlabel('Actual'); ax4.set_ylabel('Predicted')
ax4.legend(); ax4.grid(True, alpha=0.3)

# 5. GRU scatter
ax5 = axes[1,1]
ax5.scatter(yg_test_original, y_pred_gru_original, alpha=0.6, edgecolors='black', lw=0.5, color='darkorange')
limsg = [min(yg_test_original.min(), y_pred_gru_original.min()),
         max(yg_test_original.max(), y_pred_gru_original.max())]
ax5.plot(limsg, limsg, 'b--', lw=2, label='Perfect')
ax5.set_title(f'GRU  Predicted vs Actual  (R²={gru_r2:.4f})')
ax5.set_xlabel('Actual'); ax5.set_ylabel('Predicted')
ax5.legend(); ax5.grid(True, alpha=0.3)

# 6. Time series overlay
ax6 = axes[1,2]
common_len = min(len(y_test_original), len(yg_test_original))
tidx = range(common_len)
ax6.plot(tidx, y_test_original[:common_len],   'k-',  label='Actual', lw=2, alpha=0.9)
ax6.plot(tidx, y_pred_lstm_original[:common_len], 'b--', label='LSTM', lw=1.8, alpha=0.8)
ax6.plot(tidx, y_pred_gru_original[:common_len],  'r--', label='GRU',  lw=1.8, alpha=0.8, color='darkorange')
ax6.set_title('Actual vs Both Models — Test Set')
ax6.set_xlabel('Test Sample'); ax6.set_ylabel('Units Sold')
ax6.legend(); ax6.grid(True, alpha=0.3)

plt.suptitle('LSTM vs GRU — Full Visual Comparison', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('lstm_gru_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved 'lstm_gru_comparison.png'")


# ## 24. Parameters & Epochs — Detailed Comparison

# In[35]:


fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Parameters bar
ax = axes[0]
bars = ax.bar(['LSTM','GRU'], [lstm_params, gru_params], color=['steelblue','darkorange'], edgecolor='black')
ax.set_title('Model Parameters')
ax.set_ylabel('# Parameters')
for bar, val in zip(bars, [lstm_params, gru_params]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+200, f'{val:,}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Epochs run vs max
ax2 = axes[1]
x = np.arange(2); w = 0.35
ax2.bar(x-w/2, [150, 200],              w, label='Max Epochs', color='lightgray', edgecolor='black')
ax2.bar(x+w/2, [lstm_epochs_run, gru_epochs_run], w, label='Epochs Run',
        color=['steelblue','darkorange'], edgecolor='black')
ax2.set_xticks(x); ax2.set_xticklabels(['LSTM','GRU'])
ax2.set_title('Max Epochs vs Epochs Actually Run')
ax2.set_ylabel('Epochs')
ax2.legend(); ax2.grid(True, alpha=0.3, axis='y')

# Training time
ax3 = axes[2]
bars = ax3.bar(['LSTM','GRU'], [lstm_training_time, gru_training_time],
               color=['steelblue','darkorange'], edgecolor='black')
ax3.set_title('Training Time (seconds)')
ax3.set_ylabel('Seconds')
for bar, val in zip(bars, [lstm_training_time, gru_training_time]):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}s',
             ha='center', va='bottom', fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

plt.suptitle('Parameters, Epochs & Training Time Comparison', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('comparison_params_epochs.png', dpi=150, bbox_inches='tight')
plt.show()

print(f'LSTM  — params: {lstm_params:,}  |  epochs: {lstm_epochs_run}/{150}  |  time: {lstm_training_time:.2f}s')
print(f'GRU   — params: {gru_params:,}   |  epochs: {gru_epochs_run}/{200}   |  time: {gru_training_time:.2f}s')
print(f'GRU is {gru_params/lstm_params:.2f}× the size of LSTM and {gru_training_time/lstm_training_time:.2f}× the training time')


# ## 25. Cross-Product Comparison

# In[36]:


cross_df = pd.DataFrame({
    'Product ID'    : lstm_results_df['Product ID'],
    'LSTM RMSE'     : lstm_results_df['RMSE'],
    'GRU RMSE'      : gru_results_df['RMSE'],
    'LSTM R2'       : lstm_results_df['R2'],
    'GRU R2'        : gru_results_df['R2'],
    'LSTM MAPE'     : lstm_results_df['MAPE'],
    'GRU MAPE'      : gru_results_df['MAPE'],
    'Winner (RMSE)' : ['GRU ✓' if gru_results_df.iloc[i]['RMSE'] < lstm_results_df.iloc[i]['RMSE']
                       else 'LSTM ✓' for i in range(len(lstm_results_df))],
    'Winner (R2)'   : ['GRU ✓' if gru_results_df.iloc[i]['R2']   > lstm_results_df.iloc[i]['R2']
                       else 'LSTM ✓' for i in range(len(lstm_results_df))]
})

print('CROSS-PRODUCT COMPARISON')
print('='*80)
print(cross_df.to_string(index=False))

lstm_rmse_wins  = sum(cross_df['Winner (RMSE)'] == 'LSTM ✓')
gru_rmse_wins   = sum(cross_df['Winner (RMSE)'] == 'GRU ✓')
lstm_r2_wins    = sum(cross_df['Winner (R2)']   == 'LSTM ✓')
gru_r2_wins     = sum(cross_df['Winner (R2)']   == 'GRU ✓')

print(f'\nBy RMSE: LSTM {lstm_rmse_wins}/4  |  GRU {gru_rmse_wins}/4')
print(f'By R2  : LSTM {lstm_r2_wins}/4    |  GRU {gru_r2_wins}/4')


# In[37]:


fig, axes = plt.subplots(1, 3, figsize=(16, 5))
prods = cross_df['Product ID'].values
x     = np.arange(len(prods)); w = 0.35

# RMSE
axes[0].bar(x-w/2, cross_df['LSTM RMSE'], w, label='LSTM', color='steelblue')
axes[0].bar(x+w/2, cross_df['GRU RMSE'],  w, label='GRU',  color='darkorange')
axes[0].set_xticks(x); axes[0].set_xticklabels([f'P{p}' for p in prods])
axes[0].set_title('RMSE by Product (Lower=Better)')
axes[0].set_ylabel('RMSE'); axes[0].legend(); axes[0].grid(True, alpha=0.3, axis='y')

# R2
axes[1].bar(x-w/2, cross_df['LSTM R2'], w, label='LSTM', color='steelblue')
axes[1].bar(x+w/2, cross_df['GRU R2'],  w, label='GRU',  color='darkorange')
axes[1].set_xticks(x); axes[1].set_xticklabels([f'P{p}' for p in prods])
axes[1].axhline(y=0.6, color='green', linestyle='--', alpha=0.7, label='Good (0.6)')
axes[1].set_title('R2 by Product (Higher=Better)')
axes[1].set_ylabel('R2'); axes[1].legend(); axes[1].grid(True, alpha=0.3, axis='y')

# Winner pie
axes[2].pie([lstm_rmse_wins, gru_rmse_wins], labels=['LSTM Wins','GRU Wins'],
            autopct='%1.1f%%', colors=['steelblue','darkorange'],
            explode=(0.05,0.05), shadow=True, startangle=90)
axes[2].set_title(f'RMSE Winners\n(LSTM {lstm_rmse_wins} vs GRU {gru_rmse_wins})')

plt.suptitle('Cross-Product Performance Comparison', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('product_level_comparison.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 26. Final Efficiency Summary

# In[38]:


la_rmse = lstm_results_df['RMSE'].mean()
la_mae  = lstm_results_df['MAE'].mean()
la_r2   = lstm_results_df['R2'].mean()
la_mape = lstm_results_df['MAPE'].mean()

ga_rmse = gru_results_df['RMSE'].mean()
ga_mae  = gru_results_df['MAE'].mean()
ga_r2   = gru_results_df['R2'].mean()
ga_mape = gru_results_df['MAPE'].mean()

def w(a, b, higher=False):
    return 'GRU' if (b > a if higher else b < a) else 'LSTM'

print('='*80)
print('FINAL EFFICIENCY COMPARISON: LSTM vs GRU')
print('='*80)
print(f"{'Metric':<28} {'LSTM':>14} {'GRU':>14} {'Winner':>12}")
print('-'*80)
print(f"{'Parameters':28} {lstm_params:>14,} {gru_params:>14,} {'LSTM' if lstm_params < gru_params else 'GRU':>12}")
print(f"{'Max Epochs':28} {'150':>14} {'200':>14} {'N/A':>12}")
print(f"{'Epochs Run':28} {lstm_epochs_run:>14} {gru_epochs_run:>14} {'N/A':>12}")
print(f"{'Batch Size':28} {'8':>14} {'16':>14} {'N/A':>12}")
print(f"{'Learning Rate':28} {'0.001':>14} {'0.0005':>14} {'N/A':>12}")
print(f"{'Training Time (s)':28} {lstm_training_time:>14.2f} {gru_training_time:>14.2f} {w(lstm_training_time, gru_training_time):>12}")
print('-'*80)
print(f"{'Avg RMSE':28} {la_rmse:>14.4f} {ga_rmse:>14.4f} {w(la_rmse, ga_rmse):>12}")
print(f"{'Avg MAE':28} {la_mae:>14.4f} {ga_mae:>14.4f} {w(la_mae, ga_mae):>12}")
print(f"{'Avg R2 Score':28} {la_r2:>14.4f} {ga_r2:>14.4f} {w(la_r2, ga_r2, higher=True):>12}")
print(f"{'Avg MAPE (%)':28} {la_mape:>14.4f} {ga_mape:>14.4f} {w(la_mape, ga_mape):>12}")
print('='*80)

pe_lstm = la_r2 / lstm_params * 1000
pe_gru  = ga_r2 / gru_params  * 1000
rmse_diff = (la_rmse - ga_rmse) / la_rmse * 100
r2_diff   = (ga_r2   - la_r2)   / abs(la_r2) * 100 if la_r2 != 0 else 0

print()
print('PARAMETER EFFICIENCY (R2 per 1K params):')
print(f'  LSTM : {pe_lstm:.6f}')
print(f'  GRU  : {pe_gru:.6f}')
print()
print('PERFORMANCE DELTA:')
print(f'  RMSE : {abs(rmse_diff):.2f}% ({"GRU better" if rmse_diff > 0 else "LSTM better"})')
print(f'  R2   : {abs(r2_diff):.2f}%  ({"GRU better" if r2_diff   > 0 else "LSTM better"})')
print()
print('TRAINING COST:')
print(f'  GRU is {gru_params/lstm_params:.2f}× the parameter count of LSTM')
print(f'  GRU training was {gru_training_time/lstm_training_time:.2f}× the time of LSTM')
print('='*80)


# ## 27. Conclusion
# 
# ### Key Architectural Differences
# 
# | | LSTM | GRU |
# |--|------|-----|
# | Gates | 3 (input / forget / output) | 2 (reset / update) |
# | Cell state | Separate cell state + hidden state | Single hidden state |
# | Layer 1 units | 64 | 128 |
# | Layer 2 units | 32 | 64 |
# | Dropout | 0.2 | 0.3 |
# | Dense stack | 1 layer | 2 layers |
# | Learning rate | 0.001 | 0.0005 |
# | Batch size | 8 | 16 |
# | Window size | **21 days** | **21 days** |
# | Max epochs | 150 | 200 |
# | EarlyStopping patience | 20 | 25 |
# 
# ### Improvements Made
# - **Window size 7 → 21**: Larger receptive field lets the model capture 3-week seasonality patterns
# - **Forecast function fixed**: Predicted values now properly feed into subsequent forecast steps
# - **1D-CNN front-end (Part 4)**: Local convolutional filters extract short-term patterns before the RNN
# 
# ### When to Use Each
# 
# | Scenario | Recommended |
# |----------|-------------|
# | Fastest training / fewest parameters | **LSTM** |
# | Small dataset (<500 samples) | **LSTM** |
# | Real-time / low-latency inference | **LSTM** |
# | Complex long-range dependencies | **LSTM** (extra gate helps) |
# | Best accuracy on time-series patterns | **CNN + LSTM** or **CNN + GRU** |
# | Rapid prototyping | **GRU** |
# 

# ---
# # ═══════════════════════════════════════
# # PART 4 — 1D-CNN + LSTM AND 1D-CNN + GRU
# # ═══════════════════════════════════════
# 
# **Why CNN in front of LSTM / GRU?**
# - A 1D Convolutional layer acts as a **local feature extractor**, learning short-term
#   temporal patterns (e.g., weekly cycles) before the RNN processes long-range dependencies.
# - The CNN reduces sequence length via pooling, which speeds up the RNN.
# - This hybrid architecture typically outperforms plain RNNs on noisy, real-world time series.
# 
# **Architecture:**
# ```
# Input (window=21, features=8)
#   └─ Conv1D(64, kernel_size=3, relu)
#        └─ MaxPooling1D(pool_size=2)
#             └─ Conv1D(32, kernel_size=3, relu)
#                  └─ [LSTM(64) or GRU(64)]
#                       └─ Dropout(0.2)
#                            └─ Dense(32, relu) → Dense(1)
# ```
# 

# ## 28. 1D-CNN + LSTM Model

# In[39]:


def build_cnn_lstm_model(input_shape):
    """
    Deep 1D-CNN + stacked LSTM:
    3 Conv blocks (64→128→256 filters) with BatchNorm.
    kernel_size=5 on block 1 captures 5-day weekly context.
    Single MaxPool preserves sequence length.
    Two LSTM layers (128→64) on the compressed sequence.
    MSE loss — consistent with LSTM/GRU baselines.
    """
    model = Sequential([
        Conv1D(64,  kernel_size=5, activation='relu', padding='same', input_shape=input_shape),
        BatchNormalization(), Dropout(0.1),
        Conv1D(128, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(), Dropout(0.1),
        Conv1D(256, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.15),
        LSTM(128, return_sequences=True,  kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        LSTM(64,  return_sequences=False, kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.0005), loss='mse', metrics=['mae'])
    return model

print('DEEP 1D-CNN + LSTM')
print('='*60)
_p = build_cnn_lstm_model(input_shape=(WINDOW_SIZE, len(FEATURE_COLS)))
_p.summary()


# ## 29. 1D-CNN + LSTM — Training

# In[40]:


cnn_lstm_early_stop = EarlyStopping(monitor='val_loss', patience=30,
                                     restore_best_weights=True, verbose=1)
cnn_lstm_reduce_lr  = ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                         patience=12, min_lr=1e-7, verbose=1)

cnn_lstm_model  = build_cnn_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
cnn_lstm_params = cnn_lstm_model.count_params()

X_cnn_lstm_aug = X_train + 0.005 * np.random.randn(*X_train.shape)

print('TRAINING DEEP CNN+LSTM')
print('='*60)
cnn_lstm_start = time.time()
cnn_lstm_history = cnn_lstm_model.fit(
    X_cnn_lstm_aug, y_train,
    epochs=300, batch_size=32,
    validation_split=0.15,
    callbacks=[cnn_lstm_early_stop, cnn_lstm_reduce_lr],
    verbose=1
)
cnn_lstm_time   = time.time() - cnn_lstm_start
cnn_lstm_epochs = len(cnn_lstm_history.history['loss'])
print(f'CNN+LSTM Training Time : {cnn_lstm_time:.2f}s | Epochs: {cnn_lstm_epochs}/300')


# ## 30. 1D-CNN + LSTM — Evaluation

# In[41]:


y_pred_cnn_lstm_scaled   = cnn_lstm_model.predict(X_test, verbose=0).flatten()
y_pred_cnn_lstm_original = lstm_scaler_y.inverse_transform(
    y_pred_cnn_lstm_scaled.reshape(-1, 1)).flatten()

cnn_lstm_mse  = mean_squared_error(y_test_original, y_pred_cnn_lstm_original)
cnn_lstm_rmse = np.sqrt(cnn_lstm_mse)
cnn_lstm_mae  = mean_absolute_error(y_test_original, y_pred_cnn_lstm_original)
cnn_lstm_r2   = r2_score(y_test_original, y_pred_cnn_lstm_original)
cnn_lstm_mape = np.mean(np.abs((y_test_original - y_pred_cnn_lstm_original)
                               / y_test_original)) * 100

print('1D-CNN + LSTM EVALUATION')
print('='*60)
print(f'MSE  : {cnn_lstm_mse:.4f}')
print(f'RMSE : {cnn_lstm_rmse:.4f}')
print(f'MAE  : {cnn_lstm_mae:.4f}')
print(f'R2   : {cnn_lstm_r2:.4f}')
print(f'MAPE : {cnn_lstm_mape:.2f}%')
print(f'Parameters    : {cnn_lstm_params:,}')
print(f'Epochs run    : {cnn_lstm_epochs}')
print(f'Training time : {cnn_lstm_time:.2f}s')


# In[42]:


residuals_cnn_lstm = y_test_original - y_pred_cnn_lstm_original
tidx = range(len(y_test_original))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Scatter
axes[0,0].scatter(y_test_original, y_pred_cnn_lstm_original,
                  alpha=0.6, edgecolors='black', lw=0.5, color='mediumseagreen')
lims = [y_test_original.min(), y_test_original.max()]
axes[0,0].plot(lims, lims, 'r--', lw=2, label='Perfect')
axes[0,0].set_title(f'CNN+LSTM — Predicted vs Actual  (R²={cnn_lstm_r2:.4f})')
axes[0,0].set_xlabel('Actual'); axes[0,0].set_ylabel('Predicted')
axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)

# Residual histogram
axes[0,1].hist(residuals_cnn_lstm, bins=20, edgecolor='black',
               alpha=0.7, color='mediumseagreen')
axes[0,1].axvline(x=0, color='red', linestyle='--', lw=2)
axes[0,1].set_title(f'CNN+LSTM — Residuals  (mean={residuals_cnn_lstm.mean():.2f})')
axes[0,1].set_xlabel('Residual'); axes[0,1].set_ylabel('Freq')
axes[0,1].grid(True, alpha=0.3)

# Actual vs Predicted time series
axes[1,0].plot(tidx, y_test_original,        'b-',  label='Actual',       lw=2, alpha=0.8)
axes[1,0].plot(tidx, y_pred_cnn_lstm_original,'g--', label='CNN+LSTM Pred', lw=2, alpha=0.9)
axes[1,0].fill_between(tidx, y_test_original, y_pred_cnn_lstm_original,
                        alpha=0.15, color='green')
axes[1,0].set_title('CNN+LSTM — Actual vs Predicted on Test Set')
axes[1,0].set_xlabel('Test Sample'); axes[1,0].set_ylabel('Units Sold')
axes[1,0].legend(); axes[1,0].grid(True, alpha=0.3)

# Residuals over time
axes[1,1].plot(tidx, residuals_cnn_lstm, color='mediumseagreen', lw=1.5)
axes[1,1].axhline(y=0, color='red', linestyle='--', lw=2)
sig = residuals_cnn_lstm.std()
axes[1,1].axhline(y= sig, color='orange', linestyle=':', lw=1.5, label=f'+1σ ({sig:.2f})')
axes[1,1].axhline(y=-sig, color='orange', linestyle=':', lw=1.5, label='-1σ')
axes[1,1].set_title('CNN+LSTM — Residuals Over Time')
axes[1,1].set_xlabel('Test Sample'); axes[1,1].set_ylabel('Residual')
axes[1,1].legend(); axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cnn_lstm_evaluation.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved 'cnn_lstm_evaluation.png'")


# ## 31. 1D-CNN + LSTM — 7-Day Forecast

# In[43]:


cnn_lstm_forecasts = forecast_future(
    cnn_lstm_model, X_test[-1:].copy(),
    lstm_scaler_X, lstm_scaler_y,
    FEATURE_COLS, n_days=7
)

print('='*60)
print('CNN+LSTM — 7-DAY SALES FORECAST')
print('='*60)
for i, f in enumerate(cnn_lstm_forecasts, 1):
    print(f'  Day {i}: {f:.0f} units')
print(f'\nTotal 7-day : {sum(cnn_lstm_forecasts):.0f} units')
print(f'Daily avg   : {np.mean(cnn_lstm_forecasts):.1f} units')

hist_days    = 14
recent_sales = product_df['units_sold'].iloc[-hist_days:].values
recent_dates = pd.date_range(end=product_df['date'].max(), periods=hist_days)
future_dates = pd.date_range(start=product_df['date'].max()+pd.Timedelta(days=1), periods=7)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(recent_dates, recent_sales, 'b-o', lw=2, label='Historical Sales', ms=6)
ax.plot(future_dates, cnn_lstm_forecasts, 'g--^', lw=2,
        label='CNN+LSTM Forecast', ms=8, color='mediumseagreen')
fstd = np.std(cnn_lstm_forecasts)
ax.fill_between(future_dates,
                [f - fstd for f in cnn_lstm_forecasts],
                [f + fstd for f in cnn_lstm_forecasts],
                alpha=0.2, color='green', label='±1 Std Dev')
ax.axvline(x=product_df['date'].max(), color='gray', linestyle=':', lw=2,
           alpha=0.7, label='Forecast Start')
ax.set_title('CNN+LSTM Sales Forecast — Product 1 (Next 7 Days)', fontsize=13)
ax.set_xlabel('Date'); ax.set_ylabel('Units Sold')
ax.legend(); ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cnn_lstm_forecast.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 32. 1D-CNN + GRU Model

# In[44]:


def build_cnn_gru_model(input_shape):
    model = Sequential([
        Conv1D(64,  kernel_size=5, activation='relu', padding='same', input_shape=input_shape),
        BatchNormalization(), Dropout(0.1),
        Conv1D(128, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(), Dropout(0.1),
        Conv1D(256, kernel_size=3, activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.15),
        GRU(128, return_sequences=True,  kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        GRU(64,  return_sequences=False, kernel_regularizer=regularizers.l2(1e-4)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.0005), loss='mse', metrics=['mae'])
    return model

print('DEEP 1D-CNN + GRU')
print('='*60)
_p2 = build_cnn_gru_model(input_shape=(WINDOW_SIZE, len(FEATURE_COLS)))
_p2.summary()


# ## 33. 1D-CNN + GRU — Training

# In[45]:


cnn_gru_early_stop = EarlyStopping(monitor='val_loss', patience=30,
                                    restore_best_weights=True, verbose=1)
cnn_gru_reduce_lr  = ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                        patience=12, min_lr=1e-7, verbose=1)

cnn_gru_model  = build_cnn_gru_model(input_shape=(Xg_train.shape[1], Xg_train.shape[2]))
cnn_gru_params = cnn_gru_model.count_params()

Xg_cnn_aug = Xg_train + 0.005 * np.random.randn(*Xg_train.shape)

print('TRAINING DEEP CNN+GRU')
print('='*60)
cnn_gru_start = time.time()
cnn_gru_history = cnn_gru_model.fit(
    Xg_cnn_aug, yg_train,
    epochs=300, batch_size=32,
    validation_split=0.15,
    callbacks=[cnn_gru_early_stop, cnn_gru_reduce_lr],
    verbose=1
)
cnn_gru_time   = time.time() - cnn_gru_start
cnn_gru_epochs = len(cnn_gru_history.history['loss'])
print(f'CNN+GRU Training Time : {cnn_gru_time:.2f}s | Epochs: {cnn_gru_epochs}/300')


# ## 34. 1D-CNN + GRU — Evaluation

# In[46]:


y_pred_cnn_gru_scaled   = cnn_gru_model.predict(Xg_test, verbose=0).flatten()
y_pred_cnn_gru_original = gru_scaler_y.inverse_transform(
    y_pred_cnn_gru_scaled.reshape(-1, 1)).flatten()

cnn_gru_mse  = mean_squared_error(yg_test_original, y_pred_cnn_gru_original)
cnn_gru_rmse = np.sqrt(cnn_gru_mse)
cnn_gru_mae  = mean_absolute_error(yg_test_original, y_pred_cnn_gru_original)
cnn_gru_r2   = r2_score(yg_test_original, y_pred_cnn_gru_original)
cnn_gru_mape = np.mean(np.abs((yg_test_original - y_pred_cnn_gru_original)
                              / yg_test_original)) * 100

print('1D-CNN + GRU EVALUATION')
print('='*60)
print(f'MSE  : {cnn_gru_mse:.4f}')
print(f'RMSE : {cnn_gru_rmse:.4f}')
print(f'MAE  : {cnn_gru_mae:.4f}')
print(f'R2   : {cnn_gru_r2:.4f}')
print(f'MAPE : {cnn_gru_mape:.2f}%')
print(f'Parameters    : {cnn_gru_params:,}')
print(f'Epochs run    : {cnn_gru_epochs}')
print(f'Training time : {cnn_gru_time:.2f}s')


# In[47]:


residuals_cnn_gru = yg_test_original - y_pred_cnn_gru_original
gidx = range(len(yg_test_original))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].scatter(yg_test_original, y_pred_cnn_gru_original,
                  alpha=0.6, edgecolors='black', lw=0.5, color='mediumpurple')
lims = [yg_test_original.min(), yg_test_original.max()]
axes[0,0].plot(lims, lims, 'r--', lw=2, label='Perfect')
axes[0,0].set_title(f'CNN+GRU — Predicted vs Actual  (R²={cnn_gru_r2:.4f})')
axes[0,0].set_xlabel('Actual'); axes[0,0].set_ylabel('Predicted')
axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)

axes[0,1].hist(residuals_cnn_gru, bins=20, edgecolor='black',
               alpha=0.7, color='mediumpurple')
axes[0,1].axvline(x=0, color='red', linestyle='--', lw=2)
axes[0,1].set_title(f'CNN+GRU — Residuals  (mean={residuals_cnn_gru.mean():.2f})')
axes[0,1].set_xlabel('Residual'); axes[0,1].set_ylabel('Freq')
axes[0,1].grid(True, alpha=0.3)

axes[1,0].plot(gidx, yg_test_original,       'b-',  label='Actual',      lw=2, alpha=0.8)
axes[1,0].plot(gidx, y_pred_cnn_gru_original,'m--',  label='CNN+GRU Pred', lw=2, alpha=0.9)
axes[1,0].fill_between(gidx, yg_test_original, y_pred_cnn_gru_original,
                        alpha=0.15, color='purple')
axes[1,0].set_title('CNN+GRU — Actual vs Predicted on Test Set')
axes[1,0].set_xlabel('Test Sample'); axes[1,0].set_ylabel('Units Sold')
axes[1,0].legend(); axes[1,0].grid(True, alpha=0.3)

axes[1,1].plot(gidx, residuals_cnn_gru, color='mediumpurple', lw=1.5)
axes[1,1].axhline(y=0, color='red', linestyle='--', lw=2)
sig2 = residuals_cnn_gru.std()
axes[1,1].axhline(y= sig2, color='orange', linestyle=':', lw=1.5, label=f'+1σ ({sig2:.2f})')
axes[1,1].axhline(y=-sig2, color='orange', linestyle=':', lw=1.5, label='-1σ')
axes[1,1].set_title('CNN+GRU — Residuals Over Time')
axes[1,1].set_xlabel('Test Sample'); axes[1,1].set_ylabel('Residual')
axes[1,1].legend(); axes[1,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cnn_gru_evaluation.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved 'cnn_gru_evaluation.png'")


# ## 35. 1D-CNN + GRU — 7-Day Forecast

# In[48]:


cnn_gru_forecasts = forecast_future(
    cnn_gru_model, Xg_test[-1:].copy(),
    gru_scaler_X, gru_scaler_y,
    FEATURE_COLS, n_days=7
)

print('='*60)
print('CNN+GRU — 7-DAY SALES FORECAST')
print('='*60)
for i, f in enumerate(cnn_gru_forecasts, 1):
    print(f'  Day {i}: {f:.0f} units')
print(f'\nTotal 7-day : {sum(cnn_gru_forecasts):.0f} units')
print(f'Daily avg   : {np.mean(cnn_gru_forecasts):.1f} units')

future_dates_cnn = pd.date_range(
    start=product_df_gru['date'].max()+pd.Timedelta(days=1), periods=7)
recent_dates_cnn = pd.date_range(end=product_df_gru['date'].max(), periods=14)
recent_sales_cnn = product_df_gru['units_sold'].iloc[-14:].values

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(recent_dates_cnn, recent_sales_cnn, 'b-o', lw=2, label='Historical Sales', ms=6)
ax.plot(future_dates_cnn, cnn_gru_forecasts, 'm--D', lw=2,
        label='CNN+GRU Forecast', ms=8, color='mediumpurple')
gfstd2 = np.std(cnn_gru_forecasts)
ax.fill_between(future_dates_cnn,
                [f - gfstd2 for f in cnn_gru_forecasts],
                [f + gfstd2 for f in cnn_gru_forecasts],
                alpha=0.2, color='purple', label='±1 Std Dev')
ax.axvline(x=product_df_gru['date'].max(), color='gray', linestyle=':', lw=2,
           alpha=0.7, label='Forecast Start')
ax.set_title('CNN+GRU Sales Forecast — Product 1 (Next 7 Days)', fontsize=13)
ax.set_xlabel('Date'); ax.set_ylabel('Units Sold')
ax.legend(); ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cnn_gru_forecast.png', dpi=150, bbox_inches='tight')
plt.show()


# ## 36. All Four Models — Head-to-Head Comparison

# In[49]:


# ── Final comparison table: LSTM vs GRU vs CNN+LSTM vs CNN+GRU ──
def w4(vals, higher=False):
    """Return label of the best value among four."""
    labels = ['LSTM','GRU','CNN+LSTM','CNN+GRU']
    idx = np.argmax(vals) if higher else np.argmin(vals)
    return labels[idx] + ' ✓'

all_rmse  = [lstm_rmse,  gru_rmse,  cnn_lstm_rmse,  cnn_gru_rmse]
all_mae   = [lstm_mae,   gru_mae,   cnn_lstm_mae,   cnn_gru_mae]
all_r2    = [lstm_r2,    gru_r2,    cnn_lstm_r2,    cnn_gru_r2]
all_mape  = [lstm_mape,  gru_mape,  cnn_lstm_mape,  cnn_gru_mape]
all_time  = [lstm_training_time, gru_training_time, cnn_lstm_time, cnn_gru_time]
all_params= [lstm_params, gru_params, cnn_lstm_params, cnn_gru_params]

final_df = pd.DataFrame({
    'Metric' : ['RMSE','MAE','R2','MAPE (%)','Training Time (s)','Parameters'],
    'LSTM'   : [f'{lstm_rmse:.4f}',  f'{lstm_mae:.4f}',  f'{lstm_r2:.4f}',
                f'{lstm_mape:.2f}',  f'{lstm_training_time:.1f}',  f'{lstm_params:,}'],
    'GRU'    : [f'{gru_rmse:.4f}',   f'{gru_mae:.4f}',   f'{gru_r2:.4f}',
                f'{gru_mape:.2f}',   f'{gru_training_time:.1f}',   f'{gru_params:,}'],
    'CNN+LSTM': [f'{cnn_lstm_rmse:.4f}', f'{cnn_lstm_mae:.4f}', f'{cnn_lstm_r2:.4f}',
                 f'{cnn_lstm_mape:.2f}', f'{cnn_lstm_time:.1f}',  f'{cnn_lstm_params:,}'],
    'CNN+GRU' : [f'{cnn_gru_rmse:.4f}',  f'{cnn_gru_mae:.4f}',  f'{cnn_gru_r2:.4f}',
                 f'{cnn_gru_mape:.2f}',  f'{cnn_gru_time:.1f}',   f'{cnn_gru_params:,}'],
    'Best'   : [
        w4(all_rmse), w4(all_mae), w4(all_r2, higher=True),
        w4(all_mape), w4(all_time), w4(all_params)
    ]
})

print('='*90)
print('ALL MODELS — HEAD-TO-HEAD COMPARISON (Product 1, window=21)')
print('='*90)
print(final_df.to_string(index=False))


# In[50]:


# ── Visual head-to-head ──
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

model_names = ['LSTM', 'GRU', 'CNN+LSTM', 'CNN+GRU']
colors4 = ['steelblue', 'darkorange', 'mediumseagreen', 'mediumpurple']
x4 = np.arange(4)

# RMSE
bars = axes[0,0].bar(model_names, all_rmse, color=colors4, edgecolor='black')
axes[0,0].set_title('RMSE (Lower = Better)')
axes[0,0].set_ylabel('RMSE'); axes[0,0].grid(True, alpha=0.3, axis='y')
for bar, v in zip(bars, all_rmse):
    axes[0,0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                   f'{v:.3f}', ha='center', va='bottom', fontsize=9)

# MAE
bars = axes[0,1].bar(model_names, all_mae, color=colors4, edgecolor='black')
axes[0,1].set_title('MAE (Lower = Better)')
axes[0,1].set_ylabel('MAE'); axes[0,1].grid(True, alpha=0.3, axis='y')
for bar, v in zip(bars, all_mae):
    axes[0,1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                   f'{v:.3f}', ha='center', va='bottom', fontsize=9)

# R2
bars = axes[0,2].bar(model_names, all_r2, color=colors4, edgecolor='black')
axes[0,2].axhline(y=0.6, color='green',     linestyle='--', alpha=0.6, label='Good (0.6)')
axes[0,2].axhline(y=0.8, color='darkgreen', linestyle='--', alpha=0.6, label='Excellent (0.8)')
axes[0,2].set_title('R² Score (Higher = Better)')
axes[0,2].set_ylabel('R²'); axes[0,2].legend(fontsize=8)
axes[0,2].grid(True, alpha=0.3, axis='y')
for bar, v in zip(bars, all_r2):
    axes[0,2].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005,
                   f'{v:.3f}', ha='center', va='bottom', fontsize=9)

# MAPE
bars = axes[1,0].bar(model_names, all_mape, color=colors4, edgecolor='black')
axes[1,0].set_title('MAPE % (Lower = Better)')
axes[1,0].set_ylabel('MAPE (%)'); axes[1,0].grid(True, alpha=0.3, axis='y')
for bar, v in zip(bars, all_mape):
    axes[1,0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                   f'{v:.1f}%', ha='center', va='bottom', fontsize=9)

# Training time
bars = axes[1,1].bar(model_names, all_time, color=colors4, edgecolor='black')
axes[1,1].set_title('Training Time (s) — Lower = Faster')
axes[1,1].set_ylabel('Seconds'); axes[1,1].grid(True, alpha=0.3, axis='y')
for bar, v in zip(bars, all_time):
    axes[1,1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
                   f'{v:.1f}s', ha='center', va='bottom', fontsize=9)

# Actual vs all preds (test set)
common = min(len(y_test_original), len(yg_test_original))
tidx4  = range(common)
axes[1,2].plot(tidx4, y_test_original[:common],          'k-',  label='Actual',    lw=2, alpha=0.9)
axes[1,2].plot(tidx4, y_pred_lstm_original[:common],     'b--', label='LSTM',      lw=1.5, alpha=0.8)
axes[1,2].plot(tidx4, y_pred_gru_original[:common],      '--',  label='GRU',       lw=1.5, alpha=0.8, color='darkorange')
axes[1,2].plot(tidx4, y_pred_cnn_lstm_original[:common], 'g-.',  label='CNN+LSTM',  lw=1.5, alpha=0.85)
axes[1,2].plot(tidx4, y_pred_cnn_gru_original[:common],  'm-.',  label='CNN+GRU',   lw=1.5, alpha=0.85)
axes[1,2].set_title('All Models — Actual vs Predicted (Test Set)')
axes[1,2].set_xlabel('Test Sample'); axes[1,2].set_ylabel('Units Sold')
axes[1,2].legend(fontsize=8); axes[1,2].grid(True, alpha=0.3)

plt.suptitle('All Four Models — Head-to-Head (window=21)', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('all_models_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved 'all_models_comparison.png'")


# ## 37. Part 4 — Summary
# 
# ### Why CNN + RNN Works Better
# 
# | Stage | Role |
# |-------|------|
# | `Conv1D (kernel=3)` | Detects short local patterns (e.g. 3-day spikes, weekend effects) |
# | `MaxPooling1D` | Reduces sequence length → faster RNN, reduced overfitting |
# | `LSTM / GRU` | Captures long-range dependencies in the compressed sequence |
# | `Dense` | Maps learned representation to the sales forecast |
# 
# ### Key Takeaways from Mentor Feedback
# 1. **Window size 7 → 21**: Exposes the model to three full weeks of history,
#    capturing weekly seasonality (weekday effects show up clearly in this data).
# 2. **Forecast function fix**: The original `np.roll` approach recycled stale
#    historical values; the corrected version injects each predicted value back
#    into the sliding window so future steps are informed by model predictions.
# 3. **CNN front-end**: Acts as a learned feature extractor before the RNN,
#    improving the predicted curve's ability to follow the actual curve.
# 
