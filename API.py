from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Model import prepareAndPredict
from urllib.parse import urlparse

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def checkIsUrl(url):
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

class UrlItem(BaseModel):
    url_value: str

@app.post("/scan")
async def checkUrl(url: UrlItem):
    if not checkIsUrl(url.url_value):
        raise HTTPException(status_code=400, detail="There is no URL to scan!")

    url_copy = url.url_value
    url_copy = url_copy.replace('www.', '')

    prediction_result = prepareAndPredict(url_copy)
    prediction_means = {
        0: "Safe",
        1: "Phishing",
        2: "Malware",
    }

    return { "checkedUrl": url.url_value, "result": prediction_means[prediction_result] }