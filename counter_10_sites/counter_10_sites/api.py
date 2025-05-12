import re
from timeit import default_timer as timer

import aiohttp
from ninja import NinjaAPI
from ninja import Schema, Path
from ninja.responses import JsonResponse

api = NinjaAPI()

class TagsSchema(Schema):
    id: str
    url: str
    result: int

class Error(Schema):
    message: str


urls = [
    "https://go.dev",
    "https://www.paradigmadigital.com",
    "https://www.realpython.com",
    "https://www.lapatilla.com",
    "https://www.facebook.com",
    "https://www.gitlab.com",
    "https://www.youtube.com",
    "https://www.mozilla.org",
    "https://www.github.com",
    "https://www.google.com",
]

pattern = r"href=\"(http|https)://"

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def search_tag(data: str, pattern: str) -> int:
    """
    Search the specific tag from file
    :param data: str
    :param pattern: str
    :return: String with matching tags
    """
    count_word = 0

    for tag in re.findall(pattern, str(data)):
        if tag:
         count_word += len(tag.split())

    return count_word

async def results(url):
    """
    Return Tags from url
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)

        return search_tag(html, pattern)

@api.get("/")
def index(request):
    return  {
        "data": [
             {
                 "message": "Welcome to Django Ninja Counter 10 Sites",
                 "version": "v1.0.0"
              }
        ]
    }

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def search_tag(data: str, pattern: str) -> int:
    """
    Search the specific tag from file
    :param data: str
    :param pattern: str
    :return: String with matching tags
    """
    count_word = 0

    for tag in re.findall(pattern, str(data)):
        if tag:
         count_word += len(tag.split())

    return count_word

async def results(url):
    """
    Return Tags from url
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)

        return search_tag(html, pattern)

@api.get("/v1/tags", response={200: TagsSchema, 403: Error})
async def get_tags(request):
    """
    Get pattern https?://
    :return: JSON with results
    """

    start = timer()
    content = []

    for url_id, url in enumerate(urls):
        result = await results(url)

        if result:
            content.append(
                {
                    "id": url_id,
                    "url": url,
                    "result": result,
                })
        else:
            content.append(
                {
                    "id": url_id,
                    "url": url,
                    "result": None,
                })

    end = timer()

    return JsonResponse(
            {
                "data": content,
                "time": end - start
            }
    )

@api.get("/v1/tags/{url_id}", response={200: TagsSchema, 403: Error})
async def get_tag(request, url_id: int = Path(...)):
    """
    Get pattern https?://
    :return: JSON with results
    """

    start = timer()
    content = []

    try:
        url = urls[url_id]
        result = await results(url)

        if result:
            content.append(
                {
                    "id": url_id,
                    "url": url,
                    "result": result,
                })
        else:
            content.append(
                {
                    "id": url_id,
                    "url": url,
                    "result": None,
                })

        end = timer()

        return JsonResponse(
                {
                    "data": content,
                    "time": end - start
                }
        )
    except IndexError:
        return JsonResponse(
                {
                    "data": "id must be between 0 and 9",
                }
        )


@api.get("/healthcheck")
async def healthcheck(request):
    """
    Healthcheck endpoint
    :return: JSON with success message
    """
    return  JsonResponse(
            {
                "data": "Ok!",
            }
    )