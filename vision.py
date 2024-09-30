import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import random
import io

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

genai.configure(api_key=api_key)

# Set page config
st.set_page_config(page_title="SIGMA Pro: AI Q&A Assistant", page_icon="https://i.postimg.cc/FsvsmXbC/pixelcut-export.png", layout="wide")
st.logo("https://i.postimg.cc/FsvsmXbC/pixelcut-export.png")
st.sidebar.markdown("SIGMA Pro")

# Custom CSS for improved theming (unchanged)
st.markdown("""
<style>
    /* ... (CSS remains unchanged) ... */
</style>
""", unsafe_allow_html=True)

@st.cache_data
def add_friendly_touch(response):
    friendly_intros = [
        "Hello! ",
        "Great question! ",
        "Interesting query! ",
        "I'm happy to help with this! ",
        "Let's explore this topic! ",
    ]
    friendly_outros = [
        " I hope this information is helpful!",
        " Please let me know if you need any clarification.",
        " Feel free to ask for more details if needed.",
        " I hope this answers your question.",
        " Don't hesitate to ask if you have any follow-up questions.",
    ]

    response = random.choice(friendly_intros) + response.strip()
    response += random.choice(friendly_outros)
    
    return response

def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        if input_text and image:
            response = model.generate_content([input_text, image])
        elif image:
            response = model.generate_content(image)
        elif input_text:
            response = model.generate_content(input_text)
        else:
            return "Please provide a question or an image."
        
        friendly_response = add_friendly_touch(response.text)
        return friendly_response
    except Exception as e:
        return f"An error occurred: {str(e)}. Please try again."

def main():
    st.markdown("<h1 class='big-font'>Welcome to SIGMA Pro</h1>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("About SIGMA Pro")
        st.markdown("""
        SIGMA Pro is an advanced AI Q&A Assistant powered by Google's Gemini AI. 
        It offers intelligent responses to your questions and can analyze images.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Main content
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Ask your question")
        input_text = st.text_area("Enter your question here:", key="input", height=100)
        
        uploaded_file = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])
        image = None
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Get Answer"):
            if not input_text and not uploaded_file:
                st.warning("Please enter a question or upload an image.")
            else:
                with st.spinner("Generating response..."):
                    response = get_gemini_response(input_text, image)
                st.subheader("SIGMA Pro's Response:")
                st.write(response)

    with col2:
        st.subheader("Quick Tips")
        st.markdown("""
        - Be specific in your questions
        - For image analysis, ensure the image is clear
        - You can ask follow-up questions
        - Enjoy faster response times
        """)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
