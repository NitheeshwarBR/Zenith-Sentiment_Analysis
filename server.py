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
import re

def ind(url):
    list1 = [r"www.threads.net", r"www.facebook.com", r"www.youtube.com", r"www.amazon.in"]
    option=1
    for domain in list1:
        result = re.search(domain, url)
        if result:
            option=list1.index(domain)
    if option == 0:
       return importlib.import_module("threads")
    elif option == 1:
        return importlib.import_module("facebook")
    elif option == 2:
        return importlib.import_module("youtube")
    elif option==3:
        return importlib.import_module("amazon")
    


analytics=[]
app=FastAPI()

class Data(BaseModel):
    link: str | None=None
    data: list | None=None

@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse('temporary.html',{"request":request,"id":1,})


@app.post("/output")
async def processed_data(data: Data):
    if data is None or (data.link is None and data.data is None):
        return JSONResponse(content={"error_message": "Pass the required values"}, status_code=400)
    if(data.link==None):
        response=data.data
    else:   
        mod=ind(data.link)
        print(mod.__name__)
        response=await mod.Comments(data.link,"uat")
    max_res={0:0,1:0,2:0}
    for i in response[0:10]:
        sentiments=sentiment_analysis(i)
        max_res[sentiments.index(max(sentiments))]+=1
        print(sentiments)

    return JSONResponse(content={"negative":max_res[0],"neutral":max_res[1],"positive":max_res[2]}, status_code=200)