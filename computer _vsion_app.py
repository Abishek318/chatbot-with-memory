import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from groq import Groq
import base64

load_dotenv()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to encode the image for groq
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# Function to generate response
def generate_response(prompt, images, model):
    if model == "Google Gemini":
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt] + images)
        return response.text
    elif model == "Groq":

        content= [  {"type": "text", "text": prompt}, ]
        if  images:
            base64_image = encode_image(images)
            content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        })
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content":content
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )
        return chat_completion.choices[0].message.content

st.title("Chatbot Image Prompt App")

# Model selection
model = st.radio("Select Model:", ["Google Gemini", "Groq"])

# Check API keys based on selected model
if model == "Google Gemini" :
    if 'GOOGLE_API_KEY' not in os.environ:
        google_api_key = st.text_input('Enter your Google API Key:', type='password')
        if google_api_key:
            os.environ['GOOGLE_API_KEY'] = google_api_key
            genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        else:
            st.error('Please enter your Google API Key to proceed with Google Gemini model.')
            st.stop()
    else:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

if model == "Groq" :
    if 'GROQ_API_KEY' not in os.environ:
        groq_api_key = st.text_input('Enter your Groq API Key:', type='password')
        if groq_api_key:
            os.environ['GROQ_API_KEY'] = groq_api_key
            groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])
        else:
            st.error('Please enter your Groq API Key to proceed with Groq model.')
            st.stop()
    else:
        groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])

# Image upload
if model == "Google Gemini":
    uploaded_files = st.file_uploader("Upload up to 10 images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        st.image(uploaded_files, width=100)
else:
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, width=100)

# Sample prompts
sample_prompts = [
    "Describe the contents of this image in detail.",
    "What emotions or mood does this image convey?",
    "From the image, extract the question and its number if available. Provide the answer with options or create options from A to Z, followed by an explanation."
]

# User input area with sample prompts
prompt_option = st.selectbox(
    "Choose a sample prompt or type your own:",
    ["Custom prompt"] + sample_prompts
)

if prompt_option == "Custom prompt":
    user_prompt = st.text_area("Type your custom message here:", placeholder="Enter your prompt or message...")
else:
    user_prompt = st.text_area("Edit the selected prompt or type your message here:", value=prompt_option)

# Submit button
if st.button("Send"):
    if not user_prompt:
        st.error("Please enter a prompt.")
    elif model == "Google Gemini" and len(uploaded_files) > 10:
        st.error("Please upload no more than 10 images for Google Gemini model.")
    else:
        with st.spinner("Generating response..."):
            if model == "Google Gemini":
                images = [Image.open(file) for file in uploaded_files] if uploaded_files else []
            else:
                images = uploaded_file
            
            response = generate_response(user_prompt, images, model)
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear and Download buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.messages:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

with col2:
    if st.session_state.messages:
        response_text = "\n".join([m["content"] for m in st.session_state.messages if m["role"] == "assistant"])
        st.download_button("Download Response", response_text, "response.txt")