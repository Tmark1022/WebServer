#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-27
# module	: App.BluePrint.Auth.Views
#===================================================
from App.BluePrint.Auth import auth
from flask import redirect, url_for, render_template, flash
from flask import current_app, g, request, session
from flask_login import login_required, login_user, logout_user, current_user
from App.BluePrint.Auth.Form import LoginForm, RegisterForm
from App.Models import User
from App.Email import SendMessage
from App import db

# 定义全局的请求钩子
@auth.before_app_request
def before_app_request():
	if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
		# 已经登录且还没有认证， 而且请求不是auth蓝本
		return redirect(url_for('auth.RemindConfirm'))

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
		user = User(email = form.email.data, password = form.password.data, user_name = form.user_name.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		SendMessage("Register Confirm", [form.email.data,], "auth/email/confirm", user = user, token = token)
		flash("已发送注册验证邮件， 请前往邮件验证操作以完成注册")
		return redirect(url_for("main.Index"))
	return render_template("auth/register.html", form = form)

@auth.route("/user/info")
@login_required
def UserInfo():
	return "个人中心"

@auth.route("/confirm/<token>")
@login_required
def Confirm(token):
	if not current_user.confirmed:
		# 没有验证
		if current_user.confirm(token):
			flash("Confirm Successfully.")
		else:
			flash("this confirmation link is valid or has expired.")
	return redirect(url_for("main.Index"))

@auth.route("/remindconfirm")
@login_required
def RemindConfirm():
	if current_user.confirmed:
		return redirect(url_for("main.Index"))
	return render_template("auth/remindconfirm.html")

@auth.route("/confirm/newemail")
@login_required
def ResendEmail():
	token = current_user.generate_confirmation_token()
	SendMessage("Register Confirm", [current_user.email,], "auth/email/confirm", user = current_user, token = token)
	flash("新的注册验证邮件已发送， 请前往邮件验证操作以完成注册")
	return redirect(url_for("main.Index"))

