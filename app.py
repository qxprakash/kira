from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from pprint import pprint
import chainlit as cl

load_dotenv()
DATA_FAISS = "vector_store/db_faiss"
embeddings = HuggingFaceEmbeddings(model_name= "sentence-transformers/all-MiniLM-L6-v2", model_kwargs= {"device": "cpu"})


custom_prompt_template = """
    You are kira ai assitant all the information about you has been described below you are a helpful bot
    If you don't know the answer, please just say that you don't know the answer 

    Context: {context}

    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful Answer:
    """

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def set_custom_prompt():
    """
        Prompt Template for QA retrievtal for each vector stores
    """

    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])
    return prompt

# def load_llm():
#     llm = CTransformers(
#         model="",
#         model_type="llama",
#         max_new_tokens=512,
#         tempreature=0.5
#     )

#     return llm




def conversational_chain(llm , prompt, db):
    
    vector = FAISS.load_local(DATA_FAISS, embeddings)
    # pprint(vector)
    # while True:
        # query = input("Query:")
        # query_vector = embeddings.embed_query(query)
        # res = vector.similarity_search_with_score(query)
    c_chain = ConversationalRetrievalChain.from_llm(
        OpenAI(model="gpt-3.5-turbo-0613", temperature=0.2),
        vector.as_retriever(),
        memory=memory
    )

    while True:
        query = input("You: ")
        res = c_chain({"question": query})
        pprint(res["answer"])


conversational_chain()