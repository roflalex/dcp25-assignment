import glob
import pathlib
import re
import sqlite3
import parser 
from dataclasses import dataclass

logger = logging.getLogger('books')

@dataclass 
class BookMetadata:
    path: str
    prefix: str
    index: int
    name: str

@dataclass
class Tune:
    #X:
    reference_number: int
    #T 
    title: str
    #L
    length: str
    #R 
    rhythm: str
    #K 
    key:str
    
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
    

    def parse(self, books: list[BookMetadata]) -> list[Tune]:

        data = [{ 'book': book, 'parser': parser.ABCParser(book.path)} for book in books]

