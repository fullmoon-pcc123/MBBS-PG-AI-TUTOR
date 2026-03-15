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

user_question = st.text_input("Type your medical question")

if st.button("Ask AI Tutor"):

    # Step 1 — Classify if question is medical
    classification = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Answer YES if the question is related to medicine, MBBS subjects, diseases, drugs, anatomy, physiology, pathology, surgery, or clinical topics. Otherwise answer NO."
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    decision = classification.choices[0].message.content.strip().upper()

    # Step 2 — Block unrelated questions
    if decision != "YES":
        st.warning("I am designed only for MBBS and medical entrance preparation. Please ask a medical question.")

    else:

        # Step 3 — Generate tutor answer
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI tutor helping MBBS students prepare for PG entrance exams.

Explain clearly and concisely.
Focus on exam-relevant concepts.
Include a short memory tip if possible.
"""
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ]
        )

        answer = response.choices[0].message.content

        st.session_state.answer = answer
        st.session_state.question = user_question


# Step 4 — Display answer
if "answer" in st.session_state:
    st.write(st.session_state.answer)


# Step 5 — Visual Representation button
if "answer" in st.session_state:
    if st.button("🔬 View Visual Representation"):

        search_query =  st.session_state.question 

        search_url = f"https://teachmeanatomy.info/?s={search_query}"

        st.markdown(f'<a href="{search_url}" target="_blank">Open Diagram</a>', unsafe_allow_html=True)

    with col2:
        if st.button("🎥 Watch Video"):
            video_query = st.session_state.question + " osmosis medical animation"
            video_url = f"https://www.youtube.com/results?search_query={video_query}"

            st.markdown(
                f'<a href="{video_url}" target="_blank">Watch Explanation Video</a>',
                unsafe_allow_html=True
            )


st.markdown("Powered by AnecdoteBox.com — Stories to make your Day!")
