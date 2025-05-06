import os
from dotenv import load_dotenv
import logging

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

GROQ_SUMMARIZATION_MODEL = "llama3-8b-8192"
GROQ_GENERATION_MODEL = "llama3-8b-8192"

NEWS_KEYWORDS = '"artificial intelligence" OR "machine learning" OR "LLM" OR "AI ethics" OR "AI regulation"'
NEWS_LANGUAGE = "en"
NEWS_SORT_BY = "relevancy"
NEWS_PAGE_SIZE = 10
MAX_ARTICLES_TO_PROCESS = 1

MAX_ARTICLE_TEXT_FOR_GROQ = 7000
GENERATION_TEMPERATURE_GROQ = 0.6

SCHEDULE_TIME = "08:00"
RUN_IMMEDIATELY_ON_START = True

LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

if not NEWS_API_KEY:
    logging.warning("NEWS_API_KEY not found")
if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not found")
if not TELEGRAM_BOT_TOKEN:
    logging.warning("TELEGRAM_BOT_TOKEN not found")
if not TELEGRAM_CHAT_ID:
    logging.warning("TELEGRAM_CHAT_ID not found")
