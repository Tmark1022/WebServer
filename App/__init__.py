#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: App
#===================================================
from flask import Flask
from Config import ConfigDict
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



def PrintConfig(config_obj):
	print "----------------Config Info-----------------------------"
	for aa in dir(config_obj):
		if aa.isupper():
			print "%s:%s" % (aa, getattr(config_obj, aa))
	print "----------------Config end-----------------------------"

#====================================================
# flask拓展实例化
#====================================================
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.Login"



def CreateApp(config_name):
	'''
	创建flask app共厂函数
	@param config_name:
	'''
	config_obj = ConfigDict[config_name]
	PrintConfig(config_obj)
	
	app = Flask(__name__)
	app.config.from_object(config_obj)
	config_obj.init_app(app)
	
	# 拓展初始化
	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	
	# 主蓝图加载
	from App.BluePrint.Main import main
	app.register_blueprint(main)
	
	# 游戏后台蓝图加载
	from App.BluePrint.GameRoute import gameRoute
	app.register_blueprint(gameRoute)
	
	# 用户验证蓝图
	from App.BluePrint.Auth import auth
	app.register_blueprint(auth, url_prefix = "/auth")
	
	
	return app
	