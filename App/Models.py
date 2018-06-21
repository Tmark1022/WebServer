#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-21
# module	: App.DBMgr
#===================================================
from App import db


#====================================================
# 数据库表定义
#====================================================
class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key = True)
	user_password = db.Column(db.String(50), nullable = False)
	user_name = db.Column(db.String(50), unique = True)
