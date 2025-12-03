import glob
import pathlib
import re
import sqlite3
import parser 
import logging
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
    #M 
    meter: str
    #L
    length: str
    #R 
    rhythm: str
    #K 
    key:str
    
