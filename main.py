import manager

def main():
    bm = manager.BookManager('../abc_books')
    books = bm.search()
    
main()