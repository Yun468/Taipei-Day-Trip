import mysql.connector
import json

mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password="",
    database="week09",
) 

#讀取JSON檔案
with open ("taipei-attractions.json",mode="r", encoding = "utf-8") as attractions:
    attractions = json.load(attractions)              
    #attractions = json資料  → {'result': {'limit': 1000, 'offset': 0, 'count': 58, 'sort': '', 'results': [**旅遊景點資料**]}

datas = attractions["result"]["results"]
#整理景點圖片的url, 最終result = 陣列，所有景點的圖檔url集合，第一項代表第一個景點(共58項)，每一項裡面還有有許多小項代表幾張圖檔
results=[]

for index in datas:
    urls = index["file"].split("https://")           #每一筆 urls 都會成為一個陣列(代表一個景點)，每個陣列的「第一項」都是 ""，且每項都沒有 「https://」在前面
    del urls[0]                                       #刪除每個list 的第一項
    _file=[]
    for url in urls:
        if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".PNG") or url.endswith(".JPG"):     
            url = "https://"+url
            _file.append(url)
    results.append(_file)


#將attractions 分類成兩份table 儲存管理：data,image
cur = mydb.cursor()

#image 資料表：存放圖檔urls
id = 1
for images in results:
    sql = "INSERT INTO image_url (ID,images) VALUES (%s,%s)"
    
    val = (id,str(images))
    cur.execute(sql,val)
    mydb.commit()
    id = id + 1


#data資料表： 存放景點資料(除了圖片)
for data in datas:
    _id = data["_id"]
    rate = data["rate"]
    transport = data["direction"]
    name = data["name"]
    date = data["date"]
    lng = data["longitude"]
    REF_WP = data["REF_WP"]
    avBegin = data["avBegin"]
    langinfo = data["langinfo"]
    mrt = data["MRT"]
    SERIAL_NO = data["SERIAL_NO"]
    RowNumber = data["RowNumber"]
    category = data["CAT"]
    MEMO_TIME = data["MEMO_TIME"]
    POI = data["POI"]
    idpt = data["idpt"]
    lat = data["latitude"]
    description = data["description"]
    avEnd = data["avEnd"]
    address = data["address"].replace(" ","")
    
    sql = "INSERT INTO data (id,rate,transport,name,date,lng,REF_WP,avBegin,langinfo,mrt,SERIAL_NO,RowNumber,category,MEMO_TIME,POI,idpt,lat,description,avEnd,address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (_id,rate,transport,name,date,lng,REF_WP,avBegin,langinfo,mrt,SERIAL_NO,RowNumber,category,MEMO_TIME,POI,idpt,lat,description,avEnd,address,)
    cur.execute(sql,val)
    mydb.commit()


mydb.close()

