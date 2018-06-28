#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-21
# module	: App.DBMgr
#===================================================
from App import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


#====================================================
# 数据库表定义
#====================================================
class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(128), nullable = False)
	password_hash = db.Column(db.String(128), nullable = False)
	user_name = db.Column(db.String(32), nullable = False)
	
	@property
	def password(self):
		raise AttributeError("password is not a readable attribute")
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __str__(self):
		return "<table users %s>" % self.user_id
	
	
	# flask_login 要求的四个函数（或者直接继承UserMixin, 但是这样用户id命名只能是id, 不能死user_id等其他名字）
	@property
	def is_active(self):
		return True

	@property
	def is_authenticated(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.user_id)
	
	__repr__ = __str__

# flask_login 当前登录用户current_user加载回调函数, 如果用户没有登录（session传递过来的user_id并不能登录， 就会使用AnonymousUserMixin实例， 这个实例是没有登录的）
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))
