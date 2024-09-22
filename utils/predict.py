from groq import Groq
import os
import datetime
import dotenv
import typing as t
from helpers.common import parse_json_garbage_with_safety
from helpers.prompt import USER_PREFERED_NEWS_PROMPT

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