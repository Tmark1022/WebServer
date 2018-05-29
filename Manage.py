#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Manage
#===================================================
from App import CreateApp
from flask_script import Manager

app = CreateApp("debug")
manager = Manager(app)

if __name__ == '__main__':
	manager.run()
