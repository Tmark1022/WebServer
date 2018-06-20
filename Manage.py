#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Manage
#===================================================
from App import CreateApp
from flask_script import Manager, Shell, Command

app = CreateApp("debug")
manager = Manager(app)



#====================================================
# 拓展flask_script命令
#====================================================
@manager.command
def Info():
	'''show infomation about this flask app.'''
	print '''\n    designed by Tmark.\n    contact us:779297395@qq.com'''


if __name__ == '__main__':
	# manager.run()
	app.run(debug=True, host="0.0.0.0")
