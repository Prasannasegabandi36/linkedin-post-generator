from langchain_groq import ChatGroq
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Add it in Streamlit Secrets.")
    st.stop()

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)
