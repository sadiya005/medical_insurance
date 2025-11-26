# ✨ Medical Insurance Cost Prediction

This project predicts **medical insurance costs** for customers using machine learning. It simulates a real-world scenario where data science is applied end-to-end — from **data cleaning** and **feature engineering** to **model building** and **real-time deployment**.

---

## 📌 Project Overview

The objective is to build a predictive system that estimates medical insurance costs based on customer information. This project covers:

- **Data cleaning and preprocessing**
- **Exploratory Data Analysis (EDA) and outlier analysis**
- **Feature engineering**
- **Model building and evaluation**
- **Real-time prediction through FastAPI and Streamlit**
- **Deployment using Docker**

This demonstrates a complete data science workflow, highlighting practical applications of machine learning in the insurance industry.

---

## 🛠️ Project Workflow

### 1️⃣ Data Cleaning & Preprocessing
- Handling missing values and inconsistent entries  
- Outlier analysis to improve model quality  
- Encoding categorical variables (e.g., one-hot encoding for gender, smoker status)  

### 2️⃣ Exploratory Data Analysis (EDA)
- Visualized distributions of key features such as age, BMI, and charges  
- Analyzed relationships between features and insurance costs  
- Identified trends and patterns in the data  

### 3️⃣ Feature Engineering
- Created new features based on age and BMI
- Added other relevant features to improve model performance

### 4️⃣ Model Building
- Built predictive model using **XGBoost**  
- Applied **cross-validation** and **grid search** for hyperparameter tuning   
- Saved final model as a `.pkl` file for deployment  

### 5️⃣ Real-Time Prediction
- Developed **FastAPI** backend for serving predictions  
- Built **Streamlit dashboard** for interactive user input and prediction display  
- Designed project for **real-time prediction** scenarios  

### 6️⃣ Deployment
-  Containerised the application using **Docker**
- Deployed the container on **Render** for cloud-based real-time predictions
- Users can access the **interactive dashboard** online via the deployed URL
- FastAPI backend runs inside the container for serving prediction requests

Live deployment link: [https://insurance-prediction-latest.onrender.com]

---

## 📁 Files Included
- `insurance_data_cleaning.ipynb` – Data cleaning, outlier analysis, and preprocessing  
- `insurance_model_building.ipynb` – Feature engineering, model training, and evaluation  
- `model/insurance_model.pkl` – Saved trained model  
- `app.py` – FastAPI backend  
- `streamlit_app.py` – Streamlit dashboard  
- `Dockerfile` – Containerization setup  
- `README.md` – Project documentation  

---

## 🔍 Key Insights
- Outlier analysis revealed extreme values in **BMI** and **charges**, which were handled to improve model stability  
- Age, BMI, and smoking status are major predictors of insurance costs  
- One-hot encoding of categorical variables improved model interpretability and performance  
- XGBoost with cross-validation provided robust predictions  

---

## 🧰 Tools & Libraries
- **Python** – Programming language  
- **Pandas, NumPy** – Data handling  
- **Seaborn, Matplotlib** – Visualization  
- **Scikit-learn, XGBoost** – Machine Learning  
- **FastAPI** – Backend API  
- **Streamlit** – Interactive dashboard  
- **Docker** – Containerization  

---

## 🚀 Next Steps
- Enhance the dashboard with additional visual insights
- Explore alternative models and ensemble techniques for improved accuracy
- Monitor and optimize deployed service for performance and scalability  

---

## 👩‍💻 Author
**Sadiya Sajid**   

🔗 [LinkedIn](https://www.linkedin.com/in/sadiyasajid/)

---

## 🎯 Why This Project Matters
This project demonstrates **end-to-end machine learning workflow** in a real-world scenario — from **data cleaning and outlier analysis** to **model deployment for real-time prediction**. It showcases how data science can provide actionable insights and automate decision-making in the insurance industry.
