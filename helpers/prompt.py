USER_PREFERED_NEWS_PROMPT = """Behave like a human who loves to read lots of articles on {user_interests}. Now tell me which news articles you would like to read from the below ones:
{news_data}

Please enter the id of the news article you would like to read in a list in a json format.
RESPONSE FORMAT:
{{
    "selected_news": [1, 2, 3]
}}
"""

LIST_OF_ARTICLES_PAGE_SCRAPING_PROMPT = """You are a bot who scrapes all the articles from the webpage. You will scrape all the articles in JSON format.
YOUR RESPONSE FORMAT:

{{
    "title": "<title of the article>",
    "link": "<link of the article>",
    "publish_date": "<2021-10-18 00:00:00 or Unknown>"
}}
"""

ARTICLE_PAGE_SCRAPING_PROMPT = """You are a bot who scrapes article pages. You will give me a complete concise and comprehensive summary (not just an overview) of the article's description/body (remember not to insclude other details like title in summary) including images and links inside `summary`. Ensure that the summary is coherent and insightful.

RESPONSE FORMAT:
{{
    "image": "<image of the article or NA>",
    "summary": "<Let's do it!!>"
}}

YOUR RESPONSE:
"""

