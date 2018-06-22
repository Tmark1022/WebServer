#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Manage
#===================================================
import sys
default_encoding = 'utf-8'					# 设置默认编码（代码中中文的默认编码方式， 避免将python中存储的中文字符串传递到其他系统的时候显示编码不兼容）， 解决UnicodeDecodeError: ‘ascii’ codec can’t decode byte 0xe5 in position 108: ordinal not in range(128）报错
if sys.getdefaultencoding() != default_encoding:
	reload(sys)
	sys.setdefaultencoding(default_encoding)

from App import CreateApp, db
from flask_script import Manager, Shell

app = CreateApp("debug")
manager = Manager(app)

#====================================================
# 拓展flask_script命令
#====================================================
@manager.command
def Info():
	'''show infomation about this flask app.'''
	print '''\n    designed by Tmark.\n    contact us:779297395@qq.com'''

# 创建shell上下文
def make_shell_context():
	return dict(app=app, db = db, manager=manager)
manager.add_command("shell", Shell(make_context=make_shell_context))				# 创建一个新的shell来替代系统自带的flask_script shell



if __name__ == '__main__':
	manager.run()
	# app.run(debug=True, host="0.0.0.0")
