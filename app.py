import streamlit as st
import google.generativeai as genai
import os

# Set your API key from Streamlit's secrets management
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def generate_meeting_notes(transcript):
    """
    Generates a meeting summary and action items from a transcript using the Gemini model.
    """
    prompt = f"""
    Given the following meeting transcript, perform two tasks:
    1. Summarize the main discussion points.
    2. Extract all action items, including the person responsible and the deadline (if mentioned).

    Format your response using Markdown, with clear headings for each section.

    Transcript:
    {transcript}
    """
    
    # Configure the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# --- Streamlit UI ---

st.title("AI Meeting Assistant 🤖")
st.write("Automatically summarize meeting transcripts and extract action items.")

# Text area for user to input the transcript
user_transcript = st.text_area(
    "Paste your meeting transcript here:",
    height=300,
    placeholder="e.g., [00:01] John: We need to finalize the budget...",
)

# Button to trigger the analysis
if st.button("Generate Summary & Action Items"):
    if user_transcript:
        # Show a spinner while the model is processing
        with st.spinner("Analyzing transcript..."):
            summary_and_actions = generate_meeting_notes(user_transcript)
        
        # Display the result
        st.subheader("Results")
        st.markdown(summary_and_actions)
    else:
        st.warning("Please paste a transcript to begin.")