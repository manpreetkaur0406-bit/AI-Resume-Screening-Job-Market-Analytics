import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib

resume_df = pd.read_csv("resume_data.csv")
salary_df = pd.read_csv("ds_salaries.csv")
jobs_df = pd.read_csv("/content/DataAnalyst.csv.zip", compression="zip")
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
    ...

elif menu == "📊 EDA":
elif menu == "📄 ATS Score":
