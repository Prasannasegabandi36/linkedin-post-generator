import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_groq_api_key():
    """
    First checks Streamlit secrets, then checks local .env file.
    For Streamlit Cloud, add GROQ_API_KEY in app secrets.
    For local, add GROQ_API_KEY in .env file.
    """
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


def get_llm():
    api_key = get_groq_api_key()

    if not api_key:
        st.error("GROQ_API_KEY is missing. Add it in Streamlit Secrets or .env file.")
        st.stop()

    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.7
    )


llm = get_llm()
