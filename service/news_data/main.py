import typing as t
from utils.rss_feeds import load_rss_data
from utils.scrape import scrape_webpage
from groq import Groq
import os
import datetime
import dotenv
from helpers.common import parse_json_garbage_with_safety, convert_relative_time
from helpers.news import get_news_source_details
from helpers.prompt import USER_PREFERED_NEWS_PROMPT, LIST_OF_ARTICLES_PAGE_SCRAPING_PROMPT, ARTICLE_PAGE_SCRAPING_PROMPT


dotenv.load_dotenv() # Load environment variables from .env file


async def predict_news_list(user_interests: t.List[str], news_list: t.List[t.Dict[str, str]]) -> t.List[t.Dict[str, str]]:
    """Predict news list based on user interests using AI"""

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    user_interests = ", ".join(user_interests) # Convert list to string
    current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get current date and time (like 2021-10-18 00:00:00)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": USER_PREFERED_NEWS_PROMPT.format(user_interests=user_interests, news_data=news_list, current_date_time=current_date_time),
            }
        ],
        # model="mixtral-8x7b-32768",
        # model="llama-3.1-8b-instant",
        # model="llama3-70b-8192",
        model="llama3-8b-8192",
    )

    result = chat_completion.choices[0].message.content
    result_json = parse_json_garbage_with_safety(result)
    print("result_json", result_json)

    if not result_json or not result_json.get("selected_news"):
        return {"selected_news": []}

    return result_json


async def get_news_list(preferred_sources: t.List[int], user_interests: t.List[str]) -> t.Optional[t.List[t.Dict[str, str]]]:
    """Get news data based on preferred sources and user interests"""

    result = []

    for source_id in preferred_sources: # from each news outlets
        source_details = get_news_source_details(source_id)
        type = source_details.get("type")
        if type == "rss":
            url = source_details.get("url")

            # Load RSS feed data
            loaded_data = await load_rss_data(url, user_interests) 
            if not loaded_data:
                continue

            # Check if the title contains any of the user interests using AI
            predicted_news_list = await predict_news_list(user_interests, loaded_data)
            print(predicted_news_list)  

            for news_data in loaded_data: # from each news/articles of the news outlet
                if news_data:
                    
                    # Check if the news article falls under the user interests
                    if int(news_data["id"]) not in predicted_news_list["selected_news"]:
                        continue

                    news_data.pop("id") # `id` is not needed in the response
                    news_data["source"] = source_details.get("name") # Add news source name to the response
                    result.append(news_data)
        
        # Support for web scraping from webpages
        elif type == "webpage":
            url = source_details.get("url")

            # Scrape the webpage
            scraped_data = await scrape_webpage(LIST_OF_ARTICLES_PAGE_SCRAPING_PROMPT, url)

            scraped_data = convert_relative_time(scraped_data) # Relative time to absolute datetime
            scraped_data = scraped_data.get("data") # Get the list of articles

            if not scraped_data:
                continue

            # Add unique ID to each news article
            for i, news_data in enumerate(scraped_data):
                news_data["id"] = i + 1

            # Check if the title contains any of the user interests using AI
            predicted_news_list = await predict_news_list(user_interests, scraped_data)
            print(predicted_news_list)

            for news_data in scraped_data: # from each news/articles of the news outlet
                if news_data:
                    
                    # Check if the news article falls under the user interests
                    if int(news_data["id"]) not in predicted_news_list["selected_news"]:
                        continue

                    news_data.pop("id") # `id` is not needed in the response
                    news_data["source"] = source_details.get("name") # Add news source name to the response
                    result.append(news_data)

    if not result:
        return None
    
    return result



