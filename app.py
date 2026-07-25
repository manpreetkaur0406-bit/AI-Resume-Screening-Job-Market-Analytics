import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib

resume_df = pd.read_csv("resume_data.csv")
salary_df = pd.read_csv("ds_salaries.csv")
jobs_df = pd.read_csv("DataAnalyst.csv.zip", compression="zip")
people_df = pd.read_csv("01_people.csv")


st.set_page_config(
    page_title="AI Resume Screening & Job Market Analytics",
    page_icon="🤖",
    layout="wide"
)


menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "🏠 Home",
        "📊 EDA",
        "📄 ATS Score",
        "💼 Job Recommendation",
        "📈 Salary Analytics",
        "💰 Salary Prediction",
        "ℹ️ About"
    ]
)


if menu == "🏠 Home":
    st.title("🤖 AI Resume Screening & Job Market Analytics")

    st.write("Welcome to my Final Year Data Analytics Project!")

    st.markdown("""
    ### 🚀 Features

    - 📊 EDA
    - 📄 ATS Score
    - 🧠 Skill Gap Analysis
    - 💼 Job Recommendation
    - 💰 Salary Prediction
    - 📈 Salary Analytics

    👈 Choose a page from the sidebar.
    """)

elif menu == "📊 EDA":

    st.title("📊 Exploratory Data Analysis")

    st.dataframe(resume_df.head())
    st.dataframe(salary_df.head())
    st.dataframe(jobs_df.head())

elif menu == "📄 ATS Score":

    ats_score = 40

    st.metric("ATS Score", f"{ats_score}%")

elif menu == "💼 Job Recommendation":
    st.title("💼 AI Job Recommendation")
    st.write("Job Recommendation page is under development.")

elif menu == "📈 Salary Analytics":
    st.title("📈 Salary Analytics")
    st.write("Salary Analytics page is under development.")

elif menu == "💰 Salary Prediction":
    st.title("💰 Salary Prediction")
    st.write("Salary Prediction page is under development.")

elif menu == "ℹ️ About":
    st.title("ℹ️ About")
    st.write("AI Resume Screening & Job Market Analytics")
