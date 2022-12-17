from flask import Flask
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS

MySQL_URL = "testdb.ap-northeast-1.rds.amazonaws.com"
MySQL_USER = "admin"
MySQL_PWD = "admin"
MySQL_DATABASE = "test_db"

dbconfig = {
	"host":MySQL_URL,
	"user":MySQL_USER,
	"password":MySQL_PWD ,
	"database":MySQL_DATABASE
}
mydbpool = pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
    pool_reset_session = True,
    **dbconfig
) 