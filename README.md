# Prisight 🔍📊  
**AI-Powered Product Demand & Pricing Intelligence Platform**

Prisight is a full-stack analytics platform built using **React** and **FastAPI** to deliver data-driven insights on product demand, pricing, and sales performance.  
The platform combines a scalable backend architecture with an interactive frontend dashboard to demonstrate real-world business intelligence and forecasting workflows.

This project was collaboratively developed with a focus on:
- Full-stack application development
- Analytics-ready backend systems
- Forecasting and evaluation pipelines
- Clean software engineering practices

---

## 🚀 Key Features

### 📊 Analytics & Intelligence
- 📈 **Demand Forecasting**
  - Predicts future product demand using historical sales data
  - Product-wise time-series forecasting support

- 💰 **Pricing & Performance Insights**
  - Analyzes pricing trends and product performance
  - Designed for AI/ML-driven recommendations

- 🧠 **Insight Generation Layer**
  - Structured NLP-style insight storage
  - Extendable for LLM-powered business intelligence

---

### 🖥 Frontend (React)
- Modern React-based user interface
- Dashboard-ready architecture
- API-driven dynamic data rendering
- Modular component structure for scalability
- Built for future charting and visualization support

---

### 🗄 Backend & Data
- FastAPI-powered REST APIs
- Structured relational database models
- Forecast storage and evaluation tracking
- Analytics-ready backend design
- Environment-safe configuration

---

## 🛠️ Tech Stack

### Frontend
- **React**
- **JavaScript (ES6+)**
- **Axios**
- **Vite**

### Backend
- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**

### Data & Analytics
- Demand forecasting models
- Evaluation metrics:
  - MAE (Mean Absolute Error)
  - RMSE (Root Mean Squared Error)
  - MAPE (Mean Absolute Percentage Error)

### Development & Tooling
- Git & GitHub
- Virtual environments
- Modular architecture
- Clean repository management

---

## 📂 Project Structure

```text
Prisight/
│
├── Frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Application pages
│   │   ├── services/        # API communication layer
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── Backend/
│   ├── app/                 # FastAPI application logic
│   ├── models/              # Database & analytics models
│   ├── run.py               # Backend entry point
│   ├── req.txt              # Python dependencies
│   ├── products.csv         # Sample product data
│   ├── sales.csv            # Sample sales data
│   └── prisight.db          # Local development database
│
├── .gitignore
└── README.md
````

---

## 🧪 Core Data Models

* **Product**
* **DemandForecast**
* **ModelEvaluation**
* **NLPInsight**

These models collectively enable:

* Product analytics
* Forecast generation
* Model evaluation
* AI-driven insight management

---

## ⚙️ Setup & Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/AviRedDevil/Prisight.git
cd Prisight
```

---

## 🔧 Backend Setup

### Create Virtual Environment

```bash
cd Backend
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r req.txt
```

### Run Backend Server

```bash
python run.py
```

Backend will run on:

```text
http://localhost:8000
```

---

## 🖥 Frontend Setup

### Navigate to Frontend

```bash
cd ../Frontend
```

### Install Dependencies

```bash
npm install
```

### Start Development Server

```bash
npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

## 🔗 Frontend–Backend Integration

* React frontend communicates with FastAPI backend through REST APIs
* Axios is used for API communication
* Backend serves forecasting and analytics data dynamically
* Designed for future integration with charts and real-time analytics

---

## 👥 Team Collaboration

Prisight was developed as a collaborative full-stack project with contributions across:

* Backend architecture and API development
* Database and analytics model design
* Forecasting logic and evaluation workflows
* Frontend UI development using React
* Full-stack integration and repository management

The project emphasizes clean architecture, modularity, and scalable development practices.

---

## 🎯 Use Cases

* Product demand forecasting
* Business intelligence systems
* Pricing trend analysis
* Inventory planning support
* AI-powered analytics platforms

---

## 🔮 Future Enhancements

* Advanced machine learning integration
* LLM-powered insight explanations
* Interactive analytics dashboards
* Role-based authentication
* Cloud deployment (AWS / Render / Railway)
* Real-time data pipelines

---

## 📌 Repository Notes

* Virtual environments (`.venv`) are excluded from version control
* Sensitive environment variables are not committed
* Dependencies are managed via `req.txt` and `package.json`

---

## 📄 License

This project is intended for educational and demonstrative purposes and can be extended for real-world deployments.

```
```
