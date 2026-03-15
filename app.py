import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("MBBS PG Entrance Practice Bot")

if st.button("Generate Question"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a tutor helping an MBBS student prepare for NEET-PG."},
            {"role": "user", "content": "Generate one NEET-PG level MCQ with four options."}
        ]
    )

    st.write(response.choices[0].message.content)
