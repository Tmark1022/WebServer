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


#====================================================
# flask拓展实例化
#====================================================
bootstrap = Bootstrap()
moment = Moment()



def CreateApp(config_name):
	'''
	创建flask app共厂函数
	@param config_name:
	'''
	config_obj = ConfigDict[config_name]
	app = Flask(__name__)
	app.config.from_object(config_obj)
	config_obj.init_app(app)
	
	
	
	# 拓展初始化
	bootstrap.init_app(app)
	moment.init_app(app)
	
	# 主蓝图加载
	from App.BluePrint.Main import main
	app.register_blueprint(main)
	
	# 游戏后台蓝图加载
	from App.BluePrint.GameRoute import gameRoute
	app.register_blueprint(gameRoute)
	
	return app