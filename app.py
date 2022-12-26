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
        serial_number = int(str(int(time.time())) +str(userid) + str(order["trip"]["attraction"]["id"]))
        sql = "INSERT INTO orders (userId,serial_number,price,paid,attractionId,date,time,contactName,contactEmail,contactPhone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        val = (userid,serial_number,order["price"],paid,order["trip"]["attraction"]["id"],order["trip"]["date"],order["trip"]["time"],order["contact"]["name"],order["contact"]["email"],order["contact"]["phone"])
        mycursor.execute(sql,val)
        mydb.commit()

        #傳送prime 到tappay
        phone_number = "+886"+(order["contact"]["phone"].lstrip())
        headers = {"Content-Type":"application/json","x-api-key":"partner_KIcjSTwx3Zs9P70ckr7H1SPhYm5KNCKvR49QPYvX2vNjzL6pIw4Qsewz"}
        data = {
            "prime":prime,
            "partner_key":"partner_KIcjSTwx3Zs9P70ckr7H1SPhYm5KNCKvR49QPYvX2vNjzL6pIw4Qsewz",
            "merchant_id":"Chiayun_ESUN",
            "details":"TDT Test",
            "amount":int(order["price"]),
            "cardholder": {
                "phone_number":phone_number,
                "name":order["contact"]["name"],
                "email":order["contact"]["email"],
            },
            "remember": True
        }
        res = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', json = data, headers = headers)
        res = res.json()

        #付款是否成功
        if res["status"] == 0:
            sql = "UPDATE orders SET paid = %s WHERE serial_number = %s"
            val = ("Completed",serial_number)
            mycursor.execute(sql,val)
            mydb.commit()
            # 訂單編號
            json_data = {
                "data": {
                    "number": serial_number,
                    "payment": {
                        "status": 0,
                        "message": "付款成功"
                    }
                }
            }
        else:
            msg = res["msg"]
            json_data = {
                "number" :serial_number,
                "error": True,
                "msg":msg
            }
    except:
        json_data = {
            "error": True,
            "message": "資料庫連線錯誤，請聯絡客服人員"
        }
    finally:
        #刪除booking 中已成功訂購的訂單
        sql = "DELETE FROM booking WHERE userid = %s "          #因為設計是一個userID 在booking 裡面只會有一份預定行程，故未來若想改成多個預定行程，需改動booking資料表欄位及此處的刪除方式(因未來可能改動，特此紀錄)
        val = (userid,)
        mycursor.execute(sql,val)
        mydb.commit()
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


