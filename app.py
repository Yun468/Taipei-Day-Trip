from flask import Flask,request,render_template, jsonify,Blueprint,url_for,redirect,make_response
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
import apis.mysqlconnect
from apis.attractions import api1
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
dbconfig = apis.mysqlconnect.dbconfig
mydbpool = apis.mysqlconnect.mydbpool
######################################################

@app.route("/api/user", methods=["POST"])
def user():
	mydb = mydbpool.get_connection()
	mycursor = mydb.cursor()
	req = request.get_json()
	name = req["name"]
	email = req["email"]
	password = req["password"]
	json_data = {}
	try:
		sql = "SELECT email FROM userdata where email = %s"
		val = (email,)
		mycursor.execute(sql,val)
		result = mycursor.fetchone()
		if result == None:
			sql = "INSERT INTO userdata (name,email,password) VALUES (%s,%s,%s)"
			val = (name,email,password)
			mycursor.execute(sql,val)
			mydb.commit()
			json_data = {
				"ok": True
			}
		else:
			json_data = {
				"error": True,
				"message": "此信箱已被註冊"
			}
	except:
		json_data = {
			"error": True,
			"message": "資料庫連線錯誤"
		}
	mycursor.close()
	mydb.close()
	response = jsonify(json_data)
	return response

class Auth(Resource):
	def login(self):
		mydb = mydbpool.get_connection()
		mycursor = mydb.cursor()
		req = self.get_json()
		email = req["email"]
		password = req["password"]
		login_token = None
		try:
			sql = "SELECT id,name,email,password FROM userdata where email = %s"
			val = (email,)
			mycursor.execute(sql,val)
			result = mycursor.fetchone()
			if result == None:
				json_data = {
					"error": True,
					"message": "此信箱尚未註冊"
				}
			else:
				if password == result[3]:
					json_data = {
						"ok": True
					}
					now = time.time()				#單位：秒
					expiretime = now + (7*86400)
					payload = {
						"ok":True,
						"id":result[0],
						"exp":expiretime
					}
					login_token = jwt.encode(
						payload = payload, 
						key = "secret", 
						algorithm="HS256"
					)
				else:
					json_data = {
						"error": True,
						"message": "密碼錯誤"
					}
		except:
			json_data = {
				"error": True,
				"message": "資料庫連線錯誤"
			}
		finally:
			mycursor.close()
			mydb.close()
			if login_token != None:
				json_data = jsonify(json_data)
				response = make_response(json_data)
				response.set_cookie("login_token",login_token)
			else:
				response = jsonify(json_data)
			return response

	def get_current_userdata(self):
		try:
			mydb = mydbpool.get_connection()
			mycursor = mydb.cursor()
			login_token = self.cookies.get("login_token")
			login_token = jwt.decode(login_token, 'secret', algorithms=['HS256'])
			if (login_token["ok"] == True) and (login_token["id"] != None):
				try:
					id = login_token["id"]
					sql = "SELECT id,name,email FROM userdata where id = %s"
					val = (id,)
					mycursor.execute(sql,val)
					result = mycursor.fetchone()
					if result == None:
						json_data = None
					else:
						now = time.time()				#單位：秒
						expiretime = now + (7*86400)
						payload = {
							"ok":True,
							"id":result[0],
							"exp":expiretime
						}
						login_token = jwt.encode(
							payload = payload, 
							key = "secret", 
							algorithm="HS256"
						)
						json_data = {
										"data": {
											"id": result[0],
											"name": result[1],
											"email": result[2]
										}
									}
				except:
					json_data = {
						"error": True,
						"message": "伺服器連線錯誤"
					}			
			else:
				json_data = None
		except:
			json_data = None
		finally:
			mycursor.close()
			mydb.close()
			if login_token != None:
				json_data = jsonify(json_data)
				response = make_response(json_data)
				response.set_cookie("login_token",login_token)
			else:
				response = jsonify(json_data)
			return response

	def logout(self):
		try:
			json_data = {"ok" : True}
			json_data = jsonify(json_data)
			response = make_response(json_data)
			response.set_cookie("login_token","",expires=0)
		except:
			json_data = {
				"error": True,
				"message": "伺服器連線錯誤"
			}
			json_data = jsonify(json_data)	
		finally:
			return response

@app.route("/api/user/auth", methods=["GET","PUT","DELETE"])
def user_auth():
	if request.method == "GET":
		response = Auth.get_current_userdata(request)
	elif request.method == "PUT":
		response = Auth.login(request)
	else:
		response = Auth.logout(request)
	return response
Api.add_resource(Auth, "/api/user/auth")

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


