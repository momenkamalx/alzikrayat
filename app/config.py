import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",      
        user="root",           
        password="",           
        db="alzikrayat",       
        cursorclass=pymysql.cursors.DictCursor  
    )