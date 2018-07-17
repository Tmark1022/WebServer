#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Views
#===================================================
from App.BluePrint.Main import main
from flask import redirect, url_for, render_template, flash
from flask import current_app, g, request, session
from App.Models import Permission
from App.Decorators import permission_required, admin_required


from App.BluePrint.Main.Form import RegisterForm


@main.route("/")
def Index():
	return render_template("index.html")

@main.route("/<name>")
@permission_required(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES)
def Greeting(name):
	# 增加了角色权限， 还有普通用户以上权限（当然一定要先登录）才能访问
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

@main.route("/test/for_admin", methods = ['GET'])
@admin_required
def for_adminstarter():
	return "for_adminstarter"

@main.route("/test/for_moderator", methods = ['GET'])
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderator():
	return "for_moderator"
