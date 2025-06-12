import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

## Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "O&A Chatbot"

## Prompt Template

prompt = ChatPromptTemplate(
    [
        ('system',"You are a trained psychologist with expertise in cases where people have lost someone very close to them and are grieving. \
         You must act empathetically, encourage the user to open up, and provide comfort to them."),
        ('user', "Question: {question}")

    ]


)

## Response generation

def generate_respone(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    model = ChatOpenAI(model=llm, api_key=api_key)
    parser = StrOutputParser()
    chain = prompt|model|parser
    answer = chain.invoke({'question': question})
    return answer


## APP

## Title
st.title("Q and A Chatbot with OpenAI")

## Sidebar settings
st.sidebar.title('settings')
apikey = st.sidebar.text_input("Enter your API key", type = 'password')

## Dropdown for llm select

llm = st.sidebar.selectbox('Select model', ['gpt-4.1-2025-04-14','o4-mini-2025-04-16'])

## Sliders for temeprature and max_tokens

temperature = st.sidebar.slider('Temperature', min_value = 0.0, max_value = 1.0, value= 0.5)
max_tokens = st.sidebar.slider('maxtokens', min_value = 100, max_value = 300, value= 200)


## User input interface

st.write("Please feel free to explain any issue you are facing")
user_input = st.text_input("You: ")

if user_input:
    response = generate_respone(user_input,apikey, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the issue.")