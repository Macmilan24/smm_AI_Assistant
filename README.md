## 🌟 Overview

This project is an AI-driven assistant designed to automate key parts of the social media content curation and drafting workflow for Social Media Managers (SMMs) and Content Marketers. It specifically focuses on sourcing news related to Artificial Intelligence (AI) and Machine Learning (ML), then leveraging the powerful Groq API with Llama3 models to generate summaries and platform-specific post drafts.

The assistant proactively monitors news sources, selects relevant articles, uses AI for summarization and tailored draft generation (Twitter & LinkedIn), and delivers these insights daily via Telegram for review.

## ✨ Features

- **Automated Content Discovery:** Fetches the latest AI/ML news daily using NewsAPI.
- **AI-Powered Summarization:** Utilizes Groq API (Llama3 model) to generate concise summaries of selected articles.
- **Platform-Specific Draft Generation:** Employs Groq API (Llama3 model) to create distinct draft posts optimized for Twitter and LinkedIn, including relevant hashtags.
- **Scheduled Operation:** Runs automatically at a configured time each day using the `schedule` library.
- **Telegram Notifications:** Delivers the generated summaries and social media drafts directly to a specified Telegram chat.
- **Configurable:** Easily configured via a `.env` file for API keys and a `config.py` file for operational parameters (keywords, schedule time, model IDs, etc.).
- **Robust Logging:** Comprehensive logging for monitoring and debugging.

## 🛠️ Tech Stack

- **Language:** Python 3.9+
- **Core Libraries:**

  - `requests`: For HTTP API calls to NewsAPI and Groq API.
  - `python-telegram-bot`: For interacting with the Telegram Bot API.
  - `schedule`: For in-script job scheduling.
  - `python-dotenv`: For managing environment variables from a `.env` file.
  - `asyncio`: For handling asynchronous Telegram API calls.

- **Third-Party APIs:**

  - **NewsAPI:** For fetching news articles.
  - **Groq API:** For AI-powered summarization and text generation (using Llama3 models like `llama3-8b-8192`).
  - **Telegram Bot API:** For sending notifications.

## ⚙️ Setup and Installation

1. **Prerequisites:**

   - Python 3.9 or higher.
   - `pip` (Python package installer).

2. **Clone the Repository (or Get Project Files):**

   ```bash
   # If you have it in a git repo:
   # git clone https://github.com/Macmilan24/smm_AI_Assistant.git
   # cd smm_AI_Assistant
   ```

   Ensure you have all the project files (`main.py`, `api_clients.py`, `ai_processing.py`, `config.py`) in your project directory.

3. **Create and Activate a Virtual Environment:**

   ```bash
   # For Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables:**
   Create a `.env` file in the root directory:

   ```env
   NEWS_API_KEY=YOUR_NEWS_API_KEY_HERE
   GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
   TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
   TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID_HERE
   ```

   - `NEWS_API_KEY`: [newsapi.org](https://newsapi.org/)
   - `GROQ_API_KEY`: [console.groq.com](https://console.groq.com/keys)
   - `TELEGRAM_BOT_TOKEN`: Get from BotFather on Telegram.
   - `TELEGRAM_CHAT_ID`: Can be found via `/start` command or Telegram bot ID services.

6. **Configure Parameters (Optional):**
   Edit `config.py` as needed:

   - `NEWS_KEYWORDS`, `MAX_ARTICLES_TO_PROCESS`
   - `GROQ_SUMMARIZATION_MODEL`, `GROQ_GENERATION_MODEL`
   - `SCHEDULE_TIME`, `RUN_IMMEDIATELY_ON_START`
   - Logging and other AI settings

## 🚀 Running the Agent

Run the assistant with:

```bash
python main.py
```

- If `RUN_IMMEDIATELY_ON_START` is True, one run executes immediately.
- Then it waits for `SCHEDULE_TIME` for next scheduled run.
- Logs activity and sends updates to Telegram.
- Press Ctrl+C to stop.

## 📂 Project Structure

```
smm_ai_assistant/
├── .env                    # API keys and secrets (not version controlled)
├── config.py               # Configuration and parameters
├── api_clients.py          # Handles NewsAPI, Groq API, Telegram API
├── ai_processing.py        # Summarization and post generation logic
├── main.py                 # Main script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 📝 Solution Design

Refer to `Solution_Design_Document.pdf` for architecture, data flow, and design details.

## 💡 Potential Future Improvements

- **Smarter Article Selection:** Use semantic similarity and advanced filters.
- **Visual Suggestions:** Suggest images/videos for posts.
- **Interactive Telegram Bot:** Accept commands to generate content or adjust config.
- **Trend Analysis:** Detect and prioritize trending AI/ML topics.
- **Performance Analytics:** Connect to social media insights APIs.
- **More Platform Support:** Add Instagram, Facebook, etc.
- **Web UI:** Simple interface for managing settings and viewing past outputs.

---
