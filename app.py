import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib

try:
    resume_df = pd.read_csv("resume_data.csv")
    st.sidebar.success("✅ resume_data.csv loaded")
except Exception as e:
    st.sidebar.error(f"resume_data.csv: {e}")

try:
    salary_df = pd.read_csv("ds_salaries.csv")
    st.sidebar.success("✅ ds_salaries.csv loaded")
except Exception as e:
    st.sidebar.error(f"ds_salaries.csv: {e}")

try:
    jobs_df = pd.read_csv("DataAnalyst.csv.zip", compression="zip")
    st.sidebar.success("✅ DataAnalyst.csv.zip loaded")
except Exception as e:
    st.sidebar.error(f"DataAnalyst.csv.zip: {e}")

try:
    people_df = pd.read_csv("01_people.csv")
    st.sidebar.success("✅ 01_people.csv loaded")
except Exception as e:
    st.sidebar.error(f"01_people.csv: {e}")

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

    st.title("📄 ATS Resume Score")
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    if uploaded_file is not None:

    # Extract text
    # Extract skills
    # Calculate ATS
        st.success("Resume uploaded successfully!")
    

    # Resume skills
    resume_skills = [
        "python",
        "machine learning",
        "sql",
        "data science",
        "statistics"
    ]

    # Required job skills
    required_skills = [
        "python",
        "sql",
        "statistics",
        "aws",
        "git"
    ]

    # Find matched skills
    matched_skills = list(set(resume_skills) & set(required_skills))

    # Calculate ATS score
    ats_score = (len(matched_skills) / len(required_skills)) * 100

    st.metric("ATS Score", f"{ats_score:.0f}%")

    st.subheader("✅ Matched Skills")
    st.write(matched_skills)

    missing_skills = list(set(required_skills) - set(resume_skills))

    st.subheader("❌ Missing Skills")
    st.write(missing_skills)
    st.metric("ATS Score","85%")

elif menu == "🧠 Skill Gap":

    st.title("🧠 Skill Gap Analysis")
    
elif menu == "💼 Job Recommendation":

    st.title("💼 AI Job Recommendation")

    candidate_skills = [
        "python",
        "machine learning",
        "sql",
        "statistics",
        "data science"
    ]

    recommendations = []

    for _, row in jobs_df.iterrows():

        description = str(row["Job Description"]).lower()

        score = sum(skill in description for skill in candidate_skills)

        recommendations.append(score)

    jobs_df["Match Score"] = recommendations

    top_jobs = jobs_df.sort_values(
        "Match Score",
        ascending=False
    ).head(10)

    st.subheader("Top Recommended Jobs")

    st.dataframe(
        top_jobs[
            [
                "Job Title",
                "Company Name",
                "Location",
                "Match Score"
            ]
        ]
    )

elif menu == "📈 Salary Analytics":

    st.title("📈 Salary Analytics Dashboard")

    # Average Salary by Experience Level
    avg_salary = salary_df.groupby("experience_level")["salary_in_usd"].mean().reset_index()

    fig1 = px.bar(
        avg_salary,
        x="experience_level",
        y="salary_in_usd",
        title="Average Salary by Experience Level"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Company Size Distribution
    fig2 = px.pie(
        salary_df,
        names="company_size",
        title="Company Size Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Top Hiring Countries
    top_country = salary_df["company_location"].value_counts().head(10)

    fig3 = px.bar(
        x=top_country.index,
        y=top_country.values,
        labels={"x":"Country","y":"Jobs"},
        title="Top Hiring Countries"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Remote Work Distribution
    fig4 = px.histogram(
        salary_df,
        x="remote_ratio",
        title="Remote Work Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)

elif menu == "💰 Salary Prediction":

    st.title("💰 Salary Prediction")

    model = joblib.load("salary_prediction_model.pkl")

    experience = st.number_input("Experience Level", min_value=0, max_value=4, value=2)
    employment = st.number_input("Employment Type", min_value=0, max_value=3, value=0)
    job_title = st.number_input("Job Title", min_value=0, value=10)
    salary_currency = st.number_input("Salary Currency", min_value=0, value=0)
    residence = st.number_input("Employee Residence", min_value=0, value=20)
    remote = st.number_input("Remote Ratio", min_value=0, max_value=100, value=100)
    company_location = st.number_input("Company Location", min_value=0, value=20)
    company_size = st.number_input("Company Size", min_value=0, max_value=2, value=1)

    if st.button("Predict Salary"):

        sample = pd.DataFrame([[2023, experience, employment, job_title,
                                salary_currency, residence, remote,
                                company_location, company_size]],
                              columns=[
                                  "work_year",
                                  "experience_level",
                                  "employment_type",
                                  "job_title",
                                  "salary_currency",
                                  "employee_residence",
                                  "remote_ratio",
                                  "company_location",
                                  "company_size"
                              ])

        prediction = model.predict(sample)

        usd_to_inr = 87
        salary_inr = prediction[0] * usd_to_inr

        st.success(f"💰 Predicted Salary: ₹ {salary_inr:,.0f}")

elif menu == "ℹ️ About":

    st.title("ℹ️ About Project")

    st.write("""
    **AI Resume Screening & Job Market Analytics**

    This project uses Data Analytics and Machine Learning to:

    • Analyze resumes
    • Calculate ATS scores
    • Recommend jobs
    • Analyze salary trends
    • Predict salaries

    **Technologies Used**
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - Plotly
    
    """)
