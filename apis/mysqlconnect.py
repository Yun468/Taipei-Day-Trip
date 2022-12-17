from flask import Flask
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS

MySQL_URL =""
MySQL_USER =""
MySQL_PWD =""
MySQL_DATABASE =""

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