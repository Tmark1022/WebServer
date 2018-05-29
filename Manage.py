#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: Manage
#===================================================
from App import CreateApp


app = CreateApp("debug")


if __name__ == '__main__':
	app.run(host="0.0.0.0")
