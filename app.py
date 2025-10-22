import streamlit as st
import os
from modules.pdf_utils import extract_text_from_pdf, create_pdf_from_pages
from modules.grammar_corrector import correct_grammar

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="PDF Grammar Corrector", layout="centered")
st.title("📝 PDF Grammar & Spell Checker")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    st.info("Extracting text from PDF...")
    page_texts = extract_text_from_pdf(uploaded_file)

    if st.button("Correct Grammar & Spelling"):
        corrected_pages = []
        with st.spinner("Correcting... Please wait..."):
            for i, text in enumerate(page_texts, start=1):
                st.write(f"Processing page {i}...")
                corrected_text = correct_grammar(text)
                corrected_pages.append(corrected_text)

        output_path = os.path.join(OUTPUT_DIR, "corrected_output.pdf")
        create_pdf_from_pages(corrected_pages, output_path)

        with open(output_path, "rb") as f:
            st.success("✅ Correction complete!")
            st.download_button(
                label="📥 Download Corrected PDF",
                data=f,
                file_name="corrected_output.pdf",
                mime="application/pdf"
            )
