from flask import Flask,request,json,jsonify,redirect,render_template
import jwt  #pip3 install pyjwt
from datetime import datetime,timedelta

app=Flask(__name__)
SECRET="key"
@app.route("/",methods=["POST"])
def fn():
    if(request.method=="POST"):
        name=request.json["name"]
        resp_data={"id":name,"exp":datetime.utcnow()+timedelta(minutes=15)}
        token=jwt.encode(resp_data,SECRET)
        return jsonify(token,200)
    
def deco(f):
    def wrapper(*args,**kwargs):
        try:
            token=request.headers["Authorization"].split(" ")[1]
            name=jwt.decode(token,SECRET,algorithms=["HS256"])
            return f()
        except Exception as e:
            print(e)
            return jsonify({"error": "Token is missing!"}), 401
    return wrapper

@app.route("/protected",methods=["GET"])
@deco
def fn2():
    return jsonify({"message":"Working"})

if(__name__=="__main__"):
    app.run(host="0.0.0.0",port =5000,debug=True)