# Create an instance of the BookDatabase class
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import GPT4All

from Database import BookDatabase, VectorDatabase

db = BookDatabase("books.db")
vdb = VectorDatabase()
# Add a new book entry
db.delete_all_books()

book_id = db.add_book("Dune", "Frank Herbert", "dune", "Dune-Frank-Herbert.epub")
vdb.create_index("dune", vdb.add_pdf("bookdata/Dune-Frank-Herbert.epub"))
# Search for books
results = db.search_books("dune")

# Print the search results
for book in results:
    print(book)

index = vdb.load_index(results[0]["index_name"])

local_path = "models/GPT4All-13B-snoozy.ggmlv3.q4_0.bin"  # replace with your desired local file path
callbacks = [StreamingStdOutCallbackHandler()]

llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True)
qa = ConversationalRetrievalChain.from_llm(llm, retriever=index.as_retriever())
# question = "Write me a detailed summary of chapter 1. Include important characters mentioned and important events. Talk about themes introcuded in the chapter."
question = "Writ me a detailed summary of chapter 2"
chat_history = []

result = qa({"question": question, "chat_history": chat_history})
chat_history.append((question, result["answer"]))
print(f"Question: \n {question} \n")
print(f"Answer: \n {result['answer']} \n")
print("------------------------------------------------------- \n")

# Close the database connection
db.close_connection()
