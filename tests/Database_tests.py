import unittest

from langchain.embeddings import OpenAIEmbeddings

from src.Database import VectorDatabase


class VectorDatabaseTests(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.vdb = VectorDatabase(embeddings=OpenAIEmbeddings())

    def test_epub_loader(self):
        print(self.vdb.add_epub("bookdata/Dune-Frank-Herbert.epub"))


if __name__ == '__main__':
    unittest.main()
