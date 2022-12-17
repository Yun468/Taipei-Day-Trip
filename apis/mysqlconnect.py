from flask import Flask
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
dbconfig = {
	"host":"localhost",
	"user":"root",
	"password":"123456",
	"database":"week"
}
mydbpool = pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
    pool_reset_session = True,
    **dbconfig
) 