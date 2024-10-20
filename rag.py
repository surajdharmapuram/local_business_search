from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

urls = ['https://www.makernexus.org/cart', 'https://www.makernexus.org/',
        'https://www.makernexus.org/power-up-campaign', 'https://www.makernexus.org/join-maker-nexus',
        # 'https://www.makernexus.org/visit-maker-nexus', 'https://www.makernexus.org/classes',
        # 'https://www.makernexus.org/youth-programs', 'https://www.makernexus.org/group-events',
        # 'https://www.makernexus.org/teambuilding', 'https://www.makernexus.org/kids-birthday-parties',
        # 'https://www.makernexus.org/reserve-a-room', 'https://www.makernexus.org/donate',
        # 'https://www.makernexus.org/about-us', 'https://www.makernexus.org/aboutus',
        # 'https://www.makernexus.org/facilities-and-tools', 'https://www.makernexus.org/covid-shield-nexus',
        # 'https://www.makernexus.org/jobs', 'https://www.makernexus.org/covid-19',
        # 'https://www.makernexus.org/cancellations', 'https://www.makernexus.org/shortcuts',
        # 'https://www.makernexus.org/contactus', 'https://www.makernexus.org/subscribe',
        # 'https://www.makernexus.org/donate', 'https://www.makernexus.org/',
        # 'https://www.makernexus.org/power-up-campaign', 'https://www.makernexus.org/join-maker-nexus',
        # 'https://www.makernexus.org/visit-maker-nexus', 'https://www.makernexus.org/classes',
        # 'https://www.makernexus.org/youth-programs', 'https://www.makernexus.org/group-events',
        # 'https://www.makernexus.org/teambuilding', 'https://www.makernexus.org/kids-birthday-parties',
        # 'https://www.makernexus.org/reserve-a-room', 'https://www.makernexus.org/donate',
        # 'https://www.makernexus.org/about-us', 'https://www.makernexus.org/aboutus',
        # 'https://www.makernexus.org/facilities-and-tools', 'https://www.makernexus.org/covid-shield-nexus',
        # 'https://www.makernexus.org/jobs', 'https://www.makernexus.org/covid-19',
        # 'https://www.makernexus.org/cancellations', 'https://www.makernexus.org/shortcuts',
        # 'https://www.makernexus.org/contactus', 'https://www.makernexus.org/subscribe',
        # 'https://www.makernexus.org/donate', 'https://www.makernexus.org/power-up-campaign',
        # 'https://www.makernexus.org/join-maker-nexus', 'https://www.makernexus.org/visit-maker-nexus',
        # 'https://www.makernexus.org/classes', 'https://www.makernexus.org/youth-programs',
        # 'https://www.makernexus.org/group-events', 'https://www.makernexus.org/',
        # 'https://www.makernexus.org/teambuilding', 'https://www.makernexus.org/kids-birthday-parties',
        # 'https://www.makernexus.org/reserve-a-room', 'https://www.makernexus.org/donate',
        # 'https://www.makernexus.org/about-us', 'https://www.makernexus.org/', 'https://www.makernexus.org/aboutus',
        # 'https://www.makernexus.org/facilities-and-tools', 'https://www.makernexus.org/covid-shield-nexus',
        # 'https://www.makernexus.org/jobs', 'https://www.makernexus.org/covid-19',
        # 'https://www.makernexus.org/cancellations', 'https://www.makernexus.org/shortcuts',
        # 'https://www.makernexus.org/contactus', 'https://www.makernexus.org/subscribe',
        # 'https://www.makernexus.org/donate', 'https://www.makernexus.org/power-up-campaign',
        # 'https://www.makernexus.org/join-maker-nexus', 'https://www.makernexus.org/classes',
        # 'https://www.makernexus.org/youth-programs', 'https://www.makernexus.org/group-events-teambuilding',
        # 'https://www.makernexus.org/join-maker-nexus#signup', 'https://www.makernexus.org/donate',
        # 'https://www.makernexus.org/cancellations', 'https://www.makernexus.org/covid-19',
        'https://www.makernexus.org/privacy-policy']


def get_url_content(urls):
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    return docs_list

if __name__ == '__main__':
    data = get_url_content(urls)
    print('done getting url data')
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

    llm = ChatOllama(model="llama3", format="json", temperature=0)
    prompt = PromptTemplate(
        template="""system
    You are a grader assessing relevance of a retrieved document to a user question. If the document contains keywords related to the user question, grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
        Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.
        Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
        user
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user question: {question} \n assistant""",
        input_variables=["question", "document"],
    )
    retrieval_grader = prompt | llm | JsonOutputParser()





