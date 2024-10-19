from data.source import NEWS_SOURCES
import typing as t

def get_news_outlet() -> t.Dict[str, t.List[t.Dict[str, t.Optional[str]]]]:
    """Get list of news outlets"""
    return {"data": NEWS_SOURCES}




