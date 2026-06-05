<div align="center">

```
██████╗ ██████╗ ██╗███████╗██╗ ██████╗ ██╗  ██╗████████╗
██╔══██╗██╔══██╗██║██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝
██████╔╝██████╔╝██║███████╗██║██║  ███╗███████║   ██║   
██╔═══╝ ██╔══██╗██║╚════██║██║██║   ██║██╔══██║   ██║   
██║     ██║  ██║██║███████║██║╚██████╔╝██║  ██║   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝  
```

### *See the market before it moves.*

---

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![SQLite](https://img.shields.io/badge/SQLite-Async-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](./LICENSE)

</div>

---

## 🔭 What is Prisight?

> **Prisight** is a full-stack AI-powered platform for **demand forecasting**, **dynamic pricing**, and **market intelligence** — built for businesses that want to stop guessing and start knowing.

It fuses classical statistical models *(ARIMA)* with deep learning architectures *(LSTM, GRU, CNN-LSTM, Transformer)* to give you predictions that actually age well. Layer on top a real-time pricing engine, competitor analysis, and NLP-generated insights — and you have a single command center for every revenue-critical decision.

Whether you're a solo founder managing inventory or a data team evaluating neural architectures, Prisight speaks your language.

---

## ✨ Feature Highlights

| 🧠 Intelligence | ⚙️ Engineering | 📊 Analytics |
|---|---|---|
| ARIMA demand forecasting | Async FastAPI backend | Price elasticity engine |
| LSTM / GRU / CNN-LSTM models | SQLAlchemy ORM (async) | Model evaluation (MAE, RMSE, MAPE) |
| Transformer architecture | JWT authentication | Admin leaderboard & tuning |
| NLP business insights | RESTful API (16 routers) | Actual vs. predicted charts |
| Competitor price tracking | React 18 + Vite frontend | Promotion ROI estimator |
| Dynamic pricing recommendations | Hyperparameter tuning UI | KPI dashboard cards |

---

## 🗺️ Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRISIGHT PLATFORM                        │
├─────────────────┬───────────────────────┬───────────────────────┤
│   REACT FRONTEND│    FASTAPI BACKEND     │    ML / AI LAYER      │
│                 │                       │                       │
│  Dashboard      │  /products            │  ARIMA Forecasting    │
│  Pricing Page   │  /sales               │  LSTM / GRU Networks  │
│  Inventory Page │  /forecast            │  CNN-LSTM Hybrid      │
│  Promotions     │  /pricing             │  Transformer Model    │
│  Admin Panel    │  /market              │  Price Elasticity     │
│  Model Eval UI  │  /elasticity          │  NLP Insights Engine  │
│                 │  /promotions          │                       │
│  Vite + Axios   │  /inventory           │  TensorFlow           │
│  React 18       │  /nlp                 │  scikit-learn         │
│                 │  /api (admin)         │  statsmodels          │
├─────────────────┴───────────────────────┴───────────────────────┤
│                     SQLite (prisight.db)                        │
│        11 core tables  •  3 admin/ML tables  •  async I/O       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

<details>
<summary><b>📦 Core Tables (click to expand)</b></summary>

<br>

| Table | Purpose | Key Fields |
|---|---|---|
| `users` | Auth & accounts | `uid`, `username`, `email`, `password`, `is_admin` |
| `products` | Product catalog | `sku`, `name`, `category`, `brand`, `cost_price`, `current_price` |
| `sales_history` | Historical sales | `product_id`, `date`, `units_sold`, `selling_price` |
| `demand_forecasts` | ARIMA predictions | `product_id`, `forecast_date`, `predicted_units` |
| `market_prices` | Competitor data | `product_name`, `brand`, `source`, `price`, `date_collected` |
| `elasticities` | Price sensitivity | `product_id`, `elasticity_value`, `avg_price`, `avg_units_sold` |
| `price_recommendations` | AI pricing | `product_id`, `recommended_price`, `elasticity`, `reasoning` |
| `model_evaluations` | ML metrics | `product_id`, `mae`, `rmse`, `mape`, `samples` |
| `promotion_recommendations` | Campaign ideas | `promotion_type`, `discount_percent`, `expected_revenue` |
| `nlp_insights` | Business insights | `product_id`, `insight_type`, `content` |
| `inventory` | Stock tracking | `product_id`, `current_stock`, `daily_holding_cost`, `lead_time_days` |

</details>

<details>
<summary><b>🤖 Admin / ML Tables (click to expand)</b></summary>

<br>

| Table | Purpose | Key Fields |
|---|---|---|
| `admin_model_evaluations` | Model benchmarks | `model_name`, `rmse`, `mae`, `r2_score`, `mape`, `epochs`, `training_time` |
| `admin_model_predictions` | Actual vs predicted | `evaluation_id`, `timestep`, `actual_value`, `predicted_value`, `residual` |
| `admin_training_history` | Epoch-level loss | `evaluation_id`, `epoch`, `loss`, `val_loss`, `mae`, `val_mae` |

</details>

---

## 🧱 Tech Stack

```
FRONTEND                 BACKEND                  ML / DATA
─────────────────────    ─────────────────────    ─────────────────────
React 18                 FastAPI                  TensorFlow 2.x
Vite                     Python 3.12              scikit-learn
Axios                    Uvicorn                  statsmodels
JavaScript ES6+          SQLAlchemy (async)       pandas / numpy
                         aiosqlite                ARIMA / LSTM / GRU
                         python-jose (JWT)        CNN-LSTM / Transformer
                         bcrypt                   Matplotlib / Seaborn
```

---

## 📁 Project Structure

```
Prisight/
│
├── Backend/
│   └── app/
│       ├── main.py                    ← FastAPI entry point
│       ├── database.py                ← Async DB setup
│       ├── models/                    ← 14 SQLAlchemy models
│       ├── routers/                   ← 16 API routers
│       ├── Services/                  ← 14 business logic services
│       ├── ML/                        ← ML utilities & helpers
│       ├── admin/                     ← Admin models, routers, services
│       └── utils/                     ← Shared utilities
│
├── frontend/
│   └── src/
│       ├── App.jsx / Dashboard.jsx    ← Core pages
│       ├── components/
│       │   ├── DemandChart.jsx        ← Time-series visualization
│       │   ├── PricingCard.jsx        ← Price recommendation widget
│       │   ├── InventoryCard.jsx      ← Stock level display
│       │   ├── PromotionCard.jsx      ← Campaign suggestions
│       │   ├── KpiCard.jsx            ← Business KPI display
│       │   ├── Sidebar.jsx            ← Navigation
│       │   └── admin/                 ← Model comparison charts, tables
│       ├── pages/
│       │   ├── Inventory.jsx
│       │   ├── Pricing.jsx
│       │   ├── Promotions.jsx
│       │   └── admin/
│       │       ├── ModelEvaluation.jsx
│       │       ├── ModelLeaderboard.jsx
│       │       └── HyperparameterTuning.jsx
│       └── services/
│           ├── api.js                 ← Base Axios client
│           └── adminApi.js            ← Admin endpoints
│
└── Model Evaluation/
    ├── Prisight_enhancement_notebook_1.ipynb   ← LSTM vs GRU vs CNN
    └── Prisight_enhancement_notebook_2.ipynb   ← LSTM vs Transformer
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have these installed before you begin:

- **Python 3.12+** — [Download](https://python.org/downloads)
- **Node.js 18+** — [Download](https://nodejs.org)
- **Git** — [Download](https://git-scm.com)

---

### 1 · Clone the Repository

```bash
git clone https://github.com/yourusername/prisight.git
cd prisight
```

---

### 2 · Set Up the Backend

```bash
# Navigate to the backend folder
cd Backend

# Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install all dependencies
pip install -r req.txt
```

---

### 3 · Start the Backend Server

```bash
python run.py
```

> ✅ The API will be live at **`http://localhost:8000`**  
> 📖 Auto-generated docs available at **`http://localhost:8000/docs`**

---

### 4 · Set Up the Frontend

```bash
# Open a new terminal, navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

> ✅ The app will be running at **`http://localhost:5173`**

---

### 5 · You're in. 🎉

Open your browser to `http://localhost:5173`, register an account, and start exploring demand forecasts, pricing recommendations, and market intelligence — all in one place.

---

## 🤖 ML Models Explained

*Not a machine learning expert? No problem. Here's what each model does in plain English.*

<details>
<summary><b>📈 ARIMA — The Classic Statistician</b></summary>

**What it does:** Looks at your past sales data and finds patterns — trends, seasonal cycles, noise — to project what demand will look like next week or next month.

**Best for:** Products with consistent historical data and predictable seasonality.

**Why it's here:** It's interpretable, fast, and a solid baseline. Great for business users who want to understand *why* a forecast is what it is.

</details>

<details>
<summary><b>🧠 LSTM — The Memory Machine</b></summary>

**What it does:** A type of neural network that has "memory" — it can learn from sequences of data over time, catching long-range dependencies that ARIMA misses.

**Best for:** Complex, non-linear demand patterns — like products that spike around events, competitor launches, or economic shifts.

**Why it's here:** When patterns are too complex for statistics alone, deep learning steps in.

</details>

<details>
<summary><b>⚡ GRU — LSTM's Leaner Sibling</b></summary>

**What it does:** Similar to LSTM, but with a simpler architecture — fewer parameters, faster training, often comparable accuracy.

**Best for:** When you need LSTM-level power but want quicker iteration and lower compute cost.

</details>

<details>
<summary><b>🔭 CNN-LSTM / CNN-GRU — Pattern Detector + Memory</b></summary>

**What it does:** A hybrid model. The CNN layer scans for local patterns in the data (like a feature detector), then passes them to LSTM/GRU for sequence reasoning.

**Best for:** Noisy data where local feature extraction helps before sequence modeling.

</details>

<details>
<summary><b>🤖 Transformer — The Attention Powerhouse</b></summary>

**What it does:** Doesn't process data sequentially — instead, it uses "attention" to weigh the importance of every past time step when making predictions. The same architecture behind GPT and BERT.

**Best for:** Long sequences with complex dependencies where every historical point might matter.

</details>

---
[![GitHub](https://img.shields.io/badge/GitHub-avi03--dev--oi%2FPrisight-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/avi03-dev-oi/Prisight)

## 🔌 API Reference

The backend exposes **16 RESTful routers**. Here's a quick map:

| Prefix | Router | What it does |
|---|---|---|
| `/users` | Auth | Register, login, JWT tokens |
| `/products` | Products | CRUD for product catalog |
| `/sales` | Sales | Log and retrieve sales records |
| `/forecast` | Forecast | Run ARIMA demand forecasts |
| `/lstm` | LSTM | Run LSTM/GRU/CNN forecasts |
| `/pricing` | Pricing | Get AI price recommendations |
| `/market` | Market | Competitor pricing data |
| `/elasticity` | Elasticity | Calculate price sensitivity |
| `/inventory` | Inventory | Stock level management |
| `/promotions` | Promotions | Promotional strategy suggestions |
| `/evaluation` | Evaluation | Per-product model metrics |
| `/nlp` | NLP | Generate AI business insights |
| `/features` | Features | ML feature engineering |
| `/api` (admin) | Admin Eval | Model comparison & benchmarks |
| `/api` (tuning) | Tuning | Hyperparameter optimization |
| `/api` (board) | Leaderboard | Model performance rankings |

> 💡 **Tip:** Visit `http://localhost:8000/docs` for the full interactive Swagger UI — every endpoint, parameter, and response schema, live.

---

## 📓 Jupyter Notebooks

The `Model Evaluation/` directory contains research notebooks for deep-diving into model architecture comparisons:

### `Prisight_enhancement_notebook_1.ipynb`
> **LSTM vs GRU vs CNN-LSTM vs CNN-GRU**

Compares four architectures head-to-head on the same dataset. Covers data preprocessing, architecture design, training pipelines, and a full evaluation suite (RMSE, MAE, R², MAPE).

### `Prisight_enhancement_notebook_2.ipynb`
> **LSTM vs Transformer**

Pits the dominant sequential model against the attention-based Transformer. Ideal for understanding trade-offs in accuracy, training time, and model complexity.

---

## 🛡️ Authentication

Prisight uses **JWT (JSON Web Tokens)** for stateless authentication:

- Passwords are hashed with **bcrypt** before storage — never stored in plain text
- Tokens are issued on login and must be included in the `Authorization` header for protected routes
- Admin routes are gated behind `is_admin` flag in the `users` table

---

## 🤝 Contributing

Contributions are welcome and appreciated. Here's how to get involved:

```bash
# 1. Fork the repository on GitHub

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes and commit
git commit -m "feat: add your feature description"

# 4. Push to your fork
git push origin feature/your-feature-name

# 5. Open a Pull Request on GitHub
```

Please make sure your code follows existing style conventions and includes relevant tests where applicable.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

**Built with precision. Powered by intelligence.**

*Prisight — where data becomes decisions.*

---

⭐ If this project helped you, consider giving it a star on GitHub!

</div>
