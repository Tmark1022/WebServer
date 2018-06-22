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
	level = db.Column(db.Integer, default = 0)
	head_id = db.Column(db.Integer)
	
	
	
	
	theme_id = db.Column(db.Integer, db.ForeignKey("theme.theme_id"))			# 外键
	
	def __str__(self):
		return "<table users %s>" % self.user_id
	
	__repr__ = __str__
	
	
class Theme(db.Model):
	__tablename__ = 'theme'
	theme_id = db.Column(db.Integer, primary_key = True)
	theme_name = db.Column(db.String(50), unique = True)
	
	# 反过来的外键关系引用（使用到该主题的用户引用列表）
	users = db.relationship("User", backref='theme')
	
	def __str__(self):
		return "<table theme %s>" % self.theme_id
	
	__repr__ = __str__


