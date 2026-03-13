# mini-project

**Operations Intelligence for Quick-Commerce Logistics**

This project transforms fragmented quick-commerce datasets into an **Interactive Visual Analytics Framework** and a **Delivery Risk Predictor**.

## 🚀 Getting Started (For Teammates)
1. **Clone the repo:**
   `git clone https://github.com/your-username/q-comm-pulse.git`
2. **Setup Environment:**
   `conda activate mini_project`
3. **Install Dependencies:**
   `pip install streamlit pandas plotly scikit-learn matplotlib joblib`

## 🛠️ Project Components
- **The Brain:** `ml_model.py` trains a Random Forest model to predict delays based on distance, area, and time.
- **The Face:** `app.py` is the Streamlit dashboard providing real-time operational insights.
- **The Data:** `Blinkit_Master_Data.csv` is our cleaned "Golden Dataset" (5,000 rows).

## 📊 Business Logic
We prioritize **Recall** over Precision. It is better to warn a customer about a potential delay (False Positive) than to promise speed and fail (False Negative).