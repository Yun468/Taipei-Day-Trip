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
import requests


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





@app.route("/api/orders", methods=["POST"])
def orders():
    json_data = []
    mydb = mydbpool.get_connection()
    mycursor = mydb.cursor()
    try:
        login_token = request.cookies.get("login_token")
        login_token = jwt.decode(login_token, 'secret', algorithms=['HS256'])
        userid = login_token["id"]                                  #使用者ID
        req = request.get_json()
        prime = req["prime"]
        order = req["order"]
        paid = "Not Completed"
        sql = "INSERT INTO orders (userId,price,paid,attractionId,date,time,contactName,contactEmail,contactPhone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val = (userid,order["price"],paid,order["trip"]["attraction"]["id"],order["trip"]["date"],order["trip"]["time"],order["contact"]["name"],order["contact"]["email"],order["contact"]["phone"])
        mycursor.execute(sql,val)
        mydb.commit()
        phone_number = order["contact"]["phone"].lstrip()
        #傳送prime 到tappay
        headers = {"Content-Type":"application/json","x-api-key":"partner_KIcjSTwx3Zs9P70ckr7H1SPhYm5KNCKvR49QPYvX2vNjzL6pIw4Qsewz"}
        data = {
            "prime":prime,
            "partner_key":"partner_KIcjSTwx3Zs9P70ckr7H1SPhYm5KNCKvR49QPYvX2vNjzL6pIw4Qsewz",
            "merchant_id":"Chiayun_ESUN",
            "details":"TDT Test",
            "amount":order["price"],
            "currency":"TWD",
            "cardholder": {
                "phone_number":"+886923456789",                #測試號碼
                "name":order["contact"]["name"],
                "email":order["contact"]["email"],
            },
        }
        res = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', data = data, headers = headers)
        print(res.text)
        json_data = res.text
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


