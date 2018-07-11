#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-27
# module	: App.BluePrint.Auth.Views
#===================================================
from App.BluePrint.Auth import auth
from flask import redirect, url_for, render_template, flash
from flask import current_app, g, request, session
from flask_login import login_required, login_user, logout_user
from App.BluePrint.Auth.Form import LoginForm, RegisterForm
from App.Models import User
from App.Email import SendMessage


@auth.route("/login", methods = ["GET", "POST"])
def Login():
	form  = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is not None and user.verify_password(form.passwrod.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get("next") or url_for("main.Index"))
		flash("账号有误")
	return render_template("auth/login.html", form = form)

@auth.route("/logout")
def Logout():
	logout_user()
	flash("退出登录成功")
	return redirect(url_for("main.Index"))

@auth.route("/register", methods = ["GET", "POST"])
def Register():
	form  = RegisterForm()
	if form.validate_on_submit():
#		user = User.query.filter_by(email = form.email.data).first()
#		if user is not None and user.verify_password(form.passwrod.data):
#			login_user(user, form.remember_me.data)
#			return redirect(request.args.get("next") or url_for("main.Index"))
		SendMessage("Register Confirm", [form.email.data,], "auth/email/confirm")
		flash("注册成功")
	return render_template("auth/register.html", form = form)

@auth.route("/user/info")
@login_required
def UserInfo():
	return "个人中心"