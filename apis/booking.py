from flask import Flask,request,render_template, jsonify,Blueprint,url_for,redirect,make_response
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
import apis.mysqlconnect
from flask_restful import Api, Resource


api3 = Blueprint('api3',__name__,)
dbconfig = apis.mysqlconnect.dbconfig
mydbpool = apis.mysqlconnect.mydbpool




class  Travel(Resource):
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
					else:
						sql = "SELECT attractionId,date,time,price FROM booking where userid = %s "		
						val = (userid,)
						mycursor.execute(sql,val)
						result = mycursor.fetchone()
						if result == None:
							sql = "INSERT INTO booking (userid,attractionId,date,time,price) VALUES (%s,%s,%s,%s,%s) "
							val = (userid,attractionId,date,time,price)
							mycursor.execute(sql,val)
							mydb.commit()
							json_data = {"ok" : True}
						else:
							sql = "UPDATE booking SET attractionId =%s,date =%s,time =%s,price =%s "
							val = (attractionId,date,time,price)
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
			

@api3.route("/api/booking", methods=["GET","POST","DELETE"])
def api_booking():
	if request.method == "GET":
		response =  Travel.reserve(request)
	elif request.method == "POST":
		response =  Travel.establish(request)
	else:
		response =  Travel.delete_est(request)
	return response
