import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

CATEGORIES = [
    "Housing & Utilities",
    "Food & Groceries",
    "Transportation",
    "Entertainment & Dining",
    "Shopping & Lifestyle",
    "Savings & Investments",
    "Miscellaneous"
]

DEFAULT_50_30_20 = {
    "Needs": 0.50,
    "Wants": 0.30,
    "Savings": 0.20
}