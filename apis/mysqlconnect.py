from flask import Flask
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
import os
from dotenv import load_dotenv


load_dotenv()
MySQL_URL = os.getenv("MySQL_URL")
MySQL_USER = os.getenv("MySQL_USER")
MySQL_PWD = os.getenv("MySQL_PWD")
MySQL_DATABASE = os.getenv("MySQL_DATABASE")


dbconfig = {
	"host":MySQL_URL,
	"user":MySQL_USER,
	"password":MySQL_PWD,
	"database":MySQL_DATABASE,
	'buffered': True
}
mydbpool = pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
    pool_reset_session = True,
    **dbconfig
) 