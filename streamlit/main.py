import streamlit as st
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
from PIL import Image
import base64
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ---------------------------#
# 🎨 Page Config & Title
# ---------------------------#
st.set_page_config(
    page_title="Medical Insurance Predictor 💸",
    page_icon="💊",
    layout="centered"
)

# Get the correct path relative to this file
image_path = os.path.join(os.path.dirname(__file__), "Medical Insurance BG.jpg")


# Encode the image to base64
with open(image_path, "rb") as f:
    img_bytes = f.read()
    encoded = base64.b64encode(img_bytes).decode()

# Use the base64 string in CSS with transparency overlay
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255,0.9)),
            url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)




# ---------------------------#
# 💫 Fixed Title
# ---------------------------#
st.markdown("""
<style>
.stApp header {position: fixed;}
h1 {text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("💸 Medical Insurance Predictor")
st.markdown("---")

# ---------------------------#
# 👤 Personal Info Section
# ---------------------------#
st.subheader("🧍‍♀️ Personal Information")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", key="name")
    age = st.number_input("Age", min_value=1, max_value=120, key="age")
    sex = st.selectbox("Gender", ["male", "female", "others"],index=0, key="sex")
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"],index=0,key="region")
with col2:
    phone = st.text_input("Phone Number (10 digits)",key="phone")
    email = st.text_input("Email Address", key="email")
    children = st.number_input("Children", min_value=0, step=1, key="children")
    smoker = st.radio("Do you smoke?", ["Yes", "No"], index=1, key="smoker")

# ---------------------------#
# ⚕️ Health Info
# ---------------------------#
st.subheader("⚕️ Health Details")
weight = st.number_input("Weight (kg)", min_value=1, key="weight")
height = st.number_input("Height (m)", min_value=0.5, max_value=3.0, key="height")
bmi = round(weight / (height ** 2), 2) if height > 0 else None
if bmi:
    st.info(f"Your BMI: **{bmi}**")

# ---------------------------#
# ✅ Validation
# ---------------------------#
def validate_inputs(name, phone, email):
    if not name.strip():
        st.warning("⚠️ Name cannot be empty.")
        return False
    if not re.fullmatch(r"\d{10}", phone):
        st.warning("⚠️ Enter a valid 10-digit phone number.")
        return False
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        st.warning("⚠️ Enter a valid email address.")
        return False
    return True

# ---------------------------#
# 🚀 Prediction
# ---------------------------#
if st.button("🔍 Predict My Insurance Charges"):
    if not validate_inputs(name, phone, email):
        st.stop()

    input_data = {
        "age": age,
        "sex": sex,
        "weight": weight,
        "height": height,
        "children": children,
        "smoker": smoker == "Yes",
        "region": region
    }

    try:
        response = requests.post(f"{API_URL}/predict", json=input_data)
        if response.status_code == 200:
            result = response.json()
            charges = result['predicted_charges']

            # Display results
            st.success(f"💰 **Predicted Charges:** ${charges}")
            st.markdown(f"**BMI Category:** {result['bmi_category']}")
            st.markdown(f"**Lifestyle Risk:** {result['lifestyle_risk']}")
            st.markdown(f"**Age Group:** {result['age_group']}")

            # ---------------------------#
            # 📊 Horizontal Bar Chart
            categories = ['Your Charges ($)', 'Average Charges ($)']
            values = [charges, 13000 ]  # Example average values
            colors = ['#6c63ff', '#ff6c63']

            fig, ax = plt.subplots(figsize=(8,4))
            ax.barh(categories, values, color=colors)
            ax.set_xlabel("Value")
            ax.set_title("Comparison of Charges")
            ax.grid(axis='x', linestyle='--', alpha=0.7)
            st.pyplot(fig)

            # ---------------------------#
            # 📝 Suggestions based on BMI & lifestyle
            suggestions = []
            if bmi < 18.5:
                suggestions.append("Increase calorie intake, focus on balanced diet.")
            elif 18.5 <= bmi < 25:
                suggestions.append("Maintain your current healthy lifestyle.")
            elif 25 <= bmi < 30:
                suggestions.append("Include regular exercise and monitor diet.")
            else:
                suggestions.append("Consult a nutritionist and consider lifestyle changes.")
            if smoker == "Yes":
                suggestions.append("Consider quitting smoking to reduce health risks.")

            st.subheader("💡 Health Suggestions")
            for s in suggestions:
                st.markdown(f"- {s}")

        else:
            st.error("❌ Error fetching prediction from API.")
    except Exception as e:
        st.error(f"⚠️ Could not connect to backend: {e}")

st.markdown("---")
st.caption("Built with ❤️ by **Sadiya Sajid**")
