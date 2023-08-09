import requests
from difflib import SequenceMatcher

def search_books(title, author):
    base_url = "http://openlibrary.org/search.json"
    query = f"{title}"
    params = {
        "q": query
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        docs = data.get("docs", [])

        max_ratio = 0
        max_isbn = None

        for doc in docs:
            doc_title = doc.get("title", "")
            doc_author = doc.get("author_name", [])
            isbn = doc.get("isbn", [])

            # Calculate similarity ratio between book title and given title
            title_ratio = SequenceMatcher(None, doc_title, title).ratio()

            # Calculate similarity ratio between book author and given author
            author_ratio = SequenceMatcher(None, doc_author, author).ratio()

            # Calculate a combined score using both ratios
            score = (title_ratio + author_ratio) / 2

            # If score is greater than previous max, update max
            if score > max_ratio:
                max_ratio = score
                max_isbn = isbn

        return max_isbn

    else:
        print("Error occurred while retrieving book data.")

isbn = search_books("The Great Gatsby", "F Scott Fitzgerald")
print(isbn[0])