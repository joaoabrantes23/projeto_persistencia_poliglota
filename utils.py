from typing import Any
import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_PATH = os.getenv("SQLITE_PATH", "projeto_poliglota.sqlite")
