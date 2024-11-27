# app.py
import streamlit as st
import requests
import json

# Function to call the OpenAI API directly
def call_openai_api(api_key, prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",  # Specify the model
        "messages": [
            {"role": "system", "content": "You are an experienced educator, someone who specialises simplying complex technical or mathematical concepts into easy-to-understand elemenents. When explaining a concept or describing a process you break it down into small chunks, avoid using jargon (where needed) or if you do need to use more technical langage/concepts to summarise succintly and provide information as to where else to find further information. If you need to provide code (or similar) you always comment the code to help a non-expert understand what each element is doing. You do not rely too heavily on analogies or metaphores to explain conepts if they are highly unrelated to the specific example at hand."},  # Hardcoded pre-prompt
            {"role": "user", "content": prompt}  # User message
        ],
        "max_tokens": 1500,
        "temperature": 0.1
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
    return response.json()  # Return the JSON response

# Streamlit app layout
st.title("ExPlainly")
text_input = st.text_area("What are you trying to learn or trying to do?")
purpose_input = st.text_input("Who is the audience/what is the purpose for this?")

if st.button("Get Feedback"):
    if text_input and purpose_input:
        api_key = st.secrets["openai"]["api_key"]  # Get API key from Streamlit secrets
        prompt = f"Proofread the following text for the purpose of {purpose_input}: {text_input}"
        feedback_response = call_openai_api(api_key, prompt)
        
        # Extract the content from the response
        if 'choices' in feedback_response and len(feedback_response['choices']) > 0:
            feedback = feedback_response['choices'][0]['message']['content']
            st.subheader("Feedback:")
            st.write(feedback)
        else:
            st.error("Error in response from OpenAI API.")
    else:
        st.error("Please fill in all fields.")
