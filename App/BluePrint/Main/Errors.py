#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Errors
#===================================================
from App.BluePrint.Main import main
from flask import render_template

@main.app_errorhandler(404)
def ErrorHandler404(e):
	return render_template("404.html")

@main.app_errorhandler(500)
def ErrorHandler500(e):
	return render_template("500.html")
