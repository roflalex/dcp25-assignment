import manager

def db():
    bm = manager.BookManager('abc_books')
    bdb = manager.BookDatabase('books.db')
    books = bm.search()
    tunes = bm.parse(books)
    bdb.setup()
    bdb.insert_bulk(tunes)
    bdb.get_all_tunes()
db()