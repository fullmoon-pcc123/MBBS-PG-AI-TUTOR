import streamlit as st
from openai import OpenAI
import datetime
import random

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="MBBS PG AI Tutor",
    page_icon="🩺",
    layout="centered"
)

# Banner image
st.image("banner.png", use_container_width=True)

st.subheader("AI Powered PG Medical Question Practice")
st.divider()

# Subjects list
subjects = [
    "Anatomy",
    "Physiology",
    "Biochemistry",
    "Pathology",
    "Pharmacology",
    "Microbiology",
    "Forensic Medicine",
    "Community Medicine",
    "ENT",
    "Ophthalmology",
    "Medicine",
    "Surgery",
    "OBG",
    "Pediatrics"
]

# Sidebar subject selector
st.sidebar.title("Select Subject")
selected_subject = st.sidebar.selectbox(
    "Choose a subject",
    subjects
)

# Question of the Day
st.subheader("📅 Question of the Day")

today = datetime.date.today()
random.seed(today.toordinal())

daily_subject = random.choice(subjects)

if "daily_question" not in st.session_state:

    prompt = f"""
Generate one NEET-PG style MCQ from {daily_subject}.

Format:

Question
A
B
C
D

Correct Answer

Explanation

Memory Tip
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.session_state.daily_question = response.choices[0].message.content

st.info(st.session_state.daily_question)

st.success("Come back tomorrow for a new Question of the Day!")

st.divider()

# Generate new question
st.subheader("🧠 Practice Question")

if st.button("Generate New Question"):

    prompt = f"""
Generate one NEET-PG level MCQ from {selected_subject}.

Include:

Question
A
B
C
D

Correct Answer

Explanation

Memory Tip
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.write(response.choices[0].message.content)

st.divider()

# Ask medical doubt
st.subheader("💬 Ask Your Medical Doubt")

user_question = st.text_input("Type your question")

if st.button("Ask AI Tutor"):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful medical tutor explaining concepts for MBBS PG entrance exams."
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    st.write(response.choices[0].message.content)

st.divider()

# Footer
st.markdown("**Powered by AnecdoteBox.com — Stories to make your Day!**")
