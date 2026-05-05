import os   # to access environment variables. 
import requests # to make HTTP requests to the Groq APIs.
import streamlit as st  # create web interface for UI.
from groq import Groq # to interact with Groq APIs.
from dotenv import load_dotenv  # to load environments.

# Step 2: Load environment variables.
load_dotenv()   # This will load the environment variable from the .env file
api_key = os.environ.get("GROQ_API_KEY")

# Step 3: Fetch the Available model from Groq API.

def fetch_models(api_key):
    url = "https://api.groq.com/openai/v1/models"

    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"

    }
    response = requests.get(url, headers=headers)
    available_models = []

    for i in response.json().get("data", []):        
        available_models.append(i['id'])
    return available_models

# print("Fetching available models from Groq API...")
# print(fetch_models(api_key))

# Step 4: Page Configuration
st.set_page_config(page_title=" AI chatbot using Streamlit and groq")    # to pass the page title.

# Step 5: App title in the description.
st.title("🔥 AI Chatbot using Streamlit and Groq")

# For caption 
#  For adding the icon -> copy the icon from google and paste it.
st.caption("This is the sample application.")

#  Step 6: Session state - Conversational AI Bot

if "message" not in st.session_state:
    st.session_state.message = []
    
#  Step 7: Rendering Existing Conversation.

for msg in st.session_state.message:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# Step 6: Sidebar - Configuration.

with st.sidebar:
    st.header("Confuguration ⚙️")
    api_key_default = os.getenv("GROQ_API_KEY", "") # if user is not passing the key, then by default put own API key.
    api_key = st.text_input("GROQ API KEY", 
                            value = api_key_default, 
                            type="password", 
                            help= "Enter Your GROQ API Key.")   # to get the API_KEY from the end user.
    
    # model selection from the GROQ model. (end model)
    available_models = fetch_models(api_key)
    model = st.selectbox("Select a Model", 
                         options = available_models, 
                         help = "Available Models in GROQ")  # parameters (labels,options)
    
    system_prompt = st.text_area("System Prompt",
                                 height = 100,
                                 placeholder = "You are a helpful and friendly AI system.", # to make the text in the text area semi transparent.
                                 help="sets the behaviour of the chatbot.")
    
    temperature = st.slider("Temperature",
                            min_value = 0.0,
                            max_value = 1.0,
                            value = 0.5, 
                            step = 0.05)
    
# Stap 7: User Input

# user_input = st.text_input("Ask me Anything...") # by default shows at the top of the box.
user_input = st.chat_input("Ask me Anything...") 
if user_input:
    st.session_state.message.append({"role":"user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    client = Groq(
        api_key = api_key,
    )
    message_payload =[{"role": "system", "content": system_prompt}]
    chat_completion = client.chat.completions.create(
        messages =  message_payload + st.session_state.message,
        model=model,
        temperature= temperature
    )
    
    response = chat_completion.choices[0].message.content
    st.markdown(f"**Chatbot:** {response}")
    
    st.session_state.message.append({"role": "assistant", "content": response})
    



