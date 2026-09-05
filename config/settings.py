from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_ID = "openai/gpt-oss-20b"

DATA_DIR = BASE_DIR / "data"

PDF_DIR = DATA_DIR / "pdfs"

CHROMA_DIR = DATA_DIR / "chromadb"

SQLITE_DIR = DATA_DIR / "sqlite"