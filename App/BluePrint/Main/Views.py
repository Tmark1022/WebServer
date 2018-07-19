#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Views
#===================================================
from App.BluePrint.Main import main
from flask import redirect, url_for, render_template, flash
from flask import current_app, g, request, session, abort
from App.Models import Permission
from App.Decorators import permission_required, admin_required
from App.Models import User
from flask_login import login_required, current_user
from App.BluePrint.Main.Form import EditProfileForm
from App import db

@main.route("/")
def Index():
	return render_template("index.html")

@main.route("/<name>")
@permission_required(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES)
def Greeting(name):
	# 增加了角色权限， 还有普通用户以上权限（当然一定要先登录）才能访问
	return render_template("greet.html", aaaa = "tmark")

@main.route("/test/for_admin", methods = ['GET'])
@admin_required
def for_adminstarter():
	return "for_adminstarter"

@main.route("/test/for_moderator", methods = ['GET'])
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderator():
	return "for_moderator"

@main.route("/user/<username>")
def UserInfo(username):
	user = User.query.filter_by(user_name = username).first()
	if not user:
		abort(404)
	return render_template("user_info.html", user = user)

@main.route("/user/edit_profile", methods = ['GET', 'POST'])
@login_required
def EditProfile():
	form  = EditProfileForm()
	if form.validate_on_submit():
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash("修改个人信息成功")
		return redirect(url_for("main.UserInfo", username = current_user.user_name))
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template("edit_profile.html", form = form)


