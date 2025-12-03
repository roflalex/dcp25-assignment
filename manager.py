import glob
import pathlib
import re
import sqlite3
import parser 
import logging
from dataclasses import dataclass

logger = logging.getLogger('books')


