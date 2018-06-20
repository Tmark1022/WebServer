#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Views
#===================================================
from App.BluePrint.Main import main
from flask import redirect, url_for, render_template, flash
from flask import current_app, g, request, session

from App.Form import RegisterForm

@main.route("/")
def Index():
	return render_template("index.html")

@main.route("/<name>")
def Greeting(name):
	print current_app.name, g, request, session
	print "hello world"
	print current_app.url_map
	return render_template("greet.html", aaaa = "tmark")

@main.route("/form/test1", methods = ['GET'])
def Test1():
	form  = RegisterForm()
	return render_template("test_form.html", form = form, user_id = session.get("user_id"))

@main.route("/form/test2", methods = ['POST'])
def Test2():
	form  = RegisterForm()
	if form.validate_on_submit():
		session["user_id"] = form.user_id.data
		flash("登录成功")
		return redirect(url_for("main.Test1"))
	return "no form"