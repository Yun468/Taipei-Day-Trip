from flask import Flask,request,render_template, jsonify,Blueprint,url_for,redirect,make_response
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
import apis.mysqlconnect
from apis.attractions import api1
from apis.login import api2,Auth
from apis.booking import api3,Travel
from flask_restful import Api, Resource
import jwt
import time


app = Flask(__name__,
			static_folder='static')
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
CORS(app)
app.secret_key="any string but secret"
Api = Api(app)

app.register_blueprint(api1)
app.register_blueprint(api2)
app.register_blueprint(api3)
dbconfig = apis.mysqlconnect.dbconfig
mydbpool = apis.mysqlconnect.mydbpool
Api.add_resource(Auth, "/api/user/auth")
Api.add_resource(Travel, "/api/booking/Travel")
######################################################


################################################

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")



if __name__ == "__main__":
	app.run(port=3000,host="0.0.0.0",debug=True)


