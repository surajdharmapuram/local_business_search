import bs4
from langchain_community.document_loaders import WebBaseLoader

# Only keep post title, headers, and content from the full HTML.
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_paths=('https://www.makernexus.org/group-events',),
    #bs_kwargs={"parse_only": bs4_strainer},
)
docs = loader.load()
print('loaded docs')
print(docs)
print(len(docs[0].page_content))