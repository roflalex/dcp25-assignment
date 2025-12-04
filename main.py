import manager

def main():
    bm = manager.BookManager('abc_books')
    bdb = manager.BookDatabase('books.db')
    books = bm.search()
    tunes = bm.parse(books)
    bdb.setup()
    bdb.insert_bulk(tunes)
    print("successfully made database")
    bdb.get_all_tunes()
main()