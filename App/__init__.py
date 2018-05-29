#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: App
#===================================================
from flask import Flask
from Config import ConfigDict


def CreateApp(config_name):
	'''
	创建flask app共厂函数
	@param config_name:
	'''
	config_obj = ConfigDict[config_name]
	app = Flask(__name__)
	app.config.from_object(config_obj)
	config_obj.init_app(app)
	
	from App.BluePrint.Main import main
	app.register_blueprint(main)
	
	return app