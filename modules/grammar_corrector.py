import language_tool_python
import streamlit as st

from openai import OpenAI
import os
from dotenv import load_dotenv

@st.cache_resource
def get_tool():
    """Initialize LanguageTool only once and cache it."""
    return language_tool_python.LanguageTool('en-US')

def correct_grammar_tool(text):
    """Correct grammar and spelling mistakes using cached LanguageTool."""
    tool = get_tool()
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text


# Load environment variables from .env file
load_dotenv()

# Load API key securely (assuming set as environment variable)
# Example in terminal or .env: export OPENAI_API_KEY="sk-..."
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_grammar(text):
    """Use GPT model for grammar and spelling correction."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a grammar correction assistant. Fix all grammar and spelling mistakes while keeping the original meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()
