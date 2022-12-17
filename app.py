from flask import Flask,request,render_template, jsonify,Blueprint,url_for,redirect,make_response
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
import apis.mysqlconnect
from apis.attractions import api1
from apis.login import api2,Auth
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
dbconfig = apis.mysqlconnect.dbconfig
mydbpool = apis.mysqlconnect.mydbpool
Api.add_resource(Auth, "/api/user/auth")
######################################################

class Booking(Resource):
	def reserve(self):
		json_data = []
		try:
			mydb = mydbpool.get_connection()
			mycursor = mydb.cursor()
			login_token = self.cookies.get("login_token")
			if login_token == None:
				json_data = {
					"error": True,
					"message": "尚未登入帳號"
				}
			else:
				login_token = jwt.decode(login_token, 'secret', algorithms=['HS256'])
				if (login_token["ok"] == True) and (login_token["id"] != None):			#看有沒有行程
					userid = login_token["id"]
					sql = "SELECT attractionId,date,time,price FROM booking where userid = %s "		
					val = (userid,)
					mycursor.execute(sql,val)
					result = mycursor.fetchone()
					if result == None:
						json_data = {
							"data":None
						}
					else:
						attractionId = result[0]
						date = result[1]
						time = result[2]
						price = result[3]
						sql = "SELECT data.id,data.name,data.address,image_url.images FROM data INNER JOIN image_url ON data.newid = image_url.ID WHERE data.id = %s"
						val = (attractionId,)
						mycursor.execute(sql,val)
						result1 = mycursor.fetchone()
						id = result1[0]
						name = result1[1]
						address = result1[2]
						image = (result1[3].split(","))[0].replace('[',"")
						json_data = {
							"data": {
								"attraction": {
									"id": attractionId,
									"name": name,
									"address": address,
									"image": image
								},
								"date": date,
								"time": time,
								"price": price
							}
						}
				else:
					json_data = {
						"error": True,
						"message": "尚未登入帳號"
					}
		except:
			json_data = {
				"error": True,
				"message": "資料庫連線錯誤，請聯絡客服人員"
			}
		finally:
			mydb.close()
			mycursor.close()
			response = jsonify(json_data)
			return response
	
	def establish(self):
		json_data = []
		try:
			mydb = mydbpool.get_connection()
			mycursor = mydb.cursor()
			req = request.get_json()
			login_token = self.cookies.get("login_token")
			if login_token == None:
				json_data = {
					"error": True,
					"message": "尚未登入帳號"
				}
			else:
				login_token = jwt.decode(login_token, 'secret', algorithms=['HS256'])
				if (login_token["ok"] == True) and (login_token["id"] != None):
					userid = login_token["id"]
					attractionId = int(req["id"])
					time = "moring"
					price = req["price"]
					if price == 2500:
						time = "afternoon"	
					date = req["date"]
					if date == "":
						json_data = {
							"error": True,
							"message": "請選擇出發日期"
						}
					else:												#定義好userid,attractionId,date,time,price，寫入資料表booking
						sql = "INSERT INTO booking (userid,attractionId,date,time,price) VALUES (%s,%s,%s,%s,%s) "
						val = (userid,attractionId,date,time,price)
						mycursor.execute(sql,val)
						mydb.commit()
						json_data = {"ok" : True}
				else:
					json_data = {
						"error": True,
						"message": "尚未登入帳號"
					}

		except:
			json_data = {
				"error": True,
				"message": "資料庫連線錯誤，請聯絡客服人員"
			}
		finally:
			mydb.close()
			mycursor.close()
			response = jsonify(json_data)
			return response

	def delete_est(self):
		json_data = []
		try:
			mydb = mydbpool.get_connection()
			mycursor = mydb.cursor()
			login_token = self.cookies.get("login_token")
			attractionId = self.get_json()["attractionId"]
			if login_token == None:
				json_data = {
					"error": True,
					"message": "尚未登入帳號"
				}
			else:
				login_token = jwt.decode(login_token, 'secret', algorithms=['HS256'])
				if (login_token["ok"] == True) and (login_token["id"] != None):			#刪行程
					try:
						userid = login_token["id"]
						sql = "DELETE FROM booking WHERE userid = %s and attractionId = %s "		
						val = (userid,attractionId)
						mycursor.execute(sql,val)
						mydb.commit()
						json_data = {
							"ok" : True
						}
					except:
						json_data = {
							"error": True,
							"message": "資料庫連線錯誤"
						}
				else:
					json_data = {
						"error": True,
						"message": "尚未登入帳號"
					}
		except:
			json_data = {
				"error": True,
				"message": "資料庫連線錯誤，請聯絡客服人員"
			}
		finally:
			mydb.close()
			mycursor.close()
			response = jsonify(json_data)
			return response
			

@app.route("/api/booking", methods=["GET","POST","DELETE"])
def api_booking():
	if request.method == "GET":
		response = Booking.reserve(request)
	elif request.method == "POST":
		response = Booking.establish(request)
	else:
		response = Booking.delete_est(request)
	return response

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


