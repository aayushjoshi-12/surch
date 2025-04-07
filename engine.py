import requests
import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

ACCESS_TOKEN = st.secrets["ACCESS_TOKEN"]
API_KEY = st.secrets["API_KEY"]
CSE_ID = st.secrets["CSE_ID"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Give the answer in markdown format. "
    "\n\n"
    "{context}"
)

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


class SurchEngine:
    def __init__(self, user_id, conversation_id):
        self.session_id = f"{user_id}-{conversation_id}"
        self.config = {"configurable": {"session_id": self.session_id}}
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        self.vectorstore = Chroma(
            collection_name=self.session_id,
            embedding_function=HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
            ),
        )
        self.retriever = self.vectorstore.as_retriever()
        self.llm = ChatGroq(model="mistral=saba-24b", api_key=GROQ_API_KEY)
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )
        self.question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(
            self.history_aware_retriever, self.question_answer_chain
        )
        self.conversational_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def google_search(self, query, num_results=3):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"q": query, "key": API_KEY, "cx": CSE_ID, "num": num_results}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json().get("items", [])
            links = [result["link"] for result in results]
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during Google search: {e}")
            links = []
        return links

    def get_context(self, links):
        loader = WebBaseLoader(
            links
        )  # use recursiveurlloader with bs4 to get more context
        docs = loader.load()
        splits = self.splitter.split_documents(docs)
        self.vectorstore.add_documents(splits)

    def get_session_history(self):
        return SQLChatMessageHistory(
            self.session_id, "sqlite:///memory.db", table_name="message_store"
        )

    def first_question(self, query):
        links = self.google_search(query)
        self.get_context(links)
        return self.conversational_rag_chain.invoke(
            {"input": query}, config=self.config
        )["answer"]

    def follow_up_question(self, query):
        return self.conversational_rag_chain.invoke(
            {"input": query}, config=self.config
        )["answer"]


# we can use tools and langsmith that would not require memory
# https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/
# https://python.langchain.com/v0.2/docs/how_to/message_history/
