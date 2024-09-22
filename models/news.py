from pydantic import BaseModel, ConfigDict
import typing as t


# for /get-news-list route

class RequestNewsList(BaseModel):
    preferred_sources: t.List[int] # list of ids of preferred sources
    user_interests: t.List[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "preferred_sources": [1, 2, 3],
                "user_interests": ["technology", "sports", "business"]
            }
        },
    )


class ResponeNewsList(BaseModel):
    data: t.List[t.Dict[str, str]]

    model_config = ConfigDict(
        populate_by_name=True, # Populate the model with the values from the JSON by name (e.g. `{"name": "Jane Doe"}` will populate the `name` field)
        arbitrary_types_allowed=True, # Allow arbitrary types to be passed in the JSON (e.g. `datetime`, `ObjectId`, etc.)
        json_schema_extra={
            "example": {
                "data": [
                    {
                        "title": "Lorem ipsum",
                        "link": "https://www.example.com/news/lorem-ipsum",
                        "source": "Example News",
                        "publish_date": "2021-10-18 00:00:00",
                    }
                ]
            }
        },
    )


# for /get-news-data route

class RequestNewsData(BaseModel):
    url: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://www.example.com/news/lorem-ipsum"
            }
        },
    )


class ResponseNewsData(BaseModel):
    # title: str
    image: str
    summary: str
    # author: str
    # publish_date: str
    # relative_resources: t.List[t.Dict[str, str]]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Lorem ipsum",
                "top_image": "https://www.example.com/image.jpg",
                "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "author": "John Doe",
                "publish_date": "2021-10-18 00:00:00",
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
            }
        },
    )

