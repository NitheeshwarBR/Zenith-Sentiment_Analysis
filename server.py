from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import importlib
from sentiment_analyzer import sentiment_analysis

mod=importlib.import_module("facebook")
analytics=[]
app=FastAPI()

class Data(BaseModel):
    link: str | None=None
    data: list | None=None


@app.post("/")
async def root(data: Data=None):
    if data is None:
        return JSONResponse(content={"error_message": "Pass the required values"}, status_code=400)
    if(data.link==None):
        response=data.data
    else:   
        response=await mod.facebookComments(data.link,"uat")
    for i in response:
        sentiments=sentiment_analysis(i)
        analytics.append({"comments":i,"negative":sentiments[0],"neutral":sentiments[1],"positive":sentiments[2]})
    return JSONResponse(content=analytics, status_code=200)