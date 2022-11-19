from flask import Flask,request,render_template, jsonify
import mysql.connector
from mysql.connector import pooling
from difflib import *

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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
	attractions=[]
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
			id = (page)*12+1
			count = 12
			if (id +12)> max_id:
				count = (max_id - id)+1
			for x in range(count):
				try:
					sql_1 = "SELECT images FROM image_url where ID = %s"
					val=(id,)
					mycursor.execute(sql_1,val)
					images = mycursor.fetchall()		#images = 陣列，只有一項，項為tuple，tuple 內是str，str內是list
					images = images[0][0]					#images = str
					characters = "]['"
					images = "".join( x for x in images if x not in characters)
					images = images.split(',')			#list /  print(images[0])      #str
					images={"images":images}
				except:
					attractions={
								"error": True,
								"message": "搜尋圖片資料連線錯誤"
								}
				try:
					sql_2 = "SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data WHERE ID = %s"
					val=(id,)
					mycursor.execute(sql_2,val)
					result=mycursor.fetchone()
					row_headers=[x[0] for x in mycursor.description]
					info= dict(zip(row_headers,result))
				except:
					attractions={
								"error": True,
								"message": "搜尋景點資訊錯誤"
								}
				try:
					json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON
					attractions.append(json_data)		#將json_data放入arry
					id =id+1
				except:
					attractions={
								"error": True,
								"message": "程式內部錯誤"
								}
			nextPage = page +1	
			if nextPage >= max_page:
				nextPage = None
		attractions={"naxtPage":nextPage,"data":attractions}

	else:
		sql ="SELECT DISTINCT category FROM data"
		mycursor.execute(sql)
		category = mycursor.fetchall()		
		Classification = False
		for CAT in category:
			if CAT[0] == keyword  :
				Classification = True
		if Classification == True:
			sql ="SELECT ID FROM data where category = %s"
			val=(keyword,)
			mycursor.execute(sql,val)
			res = mycursor.fetchall()		#res = ID資料
			count = len(res)
			if count <= 12 :
				if page != 0:
					attractions={
					"error": True,
					"message": "超過總頁數範圍"
					}
				else:
					for index in range(count):						
						try:
							id = res[index][0]
							sql_1 = "SELECT images FROM image_url where ID = %s"
							val=(id,)
							mycursor.execute(sql_1,val)
							images = mycursor.fetchall()		#images = 陣列，只有一項，項為tuple，tuple 內是str，str內是list
							images = images[0][0]					#images = str
							characters = "]['"
							images = "".join( x for x in images if x not in characters)
							images = images.split(',')			#list /  print(images[0])      #str
							images={"images":images}
						except:
							attractions={
							"error": True,
							"message": "搜尋圖片資料連線錯誤"
							}
						try:
							sql_2 = "SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data WHERE ID = %s"
							val=(id,)
							mycursor.execute(sql_2,val)
							result=mycursor.fetchone()
							row_headers=[x[0] for x in mycursor.description]
							info= dict(zip(row_headers,result))						
						except:
							attractions={
							"error": True,
							"message": "搜尋景點資訊錯誤"
							}
						try:
							json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON	
							attractions.append(json_data)		#將json_data放入arry
						except:
							attractions={
							"error": True,
							"message": "程式內部問題"
							}			
				nextPage = None
			else:
				max_page = (count //12)
				if page <  max_page:
					index = page*12
					for x in range(12):
						try:								
							ID =res[index][0]
							sql_1 ="SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data where ID =%s"
							val_1=(ID,)
							mycursor.execute(sql_1,val_1)
							result = mycursor.fetchone()
							row_headers=[x[0] for x in mycursor.description]
							info= dict(zip(row_headers,result))		
						except:
							attractions={
								"error": True,
								"message": "景點分類搜尋錯誤"
							}
						try:									
							sql_2 ="SELECT images FROM image_url where ID =%s"
							val_2=(ID,)
							mycursor.execute(sql_2,val_2)
							images = mycursor.fetchall()
							images = images[0][0]					#images = str
							characters = "]['"
							images = "".join( x for x in images if x not in characters)
							images = images.split(',')			#list /  print(images[0])      #str
							images={"images":images}
						except:
							attractions={
								"error": True,
								"message": "景點分類圖片搜尋錯誤"
							}
						try:
							index = index+1
							json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON
							attractions.append(json_data)		#將json_data放入arry
						except:
							attractions={
							"error": True,
							"message": "景點分類程式內部錯誤1"
							}
					nextPage = None						
				elif page == max_page:
					index = (page*12)
					for x in range(count%12):
						try:								
							ID =res[index][0]
							sql_1 ="SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data where ID =%s"
							val_1=(ID,)
							mycursor.execute(sql_1,val_1)
							result = mycursor.fetchone()
							row_headers=[x[0] for x in mycursor.description]
							info= dict(zip(row_headers,result))		
						except:
							attractions={
								"error": True,
								"message": "景點分類搜尋錯誤"
							}
						try:									
							sql_2 ="SELECT images FROM image_url where ID =%s"
							val_2=(ID,)
							mycursor.execute(sql_2,val_2)
							images = mycursor.fetchall()
							images = images[0][0]					#images = str
							characters = "]['"
							images = "".join( x for x in images if x not in characters)
							images = images.split(',')			#list /  print(images[0])      #str
							images={"images":images}

						except:
							attractions={
								"error": True,
								"message": "景點分類圖片搜尋錯誤"
							}
						try:
							index = index+1
							json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON
							attractions.append(json_data)		#將json_data放入arry
						except:
							attractions={
							"error": True,
							"message": "景點分類程式內部錯誤1"
							}				
							nextPage = None
				else:
					attractions={
						"error": True,
						"message": "頁數超出最大範圍"
					}
					nextPage = None
				nextPage = page +1	
				if nextPage >= max_page:
					nextPage = None
			attractions={"naxtPage":nextPage,"data":attractions}
		else:
			sql ="SELECT ID FROM data where name LIKE %s"
			val=("%"+keyword+"%",)
			mycursor.execute(sql,val)
			res = mycursor.fetchall()		#res = ID資料
			count = len(res)
			if count <= 12 :
				if page != 0:
					attractions={
					"error": True,
					"message": "超過總頁數範圍"
					}
				else:
					for index in range(count):						
						try:
							id = res[index][0]
							sql_1 = "SELECT images FROM image_url where ID = %s"
							val=(id,)
							mycursor.execute(sql_1,val)
							images = mycursor.fetchall()		#images = 陣列，只有一項，項為tuple，tuple 內是str，str內是list
							images = images[0][0]					#images = str
							characters = "]['"
							images = "".join( x for x in images if x not in characters)
							images = images.split(',')			#list /  print(images[0])      #str
							images={"images":images}
						except:
							attractions={
							"error": True,
							"message": "搜尋圖片資料連線錯誤"
							}
						try:
							sql_2 = "SELECT id,name,category,description,address,transport,mrt,lat,lng FROM data WHERE ID = %s"
							val=(id,)
							mycursor.execute(sql_2,val)
							result=mycursor.fetchone()
							row_headers=[x[0] for x in mycursor.description]
							info= dict(zip(row_headers,result))						
						except:
							attractions={
							"error": True,
							"message": "搜尋景點資訊錯誤"
							}
						try:
							json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON	
							attractions.append(json_data)		#將json_data放入arry
						except:
							attractions={
							"error": True,
							"message": "程式內部問題"
							}			
				nextPage = None
			else:
				max_page = (count //12)
				if page <  max_page:
					index = page*12
					for x in range(12):
						try:								
							ID =res[index][0]
							sql_1 ="SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data where ID =%s"
							val_1=(ID,)
							mycursor.execute(sql_1,val_1)
							result = mycursor.fetchone()
							row_headers=[x[0] for x in mycursor.description]
							info= dict(zip(row_headers,result))		
						except:
							attractions={
								"error": True,
								"message": "景點分類搜尋錯誤"
							}
						try:									
							sql_2 ="SELECT images FROM image_url where ID =%s"
							val_2=(ID,)
							mycursor.execute(sql_2,val_2)
							images = mycursor.fetchall()
							images = images[0][0]					#images = str
							characters = "]['"
							images = "".join( x for x in images if x not in characters)
							images = images.split(',')			#list /  print(images[0])      #str
							images={"images":images}
						except:
							attractions={
								"error": True,
								"message": "景點分類圖片搜尋錯誤"
							}
						try:
							index = index+1
							json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON
							attractions.append(json_data)		#將json_data放入arry
						except:
							attractions={
							"error": True,
							"message": "景點分類程式內部錯誤1"
							}
					nextPage = None						
				elif page == max_page:
					index = (page*12)
					for x in range(count%12):
						try:								
							ID =res[index][0]
							sql_1 ="SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data where ID =%s"
							val_1=(ID,)
							mycursor.execute(sql_1,val_1)
							result = mycursor.fetchone()
							row_headers=[x[0] for x in mycursor.description]
							info= dict(zip(row_headers,result))		
						except:
							attractions={
								"error": True,
								"message": "景點分類搜尋錯誤"
							}
						try:									
							sql_2 ="SELECT images FROM image_url where ID =%s"
							val_2=(ID,)
							mycursor.execute(sql_2,val_2)
							images = mycursor.fetchall()
							images = images[0][0]					#images = str
							characters = "]['"
							images = "".join( x for x in images if x not in characters)
							images = images.split(',')			#list /  print(images[0])      #str
							images={"images":images}

						except:
							attractions={
								"error": True,
								"message": "景點分類圖片搜尋錯誤"
							}
						try:
							index = index+1
							json_data={**info,**images}			#json_data = 所有景點資訊的資訊,JSON
							attractions.append(json_data)		#將json_data放入arry
						except:
							attractions={
							"error": True,
							"message": "景點分類程式內部錯誤1"
							}				
							nextPage = None
				else:
					attractions={
						"error": True,
						"message": "頁數超出最大範圍"
					}
					nextPage = None
				nextPage = page +1	
				if nextPage >= max_page:
					nextPage = None
			attractions={"naxtPage":nextPage,"data":attractions}

	
	mycursor.close()
	mydb.close()
	attractions = jsonify(attractions)
	return 	attractions

@app.route("/api/attraction/<attractionId>")
def apiattractionid(attractionId):
	mydb = mydbpool.get_connection()
	mycursor = mydb.cursor()
	try:
		json_data=[]
		sql = "SELECT _id,name,category,description,address,transport,mrt,lat,lng FROM data WHERE _id = %s"
		val =(attractionId,)
		mycursor.execute(sql,val)
		result = mycursor.fetchone()
		if result == None:
			json_data = {
			"error": True,
			"message": "景點編號不存在"
			}
		else:
			row_headers = [x[0] for x in mycursor.description]
			json_data.append(dict(zip(row_headers,result)))
			json_data = {"data" : json_data}
	except:
		json_data = {
		"error": True,
		"message": "景點編號搜尋伺服器內部錯誤"
		}
	json_data = jsonify(json_data)
	mycursor.close()
	mydb.close()
	return json_data

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
	return render_template("attraction.html",id=id)
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")





app.run(port=3000,host=0.0.0.0,debug=True)