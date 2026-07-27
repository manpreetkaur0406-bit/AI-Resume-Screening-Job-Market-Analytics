import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib
import pdfplumber

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
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )

    # No resume uploaded
    if uploaded_file is None:

        st.info("📂 Please upload your resume in PDF or DOCX format.")

        st.stop()

    # Invalid file
    if uploaded_file.type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:

        st.error("❌ Only PDF and DOCX files are supported.")

        st.stop()

    st.success("✅ Resume uploaded successfully!")

    # ==========================
    # Extract Resume Text
    # ==========================

    resume_text = ""

    if uploaded_file.type == "application/pdf":

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    resume_text += text.lower() + " "

    else:

        doc = Document(uploaded_file)

        for para in doc.paragraphs:

            resume_text += para.text.lower() + " "

    # ==========================
    # Skill Database
    # ==========================

    skill_database = [

        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "machine learning",
        "deep learning",
        "statistics",
        "data science",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "keras",
        "aws",
        "azure",
        "git",
        "github",
        "docker",
        "linux",
        "mysql",
        "postgresql",
        "mongodb",
        "communication",
        "problem solving",
        "critical thinking",
        "teamwork"

    ]

    # ==========================
    # Extract Skills
    # ==========================

    resume_skills = []

    for skill in skill_database:

        if skill in resume_text:

            resume_skills.append(skill)

    resume_skills = sorted(list(set(resume_skills)))

    st.session_state["resume_skills"] = resume_skills

    # ==========================
    # Required Skills
    # ==========================

    required_skills = [

        "python",
        "sql",
        "excel",
        "power bi",
        "machine learning",
        "statistics",
        "git",
        "communication"

    ]

    matched_skills = list(
        set(resume_skills) &
        set(required_skills)
    )

    missing_skills = list(
        set(required_skills) -
        set(resume_skills)
    )

    ats_score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    # ==========================
    # ATS Score
    # ==========================

    st.subheader("📊 ATS Score")

    st.metric(
        "Score",
        f"{ats_score:.0f}%"
    )

    st.progress(int(ats_score))

    # ==========================
    # Skills Found
    # ==========================

    st.subheader("✅ Skills Found")

    if resume_skills:

        st.write(", ".join(resume_skills))

    else:

        st.warning("No skills detected in the uploaded resume.")

    # ==========================
    # Matched Skills
    # ==========================

    st.subheader("🎯 Matched Skills")

    if matched_skills:

        for skill in matched_skills:

            st.success(skill.title())

    else:

        st.warning("No matching skills found.")

    # ==========================
    # Missing Skills
    # ==========================

    st.subheader("❌ Missing Skills")

    if missing_skills:

        for skill in missing_skills:

            st.error(skill.title())

    else:

        st.success("Excellent! Your resume contains all required skills.")

    # ==========================
    # ATS Feedback
    # ==========================

    st.subheader("💡 ATS Feedback")

    if ats_score >= 80:

        st.success("Excellent resume! Your profile matches most of the required skills.")

    elif ats_score >= 60:

        st.info("Good resume. Adding the missing skills can improve your ATS score.")

    elif ats_score >= 40:

        st.warning("Average ATS score. Consider improving your technical skills and resume.")

    else:

        st.error("Low ATS score. Add more relevant technical skills to improve your chances.")

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

elif menu == "💼 Job Recommendation":

    st.title("💼 AI Job Recommendation")

    # Check if resume has been analyzed
    if "resume_skills" not in st.session_state:

        st.warning("📄 Please upload your resume first from the ATS Score page.")

    else:

        candidate_skills = st.session_state["resume_skills"]

        # No skills found in resume
        if len(candidate_skills) == 0:

            st.error("❌ No skills were found in your resume.")
            st.stop()

        st.subheader("✅ Skills Found in Resume")
        st.write(", ".join(candidate_skills))

        recommendations = []

        # Calculate Match Score
        for _, row in jobs_df.iterrows():

            description = str(row["Job Description"]).lower()

            score = 0

            for skill in candidate_skills:

                if skill.lower() in description:
                    score += 1

            recommendations.append(score)

        jobs_df["Match Score"] = recommendations

        # Keep only jobs with at least one matching skill
        matched_jobs = jobs_df[jobs_df["Match Score"] > 0]

        # No matching jobs
        if matched_jobs.empty:

            st.error("❌ No jobs recommended for your resume.")
            st.info("Please improve your resume by adding relevant technical skills, projects, certifications, or experience.")

        else:

            top_jobs = matched_jobs.sort_values(
                by="Match Score",
                ascending=False
            ).head(5)

            st.subheader("🏆 Recommended Jobs")

            for _, row in top_jobs.iterrows():

                match_percentage = (
                    row["Match Score"] /
                    len(candidate_skills)
                ) * 100

                if match_percentage > 100:
                    match_percentage = 100

                st.markdown("---")

                st.markdown(f"### 💼 {row['Job Title']}")

                st.write(f"🏢 **Company:** {row['Company Name']}")
                st.write(f"📍 **Location:** {row['Location']}")
                st.write(f"🎯 **Match:** {match_percentage:.0f}%")

                st.progress(int(match_percentage))

                with st.expander("View Job Description"):
                    st.write(row["Job Description"])

elif menu == "📈 Salary Analytics":

    st.title("📈 Salary Analytics Dashboard")

    st.markdown("Explore salary trends in the Data Science job market.")

    # ===========================
    # Remove unwanted column
    # ===========================

    salary_df = salary_df.drop(columns=["Unnamed: 0"], errors="ignore")

    # ===========================
    # KPI Cards
    # ===========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Average Salary",
            f"${salary_df['salary_in_usd'].mean():,.0f}"
        )

    with col2:
        st.metric(
            "📈 Highest Salary",
            f"${salary_df['salary_in_usd'].max():,.0f}"
        )

    with col3:
        st.metric(
            "📉 Lowest Salary",
            f"${salary_df['salary_in_usd'].min():,.0f}"
        )

    with col4:
        st.metric(
            "🌍 Countries",
            salary_df["company_location"].nunique()
        )

    st.markdown("---")

    # ===========================
    # Dataset Preview
    # ===========================

    st.subheader("📄 Salary Dataset Preview")

    st.dataframe(salary_df.head())

    # ===========================
    # Average Salary by Experience
    # ===========================

    st.subheader("💼 Average Salary by Experience Level")

    avg_salary = salary_df.groupby(
        "experience_level"
    )["salary_in_usd"].mean().sort_values()

    fig = px.bar(
        avg_salary,
        x=avg_salary.index,
        y=avg_salary.values,
        labels={
            "x": "Experience Level",
            "y": "Average Salary (USD)"
        },
        color=avg_salary.values,
        title="Average Salary by Experience Level"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Salary Distribution
    # ===========================

    st.subheader("📊 Salary Distribution")

    fig = px.histogram(
        salary_df,
        x="salary_in_usd",
        nbins=30,
        title="Salary Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Top 10 Highest Paying Jobs
    # ===========================

    st.subheader("🏆 Top 10 Highest Paying Job Titles")

    top_jobs = salary_df.groupby(
        "job_title"
    )["salary_in_usd"].mean().sort_values(
        ascending=False
    ).head(10)

    fig = px.bar(
        top_jobs,
        x=top_jobs.values,
        y=top_jobs.index,
        orientation="h",
        labels={
            "x": "Average Salary (USD)",
            "y": "Job Title"
        },
        color=top_jobs.values
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Remote Work Distribution
    # ===========================

    st.subheader("🏠 Remote Work Distribution")

    remote = salary_df["remote_ratio"].value_counts()

    fig = px.pie(
        values=remote.values,
        names=remote.index,
        title="Remote Work Ratio"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Company Size Distribution
    # ===========================

    st.subheader("🏢 Company Size Distribution")

    company = salary_df["company_size"].value_counts()

    fig = px.pie(
        values=company.values,
        names=company.index,
        title="Company Size"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Top Hiring Countries
    # ===========================

    st.subheader("🌍 Top Hiring Countries")

    countries = salary_df["company_location"].value_counts().head(10)

    fig = px.bar(
        countries,
        x=countries.index,
        y=countries.values,
        labels={
            "x": "Country",
            "y": "Jobs"
        },
        color=countries.values
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Employment Type
    # ===========================

    st.subheader("📋 Employment Type")

    employment = salary_df["employment_type"].value_counts()

    fig = px.bar(
        employment,
        x=employment.index,
        y=employment.values,
        color=employment.values
    )

    st.plotly_chart(fig, use_container_width=True)

    # ===========================
    # Salary by Company Size
    # ===========================

    st.subheader("💵 Salary by Company Size")

    salary_company = salary_df.groupby(
        "company_size"
    )["salary_in_usd"].mean()

    fig = px.bar(
        salary_company,
        x=salary_company.index,
        y=salary_company.values,
        labels={
            "x": "Company Size",
            "y": "Average Salary (USD)"
        },
        color=salary_company.values
    )

    st.plotly_chart(fig, use_container_width=True)


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
