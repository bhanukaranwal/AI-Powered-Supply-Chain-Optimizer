# 📦 AI-Powered Supply Chain Optimizer

A Python-based end-to-end project that uses AI to **forecast demand** (Prophet) and **optimize delivery routes** (Google OR-Tools).  
Contains:
- **FastAPI** backend
- **Streamlit** frontend dashboard
- **Unit tests**
- **Docker deployment support**

---

## 🚀 Features
- **Demand Forecasting**: Predict future demand using Prophet time-series forecasting.
- **Route Optimization**: Solve vehicle routing problems with Google OR-Tools.
- **REST API**: Serve predictions and route plans via FastAPI.
- **Interactive Dashboard**: Visualize forecasts and maps with Streamlit + Plotly.

---

## 📂 Project Structure
supply-chain-optimizer/
├── data/ # Generated datasets (sales, locations)
├── src/ # Core modules
├── tests/ # Unit tests
├── app.py # Streamlit UI
├── Dockerfile # Deployment config
├── requirements.txt # Dependencies
└── README.md # This file

---

## ⚙️ Installation & Setup

**1️⃣ Clone the repository**
git clone https://github.com/your-username/supply-chain-optimizer.git
cd supply-chain-optimizer

**2️⃣ Install dependencies**
pip install -r requirements.txt

**3️⃣ Generate sample data**
python -c "from src.utils import generate_synthetic_sales_data, generate_synthetic_locations; generate_synthetic_sales_data(); generate_synthetic_locations()"

---

## 💻 Running Locally

**Run FastAPI Backend**
uvicorn src.api:app --reload
Access docs: `http://localhost:8000/docs`

**Run Streamlit Frontend**
streamlit run app.py
Access: `http://localhost:8501`

---

## 🧪 Running Tests
pytest tests/

---

## 🐳 Running via Docker
Build image
docker build -t supply-chain-optimizer .

Run container (FastAPI backend)
docker run -p 8000:8000 supply-chain-optimizer

---

## 📌 Notes
- Replace synthetic data with real supply chain datasets for production.
- Extend for multiple products & dynamic routing updates.
- Add authentication for production API usage.

---

## 📄 License
MIT License – see `LICENSE` for details.
