#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Views
#===================================================
from App.BluePrint.Main import main
from flask import redirect, url_for

@main.route("/")
def Index():
	return "welcome."

@main.route("/<name>")
def Greeting(name):
	return redirect(url_for("main.Index"))