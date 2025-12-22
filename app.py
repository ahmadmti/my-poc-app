import streamlit as st
import pandas as pd
import os

# 1. Setup Page Config
st.set_page_config(page_title="Lead Capture POC", layout="centered")

# 2. Simple CSS styling (Since you know CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Gym Member Interest Form")
st.write("Fill in the details below to join the waitlist.")

# 3. Data Storage Logic (Simple CSV 'Database')
DB_FILE = "leads.csv"

def save_data(name, email, goal):
    new_data = pd.DataFrame([[name, email, goal]], columns=["Name", "Email", "Goal"])
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(DB_FILE, index=False)

# 4. The User Interface (The "Form")
with st.form("interest_form", clear_on_submit=True):
    name = st.text_input("Full Name of the memeber")
    email = st.text_input("Email Address")
    goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "General Health"])
    submit = st.form_submit_button("Submit Details")

    if submit:
        if name and email:
            save_data(name, email, goal)
            st.success(f"Done! {name} has been added to the database.")
        else:
            st.error("Please fill in all fields.")

# 5. The "Admin View" (The Data Table)
st.divider()
st.subheader("📊 Collected Leads (Admin View)")
if os.path.exists(DB_FILE):
    current_leads = pd.read_csv(DB_FILE)
    st.dataframe(current_leads, use_container_width=True)
else:
    st.info("No leads collected yet.")