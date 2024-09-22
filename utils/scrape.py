from scrapegraphai.graphs import SmartScraperGraph
import dotenv
import os
import json
import typing as t
import asyncio
# from helpers.prompt import LIST_OF_ARTICLES_PAGE_SCRAPING_PROMPT, ARTICLE_PAGE_SCRAPING_PROMPT

ARTICLE_PAGE_SCRAPING_PROMPT = """You are a bot who scrapes article pages. You will give me the details of the article including images and links in JSON format.
Please provide the title, top image, content, author, publish date, and relative resources of the article.

YOUR RESPONSE FORMAT:
{{
    "title": "<title of the article or NA>",
    "top_image": "<top image of the article or NA>",
    "content": "<Let's do it!!>",
    "author": "<author of the article or NA>",
    "publish_date": "<2021-10-18 00:00:00 or Unknown>",
    "relative_resources": [
        {
            "type": "image",
            "url": "https://www.example.com/image.jpg"
        },
        {
            "type": "link",
            "url": "https://www.example.com/link"
        }
    ]
}}

Don't give any other letters or ```. Just give me the JSON format. And cross check the JSON format before sending it.
"""


dotenv.load_dotenv() # Load environment variables from .env file


# Configuration for the SmartScraperGraph instance
graph_config = {
   "llm": {
    #   "model": "groq/llama3-8b-8192",
      "model": "groq/llama3-70b-8192",
      "api_key": os.environ.get("GROQ_API_KEY"),
      "verbose": True,
   },
}


async def scrape_webpage(prompt: str, url: str) -> t.Dict[str, str]:
    """
    Scrape the webpage and return the article including images and links in JSON format.
    """
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=url,
        config=graph_config
    )

    # Use asyncio to run in a separate thread if .run() is blocking
    result = await asyncio.to_thread(smart_scraper_graph.run)
    print(result)
    return result


async def scrape_webpage_with_safety(prompt: str, url: str, retries: int = 3) -> t.Dict[str, str]:
    """
    Scrape the webpage and return the article including images and links in JSON format with retries.
    """
    for _ in range(retries):
        try:
            return await scrape_webpage(prompt, url)
        except Exception as e:
            print(f"Error scraping webpage: {e}")
            pass
    return {}


if __name__ == "__main__":
    # Example usage
    result = scrape_webpage(ARTICLE_PAGE_SCRAPING_PROMPT, "https://economictimes.indiatimes.com/wealth/invest/headline-the-investors-toolkit-how-factor-analysis-can-boost-your-investment-game/articleshow/112137713.cms")
    print(json.dumps(result, indent=2))


