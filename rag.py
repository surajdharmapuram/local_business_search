import sys

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_ollama import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from langchain_core.messages import HumanMessage, SystemMessage

main_url = "https://www.manresabread.com/"


def get_url_content(urls):
    print(f"Trying to get content of urls {urls}")
    docs = [WebBaseLoader(web_path=url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    return docs_list


def get_linked_subpage_urls(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        path = link.get('href')
        if path and (path.startswith("/") or path.startswith(url)):
            path = urljoin(url, path)
            yield path


# get url contents
# pass it to llama.
if __name__ == '__main__':
    suburls = get_linked_subpage_urls(main_url, requests.get(main_url).text)
    data = get_url_content(list(suburls))
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=0)
    doc_splits = text_splitter.split_documents(data)
    print('done splitting docs')

    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local"),
    )
    print("created vectorstore")
    retriever = vectorstore.as_retriever()
    print("create retriever")

    llm = ChatOllama(model="llama3.2:1b", format="json", temperature=0)
    print("created llm")

    # messages = [
    #     SystemMessage(
    #         content="Help me answer the following question: 1) What type of business is it? 2) What is the name of this business? 3) what type of products do they sell? 4) How many locations do they have? 5) Is it a local store with only few locations or chain with several nationwide locations?"),
    #     HumanMessage(content=""),
    # ]

    # 2. Incorporate the retriever into a question-answering chain.
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": "Answer the following question: 1) What type of business is it? 2) What is the name of this business? 3) what type of products do they sell? 4) How many locations do they have? 5) Is it a local store with only few locations or chain with several nationwide locations?"})
    print(response)
    print('answer')
    print(response['answer'])
