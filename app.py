from flask import Flask,request,render_template, jsonify
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask import *
from flask_cors import CORS

app = Flask(__name__,
			static_folder='static')
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
CORS(app)
app.secret_key="any string but secret"

dbconfig = {
	"host":"localhost",
	"user":"root",
	"password":"",
	"database":"week09"
}
mydbpool = pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
    pool_reset_session = True,
    **dbconfig
) 


@app.route("/api/attractions")
def apiattraction():
	mydb = mydbpool.get_connection()		# Get connection_object from a pool :mydb
	mycursor = mydb.cursor()
	page = request.args.get("page",0,type=int)
	keyword = request.args.get("keyword",type=str)
	info = []
	if keyword =="" or keyword== None:		
		sql = "SELECT COUNT(*) FROM data"
		mycursor.execute(sql)
		max_id = (mycursor.fetchone())[0]
		max_page = max_id //12
		if page > max_page:
			attractions={
				"error": True,
				"message": "頁數超出最大範圍"
			}
			nextPage = None
		else:
			try:
				star = (page*12)
				sql_2 = sql = "SELECT data.id,data.name,data.category,data.description,data.address,data.transport,data.mrt,data.lat,data.lng,image_url.images FROM data INNER JOIN image_url ON data.newid = image_url.ID LIMIT %s,12"
				val=(star,)
				mycursor.execute(sql_2,val)
				result=mycursor.fetchall()
				result = list(result)
				new_result = []
				for index in result:
					index = list(index)
					index[-1] = eval(index[-1])
					new_result.append(index)				
				row_headers=[x[0] for x in mycursor.description]
				for x in new_result:
					info.append(dict(zip(row_headers,x)))
			except:
				attractions={
							"error": True,
							"message": "搜尋景點資訊錯誤"
							}
			nextPage = page +1	
			if nextPage > max_page:
				nextPage = None
		attractions={"nextPage":nextPage,"data":info}

	else:
		sql ="SELECT DISTINCT category FROM data"
		mycursor.execute(sql)
		category = mycursor.fetchall()
		Classification = False
		info = []
		for CAT in category:
			if CAT[0] == keyword :
				Classification = True
				break
		if Classification == True:
			sql = "SELECT COUNT(*) FROM data WHERE category = %s"
			val =(keyword,)
			mycursor.execute(sql,val)
			count = mycursor.fetchone()[0]
			max_page = count //12
			if page > max_page:
				attractions={
					"error": True,
					"message": "頁數超出最大範圍"
				}
				nextPage = None
			else:
				try:
					star = (page*12)
					sql_2 = sql = "SELECT data.id,data.name,data.category,data.description,data.address,data.transport,data.mrt,data.lat,data.lng,image_url.images FROM data INNER JOIN image_url ON data.newid = image_url.ID WHERE category = %s LIMIT %s,12"
					val=(keyword,star)
					mycursor.execute(sql_2,val)
					result=mycursor.fetchall()
					result = list(result)
					new_result = []
					for index in result:
						index = list(index)
						index[-1] = eval(index[-1])
						new_result.append(index)				
					row_headers=[x[0] for x in mycursor.description]
					for x in new_result:
						info.append(dict(zip(row_headers,x)))
				except:
					attractions={
								"error": True,
								"message": "搜尋景點資訊錯誤"
								}
				nextPage = page +1	
				if nextPage > max_page:
					nextPage = None
			attractions={"nextPage":nextPage,"data":info}
		else:
			sql ="SELECT COUNT(*) FROM data where name LIKE %s"
			val=("%"+keyword+"%",)
			mycursor.execute(sql,val)
			count = mycursor.fetchone()[0]
			max_page = count/12
			if page > max_page:
				attractions={
					"error": True,
					"message": "頁數超出最大範圍"
				}
				nextPage = None
			else:
				try:
					star = (page*12)
					sql =  "SELECT data.id,data.name,data.category,data.description,data.address,data.transport,data.mrt,data.lat,data.lng,image_url.images FROM data INNER JOIN image_url ON data.newid = image_url.ID  where data.name LIKE %s limit %s,12;"
					val=("%"+keyword+"%",star)
					mycursor.execute(sql,val)
					result=mycursor.fetchall()
					result = list(result)
					new_result = []
					for index in result:
						index = list(index)
						index[-1] = eval(index[-1])
						new_result.append(index)				
					row_headers=[x[0] for x in mycursor.description]
					for x in new_result:
						info.append(dict(zip(row_headers,x)))
				except:
					attractions={
								"error": True,
								"message": "搜尋景點資訊錯誤"
								}
				nextPage = page +1	
				if nextPage > max_page:
					nextPage = None
			attractions={"nextPage":nextPage,"data":info}

	
	mycursor.close()
	mydb.close()
	attractions = jsonify(attractions)
	return 	attractions

@app.route("/api/attraction/<attractionId>")
def apiattractionid(attractionId):
	mydb = mydbpool.get_connection()
	mycursor = mydb.cursor()
	json_data = {}
	try:
		sql = "SELECT data.id,data.name,data.category,data.description,data.address,data.transport,data.mrt,data.lat,data.lng,image_url.images FROM data INNER JOIN image_url ON data.newid = image_url.ID WHERE data.id = %s"
		val =(attractionId,)
		mycursor.execute(sql,val)
		result = mycursor.fetchone()
		if result == None:
			json_data = {
			"error": True,
			"message": "景點編號不存在"
			}
		else:
			result = list(result)
			result[-1] = eval(result[-1])
			row_headers = [x[0] for x in mycursor.description]
			json_data = dict(zip(row_headers,result))
			json_data = {"data" : json_data}
	except:
		json_data = {
		"error": True,
		"message": "景點編號搜尋伺服器內部錯誤"
		}
	attraction = jsonify(json_data)
	mycursor.close()
	mydb.close()
	return attraction

@app.route("/api/categories")
def categories():
	mydb = mydbpool.get_connection()		# Get connection_object from a pool :mydb
	mycursor = mydb.cursor()
	sql ="SELECT DISTINCT category FROM data"
	mycursor.execute(sql)
	category = mycursor.fetchall()
	categories=[]
	for x in range(len(category)):	
		index = category[x][0]
		categories.append(index)
	mycursor.close()
	mydb.close()
	categories = {"data":categories}
	categories = jsonify(categories)
	return categories

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




app.run(port=3000,host="0.0.0.0")

