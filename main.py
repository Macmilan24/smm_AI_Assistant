import schedule
import time
import logging
import asyncio

from config import (
    NEWS_API_KEY,
    GROQ_API_KEY,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    MAX_ARTICLES_TO_PROCESS,
    SCHEDULE_TIME,
    RUN_IMMEDIATELY_ON_START,
    LOGGING_LEVEL,
    LOGGING_FORMAT,
)
from api_clients import fetch_news_articles, send_telegram_message

from ai_processing import (
    get_text_from_article,
    summarize_article_with_groq,
    generate_tweet_draft_with_groq,
    generate_linkedin_draft_with_groq,
)

logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)


def run_assistant_workflow():
    logger.info("=============================================")
    logger.info("=== Running SMM AI Assistant Workflow ===")
    logger.info("=============================================")

    if not GROQ_API_KEY:
        logger.error("CRITICAL: GROQ_API_KEY is not set. Aborting workflow.")
        return

    articles = fetch_news_articles(NEWS_API_KEY)
    selected_articles = []
    for article in articles:
        text = get_text_from_article(article)
        if text:
            selected_articles.append(article)
            if len(selected_articles) >= MAX_ARTICLES_TO_PROCESS:
                break
    if not selected_articles:
        logger.info("No articles with sufficient text found. Workflow ending.")
        return
    logger.info(f"Processing {len(selected_articles)} selected article(s)...")

    final_output = []
    for article in selected_articles:
        title = article.get("title", "No Title")
        url = article.get("url", "#")
        source_name = article.get("source", {}).get("name", "Unknown Source")
        logger.info(f"\n--- Processing Article ---")
        logger.info(f"Title: {title}\nSource: {source_name}\nURL: {url}")

        article_text = get_text_from_article(article)

        summary = summarize_article_with_groq(article_text)
        if not summary:
            logger.error(
                f"Failed to summarize article: {title}. Skipping draft generation."
            )
            continue

        logger.info(f"Summary: {summary[:150]}...")

        tweet_draft = generate_tweet_draft_with_groq(title, summary, url)
        linkedin_draft = generate_linkedin_draft_with_groq(title, summary, url)

        print("\n" + "=" * 20 + f" Drafts for: {title} " + "=" * 20)
        print(f"URL: {url}")
        print("\n--- DRAFT TWEET ---")
        print(tweet_draft or "[Generation Failed]")
        print("\n--- DRAFT LINKEDIN POST ---")
        print(linkedin_draft or "[Generation Failed]")
        print("=" * (42 + len(title)) + "\n")

        output_block = (
            f"*Article:* [{title}]({url})\n\n"
            f"*AI Summary:* {summary}\n\n"
            f"*Draft Tweet:*\n{tweet_draft or '[Generation Failed]'}\n\n"
            f"*Draft LinkedIn Post:*\n{linkedin_draft or '[Generation Failed]'}\n\n"
            f"--------------------\n"
        )
        final_output.append(output_block)

    if final_output and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        logger.info("Sending combined drafts to Telegram...")
        full_telegram_message = "🚀 *Daily AI Social Media Drafts* 🚀\n\n" + "\n".join(
            final_output
        )
        max_len = 4000
        if len(full_telegram_message) > max_len:
            logger.warning("Combined Telegram message too long, truncating...")
            full_telegram_message = (
                full_telegram_message[: max_len - 100]
                + "\n\n... \\[Message Truncated\\]"
            )

        try:
            success = asyncio.run(
                send_telegram_message(
                    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, full_telegram_message
                )
            )
            if success:
                logger.info("Telegram message dispatch handled by asyncio.")
            else:
                logger.error("Async Telegram message dispatch reported failure.")
        except Exception as e:
            logger.error(
                f"Error running send_telegram_message_async with asyncio.run: {e}"
            )
    elif not final_output:
        logger.info("No final drafts generated to send.")

    logger.info("=============================================")
    logger.info("=== SMM AI Assistant Workflow Finished ===")
    logger.info("=============================================")


def start_scheduler():
    logger.info(f"Scheduling job daily at {SCHEDULE_TIME}.")
    schedule.every().day.at(SCHEDULE_TIME).do(run_assistant_workflow)
    if RUN_IMMEDIATELY_ON_START:
        logger.info("Running job once immediately on start...")
        run_assistant_workflow()
    logger.info("Scheduler started. Waiting for scheduled time...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    if not NEWS_API_KEY:
        logger.error("CRITICAL: Missing NEWS_API_KEY in config/.env. Exiting.")
    else:
        try:
            start_scheduler()
        except KeyboardInterrupt:
            logger.info("Scheduler stopped manually.")
        except Exception as e:
            logger.exception(
                f"An uncaught exception occurred in the scheduler loop: {e}"
            )
