import requests
import logging
from datetime import datetime, timedelta
import telegram
import re
import asyncio
import time

from config import (
    NEWS_API_ENDPOINT,
    NEWS_KEYWORDS,
    NEWS_LANGUAGE,
    NEWS_SORT_BY,
    NEWS_PAGE_SIZE,
    GROQ_API_ENDPOINT,  # New
)

logger = logging.getLogger(__name__)


def fetch_news_articles(api_key):
    """
    Fetches recent news articles based on keywords in config.
    """
    if not api_key:
        logger.error("NewsAPI key is missing.")
        return []

    logger.info(f"Fetching news with keywords: {NEWS_KEYWORDS}")
    articles = []

    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        params = {
            "q": NEWS_KEYWORDS,
            "apiKey": api_key,
            "language": NEWS_LANGUAGE,
            "sortBy": NEWS_SORT_BY,
            "pageSize": NEWS_PAGE_SIZE,
            "from": yesterday,
        }

        response = requests.get(NEWS_API_ENDPOINT, params=params, timeout=15)

        response.raise_for_status()
        data = response.json()

        if data.get("status") == "ok":
            articles = data.get("articles", [])
            logger.info(f"Successfully fetched {len(articles)} articles from NewsAPI.")
        else:
            logger.error(
                f"NewsAPI returned status '{data.get('status')}': {data.get('message')}"
            )
            articles = []
    except requests.exceptions.Timeout:
        logger.error("Request to NewsAPI timed out.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news from NewsAPI: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during news fetching: {e}")

    return articles


def query_groq_api(api_key, model_id, messages, temperature=0.7, max_tokens=1024):
    """
    Queries the Groq API chat completions endpoint.
    messages: A list of message objects (e.g., [{"role": "user", "content": "Hello!"}])
    """
    if not api_key:
        logger.error(f"Groq API key is missing for model {model_id}.")
        return None

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    logger.info(f"Querying Groq model {model_id}...")
    try:
        response = requests.post(
            GROQ_API_ENDPOINT, headers=headers, json=payload, timeout=120
        )
        if response.status_code != 200:
            logger.error(
                f"Groq API returned non-200 status: {response.status_code}. Response text: {response.text[:1000]}"
            )
        response.raise_for_status()  # Will raise for 4xx/5xx

        data = response.json()

        api_choices = data.get("choices")
        if api_choices and len(api_choices) > 0:
            # Access 'message' and 'content' as dictionary keys as well
            message_obj = api_choices[0].get("message")
            if message_obj and "content" in message_obj:
                content = message_obj["content"]
                logger.info(
                    f"Successfully received response from Groq model {model_id}."
                )

                # Check and log token usage if available
                usage_data = data.get("usage")
                if usage_data:
                    prompt_tokens = usage_data.get("prompt_tokens", "N/A")
                    completion_tokens = usage_data.get("completion_tokens", "N/A")
                    total_tokens = usage_data.get("total_tokens", "N/A")
                    logger.info(
                        f"Groq Usage - Prompt: {prompt_tokens}, Completion: {completion_tokens}, Total: {total_tokens}"
                    )
                return content.strip()
        else:
            logger.error(
                f"No 'choices' in Groq response or 'choices' is empty. Full Groq response data: {data}"
            )
            # Check if there's an 'error' object in the response
            if "error" in data:
                logger.error(f"Groq API error details: {data['error']}")
            return None
    except requests.exceptions.Timeout:
        logger.error(f"Request to Groq model {model_id} timed out.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying Groq model {model_id}: {e}")
        if hasattr(e, "response") and e.response is not None:
            logger.error(
                f"Groq Response Status: {e.response.status_code}, Body: {e.response.text[:500]}"
            )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during Groq query for {model_id}: {e}"
        )
        return None


def escape_markdown_v2(text: str) -> str:
    """Escapes special characters for Telegram MarkdownV2."""
    if not text:
        return ""

    escape_chars = r"([_*\[\]()~`>#\+\-=|{}.!])"
    return re.sub(escape_chars, r"\\\1", text)


async def send_telegram_message(bot_token, chat_id, message_text):
    """Sends a message to a Telegram chat."""
    if not bot_token or not chat_id:
        logger.warning("Telegram token or chat ID missing, cannot send message.")
        return False

    escaped_message_text = escape_markdown_v2(message_text)

    try:
        bot = telegram.Bot(token=bot_token)
        logger.info(
            f"Attempting to send async message to Telegram chat ID {chat_id}..."
        )
        await bot.send_message(
            chat_id=chat_id,
            text=escaped_message_text,
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
        )
        logger.info("Message sent successfully to Telegram.")
        return True
    except telegram.error.BadRequest as e:
        logger.error(f"Telegram BadRequest Error: {e.message}")
        return False
    except telegram.error.NetworkError as e:
        logger.error(f"Telegram Network Error: {e.message}")
        return False
    except telegram.error.TelegramError as e:
        logger.error(f"Telegram API Error: {e.message}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred sending to Telegram: {e}")
        return False
