from fastapi import APIRouter
from service.news_data import get_news_list
from models.news import RequestNewsList, ResponeNewsList, RequestNewsData, ResponseNewsData
from utils.scrape import scrape_webpage
from helpers.prompt import ARTICLE_PAGE_SCRAPING_PROMPT

router = APIRouter() 


@router.post("/get-news-list", description="Get list of news based on preferred sources and user interests.")
async def request_news_list(request_data: RequestNewsList) -> ResponeNewsList:
    result = await get_news_list(request_data.preferred_sources, request_data.user_interests)

    if not result:
        return ResponeNewsList(data=[])
    
    return ResponeNewsList(data=result)


@router.post("/get-news-data", description="Get news data based on the selected news articles.")
async def request_news_data(request_data: RequestNewsData) -> ResponseNewsData:
    result = await scrape_webpage(ARTICLE_PAGE_SCRAPING_PROMPT, request_data.url)

    return ResponseNewsData(**result)
