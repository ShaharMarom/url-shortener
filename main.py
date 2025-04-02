from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from url_manger import URLManger
import re

def is_valid_url(url: str) -> bool:
    url_pattern = re.compile(
        r'^(https?|ftp)://'
        r'(([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,6}))' 
        r'(:\d+)?'
        r'(\/\S*)?$'
    )
    return re.match(url_pattern, url) is not None


class RequestUrl(BaseModel):
    url: str

app = FastAPI()
url_manger = URLManger()

BASE_URL = "http://localhost:8000/shorten"

@app.post("/shorten")
async def generate(req_url: RequestUrl, response: Response):
    if not is_valid_url(req_url.url):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "Invalid URL as a parameter"

    short_url = url_manger.generate_short_url(url=req_url.url)

    return  BASE_URL + "/" + short_url

@app.get("/shorten/{shorten_url}")
async def long_url(shorten_url: str, response: Response):
    res = url_manger.get_url(shorten_url)
    if res is not None:
        return res
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "URL doesn't exists"



# TODO - add validation function for url
# TODO - UNIT TEST
# TODO - caching mechanism