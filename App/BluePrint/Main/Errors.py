#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Errors
#===================================================
from App.BluePrint.Main import main
from flask import render_template
from App import header_file

@main.app_errorhandler(404)
def ErrorHandler404(e):
	return render_template("404.html", header_file = header_file)

@main.app_errorhandler(500)
def ErrorHandler500(e):
	return render_template("500.html", header_file = header_file)

@main.app_errorhandler(403)
def ErrorHandler403(e):
	return render_template("403.html", header_file = header_file)
