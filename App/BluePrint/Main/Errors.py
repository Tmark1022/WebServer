#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Errors
#===================================================
from App.BluePrint.Main import main

@main.app_errorhandler(404)
def ErrorHandler404(e):
	return "404 not found.", 404


@main.app_errorhandler(500)
def ErrorHandler500(e):
	return "internal server error.", 500
