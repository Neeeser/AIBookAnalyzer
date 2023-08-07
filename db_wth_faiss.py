import os
import getpass

import faiss
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.embeddings.gpt4all import GPT4AllEmbeddings

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()  # loads env variables
# # Load the document, split it into chunks, embed each chunk and load it into the vector store.
raw_documents = TextLoader("bookdata/greatgatsby.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = FAISS.from_documents(documents, GPT4AllEmbeddings())
db.save_local("faiss_db", index_name="bookindex")
# Query the vector store with a question.
# db = FAISS.load_local(
#     "faiss_db", index_name="bookindex", embeddings=GPT4AllEmbeddings()
# )

# model = ChatOpenAI(model_name="gpt-3.5-turbo")
# qa = ConversationalRetrievalChain.from_llm(model, retriever=db.as_retriever())

questions = [
    "Please summarize chapter one",
]

template = """Question: {question}

Answer: Let's think step by step."""


prompt = PromptTemplate(template=template, input_variables=["question"])

local_path = "models/llama-2-7b-chat.ggmlv3.q4_0.bin"  # replace with your desired local file path

chat_history = []

# for question in questions:
#     result = qa({"question": question, "chat_history": chat_history})
#     chat_history.append((question, result["answer"]))
#     print(f"Question: \n {question} \n")
#     print(f"Answer: \n {result['answer']} \n")
#     print("------------------------------------------------------- \n")

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)
qa = ConversationalRetrievalChain.from_llm(llm, retriever=db.as_retriever())

# llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "Summarize chapter 1"

result = qa({"question": question, "chat_history": chat_history})
chat_history.append((question, result["answer"]))
print(f"Question: \n {question} \n")
print(f"Answer: \n {result['answer']} \n")
print("------------------------------------------------------- \n")


# llm_chain.run(question)
