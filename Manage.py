#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Manage
#===================================================
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
