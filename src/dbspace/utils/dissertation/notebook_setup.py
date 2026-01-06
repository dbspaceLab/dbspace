import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

global DATADIR
DATADIR = os.getenv("DATA_DIRECTORY")
