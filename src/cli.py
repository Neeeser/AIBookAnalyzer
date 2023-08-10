import os
import sys
import textwrap
import time

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import GPT4All

from Database import Database, VectorDatabase

d = Database()
vdb = VectorDatabase()
#   ______   __       __       __   ______   ______   ______   ______   __  __
#  /\  __ \ /\ \     /\ \     /\ \ /\  == \ /\  == \ /\  __ \ /\  == \ /\ \_\ \
#  \ \  __ \\ \ \    \ \ \____\ \ \\ \  __< \ \  __< \ \  __ \\ \  __< \ \____ \
#   \ \_\ \_\\ \_\    \ \_____\\ \_\\ \_____\\ \_\ \_\\ \_\ \_\\ \_\ \_\\/\_____\
#    \/_/\/_/ \/_/     \/_____/ \/_/ \/_____/ \/_/ /_/ \/_/\/_/ \/_/ /_/ \/_____/
#

# Print out ascii file
with open("files/ascii.txt", "r") as f:
    print(f.read())


def find_models():
    # Check if open ai key in env
    supported_models = []
    if "OPENAI_API_KEY" in os.environ:
        supported_models.append("chatgpt")
    for model in os.listdir("models"):
        # If extension ends in bin, add to list of models
        if model.endswith(".bin"):
            model = os.path.join("models", model)
            supported_models.append(model)

    return supported_models


def load_model(model):
    if model == "chatgpt":
        return ChatOpenAI(model_name="gpt-3.5-turbo")

    else:
        return GPT4All(model=model)


def select_model(supported_models):
    print("Select a model to use: ")
    for i, model in enumerate(supported_models):
        print(f"{i + 1} - {model}")
    selection = input("Enter the number of the model you want to use: ")
    return supported_models[int(selection) - 1]


supported_models = find_models()


def make_request(model, prompt, loaded_index):
    qa = ConversationalRetrievalChain.from_llm(
        model, retriever=loaded_index.as_retriever()
    )
    chat_history = []
    result = qa({"question": prompt, "chat_history": chat_history})
    chat_history.append((prompt, result["answer"]))
    return result["answer"]


# Create options loop in cli
while True:
    options_text = "Search for a book (1), add a book (2), or quit (3): "
    sys.stdout.write(options_text)
    sys.stdout.flush()

    user_input = ""
    while True:
        char = sys.stdin.read(1)
        if char == "\n":
            break
        user_input += char
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)  # Optional delay for smoother typing effect
    print()

    if user_input == "1":
        # Search for a book
        search_term = input("Enter a search term: ")
        results = d.bdb.search_books(search_term)
        for book in results:
            print(
                f"{book['id']} - {book['title']} - {book['author']} - {book['index_name']}"
            )

        # Ask user to select a book
        book_id = input("Enter the id of the book you want to select: ")
        book = d.bdb.get_book_by_id(book_id)
        print(f"Selected book: {book['title']} by {book['author']}")
        index = book["index_name"]
        load_index = vdb.load_index(index)
        print(load_index)
        print(f"Loaded index: {index}")
        model = select_model(supported_models)
        model = load_model(model)
        print("------------------------------------------------------- \n")
        print("Ask a question about the book. Type 'quit' to exit.")
        user_input = input("Question: ")
        while user_input != "quit":
            print(textwrap.fill(make_request(model, user_input, load_index), 80))
            user_input = input("Question: ")


d.bdb.close_connection()
