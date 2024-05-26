import replicate
import streamlit as st
import os
from dotenv import load_dotenv
import webbrowser

# Load environment variables from .env file
load_dotenv()

# REPLICATE_API_URL = "https://replicate.com/account/api-tokens"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Add more relevant medical terminologies
relevant_terminologies = [
    "Antibiotics", "Antibodies", "Antigen", "Vaccination", "Immunization", 
    "Pathogen", "Microorganism", "Immune System", "Hormones", "Infection", 
    "Diagnosis", "Treatment", "Therapy", "Medication", "Dosage", "Side Effects", 
    "Symptoms", "Prevention", "Prognosis", "Recovery", "Surgery", "Anesthesia", 
    "Pharmaceuticals", "Biotechnology", "Genetics", "Gene Therapy", "Radiation", 
    "Chemotherapy", "Physiotherapy", "Psychotherapy", "Dietary Supplements", 
    "Holistic Medicine", "Alternative Medicine", "Complementary Medicine", 
    "Naturopathy", "Homeopathy", "Acupuncture", "Chiropractic", "Ayurveda", 
    "Massage Therapy", "Hygiene", "Nutrition", "Exercise", "Physical Therapy",
    "Medical Imaging", "X-ray", "MRI", "CT Scan", "Ultrasound", "EKG", 
    "Electrocardiogram", "Blood Pressure", "Pulse Rate", "Respiration Rate", 
    "Medical Records", "Health Insurance", "Telemedicine", "Medical Ethics", 
    "Patient Confidentiality", "Medical Research", "Clinical Trials", 
    "Healthcare Policies", "Medical Education", "Medical Training", 
    "Medical Specializations", "Anatomy", "Physiology", "Pathology", 
    "Pharmacology", "Epidemiology", "Public Health", "Healthcare Administration"
]

with st.sidebar:
    st.title("MediBot💉")
    st.write("Welcome to MediBot💉! I'm here to assist you with any medical queries you may have. Let's talk health!💊")
    headers = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json"
}

    st.subheader('Models and Parameters')
    selected_model = st.selectbox('Choose a Model', ['Model A', 'Model B'], key='selected_model')
    if selected_model == 'Model A':
            llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Model B':
            llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

    temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=32, max_value=128, value=120, step=8)
       
# First message to be initialized 
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to MediBot💉! I'm here to assist you with any medical queries you may have. Let's talk health!💊"}]

st.subheader("Chats")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
     st.session_state.messages = [{"role": "assistant", "content": "Welcome to MediBot💉! I'm here to assist you with any medical queries you may have. Let's talk health!💊"}]
st.sidebar.button("Delete Chats", on_click=clear_chat_history)

# Bot answer 
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.\n\n"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
    # Check if the user's input contains any medical terminologies
    for term in relevant_terminologies:
        if term.lower() in prompt_input.lower():
            return f"As a medical bot, I can provide some insights about {term}. Is there anything specific you would like to know?"

    output = replicate.run(
        llm,  
        input={"prompt": f"{string_dialogue} {prompt_input}\nAssistant: ", "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1.0}
    )
    return output

# Chat input and response generation
if prompt := st.chat_input(placeholder="Hello! Enter your prompt here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("User"):
        st.write(prompt)

    with st.chat_message("Assistant"):
        with st.spinner("Shhh...🤫Thinking in process"):
            response = generate_llama2_response(prompt)
            full_response = ''.join(response)
            st.write(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

with st.sidebar:
    def open_website(url):
        webbrowser.open(url, new=0, autoraise=True)

    website_url = "https://www.health.harvard.edu/blog"

    if st.button("Go to Website"):
        open_website(website_url)

    st.write("Stay updated with the latest medical news and insights!")
    website_url = "https://www.health.harvard.edu/blog"

    if st.button("Medical News"):
        open_website(website_url)

    # Add an Acknowledgment button to navigate back to the Blogging social app
    if st.button("About Us", key='ack_button'):
        st.markdown("Created by Starlets...")
