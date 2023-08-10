import sys
import time

from Database import Database

d = Database()

#   ______   __       __       __   ______   ______   ______   ______   __  __
#  /\  __ \ /\ \     /\ \     /\ \ /\  == \ /\  == \ /\  __ \ /\  == \ /\ \_\ \
#  \ \  __ \\ \ \    \ \ \____\ \ \\ \  __< \ \  __< \ \  __ \\ \  __< \ \____ \
#   \ \_\ \_\\ \_\    \ \_____\\ \_\\ \_____\\ \_\ \_\\ \_\ \_\\ \_\ \_\\/\_____\
#    \/_/\/_/ \/_/     \/_____/ \/_/ \/_____/ \/_/ /_/ \/_/\/_/ \/_/ /_/ \/_____/
#

# Print out ascii file
with open("files/ascii.txt", "r") as f:
    print(f.read())

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
        book = d.bdb.get_book(book_id)
        print(f"Selected book: {book['title']} by {book['author']}")


d.bdb.close_connection()
