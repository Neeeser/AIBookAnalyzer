from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import GPT4All
from Database import BookDatabase, VectorDatabase


class BookChatBot:
    def __init__(self, book_db_file, model_path):
        self.book_db = BookDatabase(book_db_file)
        self.vector_db = VectorDatabase()
        self.vector_index = None
        self.llm = GPT4All(
            model=model_path, callbacks=[StreamingStdOutCallbackHandler()], verbose=True
        )
        self.qa = None
        self.chat_history = []

    def search_books(self, query):
        return self.book_db.search_books(query)

    def ask_question(self, question):
        if vector_index_name:
            result = self.qa({"question": question, "chat_history": self.chat_history})
            self.chat_history.append((question, result["answer"]))
            return result["answer"]
        else:
            print("No book selected")
            return None

    def set_index(self, index_name):
        self.vector_index = self.vector_db.load_index(index_name)
        self.qa = ConversationalRetrievalChain.from_llm(
            self.llm, retriever=self.vector_index.as_retriever()
        )

    def close(self):
        self.book_db.close_connection()


# Example usage
book_db_file = "books.db"
model_path = "models/GPT4All-13B-snoozy.ggmlv3.q4_0.bin"
bot = BookChatBot(book_db_file, model_path)

results = bot.search_books("gatsby")[0]
vector_index_name = results["index_name"]
bot.set_index(vector_index_name)

for book in results:
    print(book)

question = "Write me a detailed summary of chapter 2"
answer = bot.ask_question(question)
print(f"Question: {question}")
print(f"Answer: {answer}")

bot.close()
