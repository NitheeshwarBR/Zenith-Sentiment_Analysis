from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import importlib
from sentiment_analyzer import sentiment_analysis

mod=importlib.import_module("threads")
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
        response=await mod.Comments(data.link,"uat")
    max_res={0:0,1:0,2:0}
    for i in response[0:10]:
        sentiments=sentiment_analysis(i)
        max_res[sentiments.index(max(sentiments))]+=1
        print(sentiments)

    return JSONResponse(content={"negative":max_res[0],"neutral":max_res[1],"positive":max_res[2]}, status_code=200)