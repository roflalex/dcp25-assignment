import glob
import pathlib
import re #to do regex
import sqlite3
import parser 
from dataclasses import dataclass
import pandas as pd

@dataclass 
class BookMetadata:
    path: str
    prefix: str
    index: int
    name: str

@dataclass
class Tune:
    #X:
    reference: int
    #T 
    title: str
    #R 
    rhythm: str
    #K 
    key:str
    book_no: int
class BookManager:
    pattern: str
    base: str

    def __init__(self,base:str):
        self.base = base
        self.pattern = str(pathlib.Path(base) / "*/*.abc")
    
    def _load_possible_tunes(self)->list[str]:
        return glob.glob(self.pattern)
    #find all possible tunes in the directory
    def search(self)-> list[BookMetadata]:
        paths = self._load_possible_tunes()
        paths = [pathlib.Path(p) for p in paths]
        #^ = start regex
        #() = capture regex
        #(.*) is the range for the regex
        #testaalex
        #[0] = testaalex
        #[1] = test
        #[2] = alex
        #?: = non capturing group i.e. im looking for the / and the \ but i dont want to return it
        #[0:9] = look for digits and match 
        # this is bc the directory needs numbers 
        # (.*) means accept any name of file
        # finally look for file name ending in .abc
        
        pattern = r"^(.*)(?:/|\\)([0-9]+)(?:/|\\)(.*)\.abc$"
        paths = [p for p in paths if p.is_file()]
        #matches pattern to the path
        paths = [re.match(pattern,str(p)) for p in paths]
        # construct capturing groups 
        return [BookMetadata(p[0], p[1], p[2], p[3]) for p in paths if p is not None]        
    
    #type hint to help me remember what im putting in adn returning from the method
    def parse(self, books: list[BookMetadata]) -> list[Tune]:

        #put regex path into parser
        data = []
        for book in books:
            data.append({'book':book,'parser': parser.ABCParser(book.path)})    

        tunes = []    
        for x in data:
            book = x['book']
            meta = x['parser'].metadata
            reference = int(meta['reference'])
            tunes.append(Tune(
                reference,
                meta['title'],
                rhythm=meta.get('rhythm', 'Unknown'),  
                key=meta.get('key', 'Ador'),           
                book_no=int(book.index)                
        ))
        return tunes

class BookDatabase:
    
    dbname: str
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self,db_name):
        self.dbname = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def setup(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tunes (
                tune_id INTEGER PRIMARY KEY,
                reference INTEGER,
                book_no INTEGER,
                title TEXT,
                rhythm TEXT,
                key TEXT    
                )
            """)
    
    def insert_bulk(self,tunes):
        temp = []
        for tune in tunes:
            temp.append((tune.reference,tune.book_no,tune.title,tune.rhythm,tune.key))

        self.cursor.executemany("""
            INSERT INTO tunes (reference, book_no, title, rhythm, key)
            VALUES (?,?,?,?,?)
        """,temp)
        
    def get_all_tunes(self):
        query = "SELECT * FROM tunes"
        df = pd.read_sql(query, self.conn)
        print(df.head())
        return df
    
    def get_tunes_by_rhythm(self, rhythm):
        """Get all tunes from a specific book"""
        df = self.get_all_tunes()
        filter = df[df['rhythm'] == rhythm]
        return filter

    def get_tunes_by_book(self, book_number):
        """Get all tunes from a specific book"""
        df = self.get_all_tunes()
        filter = df[df['book_no'] == book_number]
        return filter

    def search_tunes(self, search):
        """Search tunes by title"""
        df = self.get_all_tunes()
        temp = (df['title']).str.contains(search, case=False)
        filter = df[temp]
        return filter    
    def get_tune_by_reference(self, reference):
        df = self.get_all_tunes()
        filter = df[df['reference'] == reference]
        return filter
    def most_common_keys(self, n=10):
        df = self.get_all_tunes()
        filter = df['key'].value_counts().head(n)
        return filter
    
    def title_length_stats(self):
        df = self.get_all_tunes()
        df['title_length'] = df['title'].str.len()
        return df['title_length'].describe()



        