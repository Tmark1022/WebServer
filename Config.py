#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Config
#===================================================
import os
import platform


#====================================================
# 重要环境
#====================================================
SystemVersion = platform.system()				# 操作系统

def IsWindows():
	if SystemVersion == "Windows":
		return True
	else:
		return False

def IsLinux():
	if SystemVersion == "Linux":
		return True
	else:
		return False

ConfigBasedir = os.path.abspath(os.path.dirname(__file__))


#====================================================
# 基本配置
#====================================================
class Config(object):
	# 秘钥
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	
	# 数据库
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(ConfigBasedir, 'data.sqlite')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	# 邮件
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "Ms_mac@163.com"
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "tmac15626476229"
	MAIL_SENDER = MAIL_USERNAME
	
	# 管理员账号
	FLASK_ADMIN_USER = "779297395@qq.com"
	
	# 上传文件目录
	UPLOADED_HEADER_DEST = os.path.join(ConfigBasedir, os.sep.join(["App", "static", "header"]))					# 头像文件存储路径
	
	# 每页显示文章数和每页显示粉丝数量
	FLASKY_POSTS_PER_PAGE = 12
	FLASKY_FOLLOWERS_PER_PAGE = 20
	
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


if __name__ == '__main__':
	print "Windows:", IsWindows()
	print "Linux:", IsLinux()
	
	print os.path.join(Config.UPLOAD_FOLDER, "memeda.jpg")
