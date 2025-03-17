import streamlit as st
import google.generativeai as genai
import os

# Load API key
API_KEY = ("AIzaSyAkDOdMVFlj6v45uIc03_LTfMLq_83KMdY")

if not API_KEY:
    st.error("⚠️ API Key is missing! Set your Google Gemini API Key as an environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

# Adjust safety settings (Set all categories to 'BLOCK_NONE' to disable filtering)
safety_settings = [
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

# Function to generate content (poem or story)
def generate_content(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt, safety_settings=safety_settings)
        return response.text if response.text else "⚠️ The AI refused to generate a response."
    except Exception as e:
        return f"❌ Error: {e}"

# Streamlit UI
st.title("📜 AI-Powered Generator")
st.write("✨ Generate beautiful poems or cute short stories using AI! ✨")

# Session State to track page (poem or story)
if "page" not in st.session_state:
    st.session_state.page = "poem"

# Navigation buttons
col1, col2 = st.columns([1, 1])
if st.session_state.page == "story":
    if col1.button("⬅ Previous"):
        st.session_state.page = "poem"
        st.rerun()
elif st.session_state.page == "poem":
    if col2.button("Next ➡"):
        st.session_state.page = "story"
        st.rerun()

# Poem Generator Page
if st.session_state.page == "poem":
    st.subheader("📖 Generate a Poem")
    theme = st.text_input("🔹 Enter a theme (e.g., love, nature, adventure):")
    mood = st.selectbox("🔹 Select the mood:", ["Happy", "Sad", "Romantic", "Inspirational", "Mysterious", "Dark"])
    style = st.selectbox("🔹 Select the style:", ["Haiku", "Sonnet", "Free Verse", "Rhyming Couplets", "Limerick"])
    if st.button("🎤 Generate Poem"):
        if theme.strip():
            poem_prompt = f"Create a {style.lower()} poem about {theme.strip()} in a {mood.lower()} tone."
            with st.spinner("✨ Creating your poem..."):
                poem = generate_content(poem_prompt)
            st.subheader("🎶 Your AI-Generated Poem:")
            st.write(poem)
        else:
            st.warning("⚠️ Please enter a theme for the poem.")

# Short Story Generator Page
elif st.session_state.page == "story":
    st.subheader("📖 Generate a Cute Short Story")
    story_theme = st.text_input("🔹 Enter a theme (e.g., animals, friendship, magic):")
    story_length = st.selectbox("🔹 Select the story length:", ["Very Short", "Short", "Medium", "Long"])
    if st.button("📖 Generate Story"):
        if story_theme.strip():
            story_prompt = f"Write a {story_length.lower()} cute short story about {story_theme.strip()}."
            with st.spinner("✨ Creating your story..."):
                story = generate_content(story_prompt)
            st.subheader("📚 Your AI-Generated Story:")
            st.write(story)
        else:
            st.warning("⚠️ Please enter a theme for the story.")

st.markdown("---")
st.write("💡 Made with ❤️")
