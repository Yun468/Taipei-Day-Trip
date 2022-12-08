from flask import Flask,request,render_template, jsonify,Blueprint
import mysql.connector
from mysql.connector import pooling
from difflib import *
from flask_cors import CORS
 
api1 = Blueprint('api1',__name__,)

dbconfig = {
	"host":"localhost",
	"user":"",
	"password":"",
	"database":"week"
}
mydbpool = pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
    pool_reset_session = True,
    **dbconfig
) 