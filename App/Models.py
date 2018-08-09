#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-21
# module	: App.Models
#===================================================
from App import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash				# 创建散列值和检测散列值函数
from itsdangerous import TimedJSONWebSignatureSerializer								# 生成具有过期时间的签名
from flask import current_app
from flask_login.mixins import AnonymousUserMixin
from datetime import datetime
from markdown import markdown
import bleach

#====================================================
# 数据库表定义
#====================================================
# 关注者关联表
class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	
	def __str__(self):
		return "<table Follow %s>" % (self.follower_id)
	
	__repr__ = __str__

class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(128), nullable = False)
	password_hash = db.Column(db.String(128), nullable = False)
	user_name = db.Column(db.String(32), nullable = False, unique = True)
	confirmed = db.Column(db.Boolean, default = False)
	role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"))			# 外键引用
	
	# 额外个人信息
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	register_time = db.Column(db.DateTime(), default = datetime.utcnow)
	last_login_time = db.Column(db.DateTime(), default = datetime.utcnow)
	header_picutre = db.Column(db.String(128))
	
	# 博客文章
	posts = db.relationship("Post", backref = "author", lazy = "dynamic")
	
	# 关注者(设置lazy=joined是有讲究的， 可以减少反向引用的数据库查询操作)
	followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')		# 我关注的用户
	followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')		# 关注我的用户
	
	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		
		if self.role is None:
			# 还没关联起来
			if self.email == current_app.config["FLASK_ADMIN_USER"]:
				self.role = Role.query.filter_by(permissions = 0xff).first()
			if self.role is None:
				# 普通用户或者数据库中并没有管理员的定义， 那么便设置为默认用户
				self.role = Role.query.filter_by(default = True).first()
	
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
	
	def generate_confirmation_token(self, expiration = 3600):
		'''
		生成具有过期时间的令牌
		@param expiration:
		'''
		serializer = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"], expiration)
		return serializer.dumps({"confirm" : self.user_id})				# 如果user_id自动生成， 那么必须先提交了数据库后才能用这个函数
	
	def confirm(self, token):
		'''
		注册验证
		@param token:
		'''
		serializer = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
		try:
			data = serializer.loads(token)
		except:
			return False
		if data.get("confirm") != self.user_id:
			return False
		self.confirmed = True
		db.session.add(self)					# 插入会话， 跟随请求结束保存进数据库
		return True
	
	def ping(self):
		'''
		刷新用户访问时间
		'''
		self.last_login_time = datetime.utcnow()
		db.session.add(self)
	
	@staticmethod
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py
		
		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),
					user_name=forgery_py.internet.user_name(True),
					password=forgery_py.lorem_ipsum.word(),
					confirmed=True,
					location=forgery_py.address.city(),
					about_me=forgery_py.lorem_ipsum.sentence(),
					last_login_time=forgery_py.date.date(True))
			db.session.add(u)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()
	
	#====================================================
	# 角色权限验证函数(为了保证current_user不需要确保已经登录的前提下就可以使用权限验证函数， 请为匿名用户类也添加一下方法)
	#====================================================
	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions)
	
	def is_administrator(self):
		return self.can(Permission.ADMINISTER)
	
	#====================================================
	# 用户关注操作
	#====================================================
	def follow(self, user):
		'''
		关注操作
		@param user:
		'''
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)

	def unfollow(self, user):
		'''
		取消关注操作
		@param user:
		'''
		f = self.followed.filter_by(followed_id=user.user_id).first()
		if f:
			db.session.delete(f)
	
	def is_following(self, user):
		'''
		是否关注了某个用户
		@param user:
		'''
		return self.followed.filter_by(followed_id=user.user_id).first() is not None

	def is_followed_by(self, user):
		'''
		是否被某个用户关注
		@param user:
		'''
		return self.followers.filter_by(follower_id=user.user_id).first() is not None
	
	@property
	def followed_posts(self):
		'''
		获取关注的用户的文章
		'''
		return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(Follow.follower_id == self.user_id)
	
	
class Role(db.Model):
	__tablename__ = 'roles'
	role_id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	default = db.Column(db.Boolean, default = False, index = True)
	permissions = db.Column(db.Integer, nullable = False)
	users = db.relationship("User", backref = "role", lazy = "dynamic")

	def __str__(self):
		return "<table roles %s %s>" % (self.role_id, self.name)
	
	__repr__ = __str__

	@staticmethod
	def manage_roles():
		'''
		管理角色权限，可在这里修改每种角色的权限， 同时更新到数据库使系统生效
		'''
		role_permissions_dict = {
								"User" : (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
								"Moderatoe" : (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS, False),
								'Administrator': (0xff, False)
								}
		
		for role_name in role_permissions_dict.iterkeys():
			role = Role.query.filter_by(name = role_name).first()
			if not role:
				role = Role(name = role_name)
			role.permissions = role_permissions_dict[role_name][0]
			role.default = role_permissions_dict[role_name][1]
			db.session.add(role)
		db.session.commit()

# 文章模型
class Post(db.Model):
	__tablename__ = 'posts'
	post_id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	body_html = db.Column(db.Text)				# 富文本内容缓存
	
	def __str__(self):
		return "<table posts %s>" % (self.post_id)
	
	__repr__ = __str__
	
	@staticmethod
	def generate_fake(count=100):
		from random import seed, randint
		import forgery_py
		seed()
		user_count = User.query.count()
		for i in range(count):
			u = User.query.offset(randint(0, user_count - 1)).first()
			p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
					timestamp=forgery_py.date.date(True),
					author=u)
		db.session.add(p)
		db.session.commit()
	
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
					'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
					'h1', 'h2', 'h3', 'p', 'img']
		allowed_attributes = {
						'a': ['href', 'title'],
						'abbr': ['title'],
						'acronym': ['title'],
						'img':['src', 'alt']
						}
		clean_html = bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, attributes= allowed_attributes)
		target.body_html = bleach.linkify(clean_html)

# 注册数据库相应函数(post.body内容被设置的时候触发)
db.event.listen(Post.body, 'set', Post.on_changed_body)


#====================================================
# 其他
#====================================================
# 每个操作的权限定义
class Permission(object):
	FOLLOW = 0x01					# 关注他人
	COMMENT = 0x02					# 评论
	WRITE_ARTICLES = 0x04			# 写文章
	MODERATE_COMMENTS = 0x08		# 管理评论
	ADMINISTER = 0x80				# 管理员权限标记位

def GetTokenData(token):
	'''
	获取生成的令牌数据
	@param token:令牌字符串
	'''
	serializer = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
	try:
		data = serializer.loads(token)
	except:
		return None
	return data

# 重写匿名用户类并记录下来
class NewAnonymousUserMixin(AnonymousUserMixin):
	#====================================================
	# 角色权限验证函数(为了保证current_user不需要确保已经登录的前提下就可以使用权限验证函数， 请为匿名用户类也添加一下方法)
	#====================================================
	def can(self, permissions):
		return False
	
	def is_administrator(self):
		return False

login_manager.anonymous_user = NewAnonymousUserMixin			# 用户加载的时候使用这个类来创建匿名用户

# flask_login 当前登录用户current_user加载回调函数, 如果用户没有登录（session传递过来的user_id并不能登录， 就会使用AnonymousUserMixin实例， 这个实例是没有登录的）
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))


