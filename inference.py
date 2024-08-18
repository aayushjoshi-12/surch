from bs4 import BeautifulSoup
import requests
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
import streamlit as st

api_key = st.secrets["API_KEY"]
cse_id = st.secrets["CSE_ID"]
access_token = st.secrets["ACCESS_TOKEN"]

template = """
system: you are a summarizer that finds the answer the user is looking for in the context provided by the google search results top links.
keep your answers factual and only generate one response.
give the answer in markdown format.
context: {context}
user: {prompt}
"""

prompt = PromptTemplate.from_template(template)

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.5,
    huggingfacehub_api_token=access_token,
)

llm_chain = prompt | llm


def google_search(query, api_key, cse_id, num_results=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": api_key, "cx": cse_id, "num": num_results}
    response = requests.get(url, params=params)
    results = response.json().get("items", [])
    return results


def get_context(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = ""
    paragraphs = "".join([p.get_text() for p in soup.find_all("p")[:10]])
    return paragraphs


def get_answer(prompt):
    top_url = [
        result["link"]
        for result in google_search(prompt, api_key, cse_id, num_results=3)
    ]
    context = r"".join([get_context(url) for url in top_url])
    answer = llm_chain.invoke({"context": context, "prompt": prompt})
    return answer