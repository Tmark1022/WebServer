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
from App.BluePrint.Auth.Form import LoginForm, RegisterForm, ChangePasswordForm, InputEmailForm
from App.Models import User, GetTokenData
from App.Email import SendMessage
from App import db, header_file

# 定义全局的请求钩子
@auth.before_app_request
def before_app_request():
	if current_user.is_authenticated:
		# 刷新用户最后登录时间
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
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
	return render_template("normalform.html", form = form, header_text = "Login", header_file = header_file)

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
		flash("已发送注册验证邮件， 请前往邮件验证操作以完成注册（注：如果接收不到邮件， 有可能是被当做垃圾邮件了，请接收并设置发送白名单以避免下次系统邮件被当做垃圾邮件)")
		return redirect(url_for("main.Index"))
	return render_template("normalform.html", form = form, header_text = "Register", header_file = header_file)

@auth.route("/confirm/<token>")
@login_required
def Confirm(token):
	token_data = GetTokenData(token)
	if not token_data or not token_data.get("confirm"):
		flash("this confirmation link is valid or has expired.")
		return redirect(url_for("main.Index"))
	
	# 当前登录用户不是令牌对应的用户
	token_user_id = token_data.get("confirm")
	if current_user.user_id != token_user_id:
		flash("请登录新注册的账户后再次点击邮件验证链接以完成注册验证.")
		return redirect(url_for("auth.Login"))
	
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
	return render_template("auth/remindconfirm.html", header_file = header_file)

@auth.route("/confirm/newemail")
@login_required
def ResendEmail():
	token = current_user.generate_confirmation_token()
	SendMessage("Register Confirm", [current_user.email,], "auth/email/confirm", user = current_user, token = token)
	flash("新的注册验证邮件已发送， 请前往邮件验证操作以完成注册")
	return redirect(url_for("main.Index"))

@auth.route("/password/validate", methods = ["GET", "POST"])
def ChangePasswordEmail():
	form  = InputEmailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if not user:
			flash("系统异常")
			return redirect(url_for("main.Index"))
		token = user.generate_confirmation_token(300)				# 过期时间为5分钟
		SendMessage("change password email", [form.email.data,], "auth/email/change_password", user = user, token = token)
		flash("已向注册邮箱发送修改密码邮件, 请尽快前往邮箱接受邮件并完成密码修改")
		return redirect(url_for("main.Index"))
	return render_template("normalform.html", form = form, header_text = "Reset Password", header_file = header_file)

@auth.route("/password/<token>", methods = ["GET", "POST"])
def ChangePasswordCommit(token):
	token_data = GetTokenData(token)
	if not token_data:
		flash("修改密码链接不正确或已经过时了， 请重新操作")
		return redirect(url_for("main.Index"))
	user_id = token_data.get("confirm")
	if not user_id:
		flash("令牌数据异常")
		return redirect(url_for("main.Index"))
	
	form = ChangePasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(user_id = user_id).first()
		if not user:
			flash("系统异常")
			return redirect(url_for("main.Index"))
		user.password = form.password.data
		db.session.add(user)
		flash("密码修改成功")
		return redirect(url_for("auth.Login"))
	return render_template("normalform.html", form = form, header_text = "Reset Password", header_file = header_file)

