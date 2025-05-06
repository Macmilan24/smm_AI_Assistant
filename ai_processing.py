import logging
from api_clients import query_groq_api  # New
from config import (
    GROQ_API_KEY,
    GROQ_SUMMARIZATION_MODEL,
    GROQ_GENERATION_MODEL,
    MAX_ARTICLE_TEXT_FOR_GROQ,
    GENERATION_TEMPERATURE_GROQ,
)

logger = logging.getLogger(__name__)


def get_text_from_article(article):
    """Extracts usable text (description or content) from a NewsAPI article object."""
    text = article.get("content") or article.get("description") or ""

    if text and "[+" in text and text.endswith(" chars]"):
        text = text[: text.rfind("[+")]
    return text.strip()


def summarize_article_with_groq(article_text):
    """Summarizes article text using Groq API."""
    if not article_text:
        logger.warning("No text provided for summarization.")
        return None

    if len(article_text) > MAX_ARTICLE_TEXT_FOR_GROQ:
        logger.warning(
            f"Article text too long ({len(article_text)} chars), truncating to {MAX_ARTICLE_TEXT_FOR_GROQ}."
        )
        article_text = article_text[:MAX_ARTICLE_TEXT_FOR_GROQ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert news summarization AI. "
                "Distill complex articles into a clear, factual summary tailored for social media audiences."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Summarize the following article in 2–3 concise sentences, preserving key insights "
                f"and factual accuracy without filler:\n\n---\n{article_text}\n---"
            ),
        },
    ]
    max_summary_tokens = 150

    logger.info(
        f"Requesting summarization from Groq model {GROQ_SUMMARIZATION_MODEL}..."
    )
    summary = query_groq_api(
        api_key=GROQ_API_KEY,
        model_id=GROQ_SUMMARIZATION_MODEL,
        messages=messages,
        temperature=0.3,  # Lower temperature for factual summarization
        max_tokens=max_summary_tokens,
    )

    if summary:
        logger.info("Summarization successful with Groq.")
        return summary
    else:
        logger.error(
            f"Failed to get summary from Groq model {GROQ_SUMMARIZATION_MODEL}."
        )
        return None


def generate_social_post_with_groq(model_id, prompt_text, max_post_tokens=150):
    """Generates a social media post using Groq API based on a prompt."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are an industry-leading AI social media strategist and copywriter. "
                "Craft engaging, on-brand posts optimized for platform best practices with clear calls to action."
            ),
        },
        {"role": "user", "content": prompt_text},
    ]

    logger.info(f"Requesting social post generation from Groq model {model_id}...")
    post_draft = query_groq_api(
        api_key=GROQ_API_KEY,
        model_id=model_id,
        messages=messages,
        temperature=GENERATION_TEMPERATURE_GROQ,
        max_tokens=max_post_tokens,
    )

    if post_draft:
        logger.info("Social post generation successful with Groq.")

        if post_draft.startswith('"') and post_draft.endswith('"'):
            post_draft = post_draft[1:-1]
        return post_draft
    else:
        logger.error(f"Failed to generate social post from Groq model {model_id}.")
        return None


def generate_tweet_draft_with_groq(title, summary, url):
    """Generates a tweet draft using Groq."""
    prompt = (
        f"Based on the article below, craft a concise, engaging tweet under 280 characters. "
        f"Use 2–3 strategic hashtags, include a clear call to action, and append the article link.\n\n"
        f'Title: "{title}"\n'
        f'Summary: "{summary}"\n'
        f"Link: {url}\n\n"
        f"Tweet:"
    )
    return generate_social_post_with_groq(
        GROQ_GENERATION_MODEL, prompt, max_post_tokens=100
    )


def generate_linkedin_draft_with_groq(title, summary, url):
    """Generates a LinkedIn post draft using Groq."""
    prompt = (
        f"Using the details below, draft a professional LinkedIn post of 3–4 sentences. "
        f"Highlight key insights, encourage discussion, include 3–4 industry hashtags, and add the link.\n\n"
        f'Title: "{title}"\n'
        f'Summary: "{summary}"\n'
        f"Link: {url}\n\n"
        f"LinkedIn Post:"
    )
    return generate_social_post_with_groq(
        GROQ_GENERATION_MODEL, prompt, max_post_tokens=200
    )
