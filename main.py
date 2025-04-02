from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from url_manger import URLManger

class RequestUrl(BaseModel):
    url: str

app = FastAPI()
url_manger = URLManger()


BASE_URL = "http://localhost:8000/shorten"

@app.post("/shorten")
async def generate(req_url: RequestUrl):
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