"""
Basic Authentication 
1. Cannot Logout
2. Credential stored in Cache
3. Will expire once browser is closed 
4. from flask_httpauth import HttpBasicAuth


Token
1. Stored as Cookies
2   App send usn/pass
    API check credentials in DB
        If a user is found, it generates a token 
        Send token 
    App uses token from now
3. Types : Bearer (life  >15 mins ) , JWT (life < 15 mins )
    basic - Easy to hack
    Bearer -
        1. life  >15 mins
        2. stored in DB and verified each time
        3. Hard to hack
    JWT  - 
        1. Life is 15 mins
        2. Carries all info
        3. Once issued hard to invalide
        4. Hard to Hack 


document.cookie
document.cookie = 'csrftoken='
"""
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Person.sqlite3"
app.config["JWT_SECRET_KEY"] = "key"  # Change this "super secret" with something else!
jwt = JWTManager(app)

db=SQLAlchemy(app)
class Person(db.Model):
    id = db.Column( db.Integer, primary_key = True)
    name:str=db.Column(db.String,)
    password:str=db.Column(db.String)
    def __init__(self,name,password) -> None:
        self.name=name
        self.password=password
        

@app.route("/token", methods=["POST"])
def create_token():
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    
    user = Person.query.filter_by(name=name, password=password).first()
    if user is None:
        person=Person(name,password)
        db.session.add(person)
        db.session.commit()
        user = Person.query.filter_by(name=name, password=password).first()

        # return (jsonify({"err": "user no exist"}), 401)
    print(Person.query.all())    
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": name })


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    # user = Person.query.get(current_user_id)
    return jsonify({"id": current_user_id }), 200

if (__name__ =="__main__"):
    app.app_context().push()
    db.create_all()
    app.run(host="0.0.0.0", port =5000 , debug=True)