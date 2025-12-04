import manager

def main():
    bm = manager.BookManager('abc_books')
    bdb = manager.BookDatabase('books.db')
    books = bm.search()
    tunes = bm.parse(books)
    bdb.setup()
    bdb.insert_bulk(tunes)
    bdb.get_all_tunes()
    bdb.most_common_keys()
    bdb.title_length_stats()
main()