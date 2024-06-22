from transformers import pipeline
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
import requests
import os

load_dotenv()

api_key = os.environ.get('API_KEY')
cse_id = os.environ.get('CSE_ID')
access_token = os.environ.get('ACCESS_TOKEN')

def google_search(query, api_key, cse_id, num_results=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results
    }
    response = requests.get(url, params=params)
    results = response.json().get('items', [])
    return results

def get_context(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = ""
    paragraphs = "".join([p.get_text(seperator='\n') for p in soup.find_all('p')[:3]])
    return paragraphs

def get_answer(prompt):
    top_url = [result['link'] for result in google_search(prompt, api_key, cse_id, num_results=3)]
    context = r"".join([get_context(url) for url in top_url])
    print(context, "\n")
    que = question.format(prompt=prompt)
    print(que, "\n\n")
    answer = qa_pipeline(question=que, context=context)
    return answer

qa_pipeline = pipeline('question-answering', model='deepset/roberta-base-squad', token=access_token) 

question = """
system: you are a summarizer that finds the answer the user is looking for in the context provided by the google search results top links and your previous conversation with the user. answer in atleast 100 words.
user: {prompt}
"""

answer = get_answer("how to use torch.view() in pytorch")
print(answer['answer'])


#######                         UI                      ########
########-----------------------------------------------#########

# st.title("Surch")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         # response = st.write(prompt)
#         response = st.write_stream(get_answer(prompt))
#     st.session_state.messages.append({"role": "assistant", "content": response})