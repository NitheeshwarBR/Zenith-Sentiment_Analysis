from fastapi import FastAPI,Request,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import importlib
from sentiment_analyzer import sentiment_analysis
from fastapi.templating import Jinja2Templates
from starlette.middleware.trustedhost import TrustedHostMiddleware
from typing import List, Dict, Union
app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
templates = Jinja2Templates(directory="templates")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# Serve static files from the "static" directory

mod=importlib.import_module("facebook")
analytics=[]
app=FastAPI()

class Data(BaseModel):
    link: str | None=None
    data: list | None=None

@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse('temporary.html',{"request":request})


@app.post("/output")
async def processed_data(data: Data):
    if data is None or (data.link is None and data.data is None):
        return JSONResponse(content={"error_message": "Pass the required values"}, status_code=400)
    
    if data.link is not None:
        # Use data.link for processing
        response = await mod.facebookComments(data.link, "uat")
    for i in response:
        sentiments = sentiment_analysis(i)
        analytics.append({"comments": i, "negative": sentiments[0], "neutral": sentiments[1], "positive": sentiments[2]})
        print(analytics)
    return {"results": analytics}