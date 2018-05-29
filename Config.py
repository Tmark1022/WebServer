#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Config
#===================================================
import os


#====================================================
# 路径
#====================================================
ConfigBasedir = os.path.abspath(os.path.dirname(__file__))


#====================================================
# 基本配置
#====================================================
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(ConfigBasedir, 'data.sqlite')
	
	@staticmethod
	def init_app(app):
		pass
	
#====================================================
# 开发环境配置
#====================================================
class DebugConfig(Config):
	pass

#====================================================
# 发布环境配置
#====================================================
class ReleaseConfig(Config):
	pass
	
	

#====================================================
# 配置索引字典
#====================================================
ConfigDict = {"debug":DebugConfig, "release":ReleaseConfig}


if __name__ == '__main__':
	config_obj = ConfigDict["debug"]
	for aa in dir(config_obj):
		if aa.isupper():
			print "%s:%s" % (aa, getattr(config_obj, aa))

