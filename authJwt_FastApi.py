from fastapi import FastAPI,Depends,Request
import jwt
from datetime import datetime,timedelta
import uvicorn
from pydantic import BaseModel

app=FastAPI()
secret="key"
class Person(BaseModel):
    name:str

@app.post("/token")
def fn(req:Request,person:Person):
    name=person.name
    token=jwt.encode(
        {"id":name , "exp":datetime.now().utcnow()+timedelta(minutes=15)}
        ,secret)
    return token

def check(req:Request):
    try:
        token=req.headers["Authorization"].split(" ")[1]
        jwt.decode(token,secret,algorithms=["HS256"])
    except Exception as e:
        print (e)
        raise Exception(e)
    return True

@app.get("/")
def fn2(verify:bool=Depends(check)):
    return "Working"

if(__name__=="__main__"):
    uvicorn.run("test:app",host="0.0.0.0",port=5000)