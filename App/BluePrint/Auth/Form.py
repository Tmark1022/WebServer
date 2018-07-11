#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-27
# module	: App.BluePrint.Auth.Forms
#===================================================
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, EqualTo
from App.Models import User

class LoginForm(FlaskForm):
	email = StringField("email", validators = [Required(), Length(1, 64), Email()])
	passwrod = 	PasswordField("password", validators = [Required()])
	remember_me = BooleanField("自动登录")
	submit = SubmitField("log in")


class RegisterForm(FlaskForm):
	email = StringField("email", validators = [Required(), Length(1, 64), Email()])
	user_name = StringField("user name", validators = [Required(), Length(1, 20)])
	password = PasswordField("password", validators = [Required(), EqualTo("password_confirm", "password not match.")])
	password_confirm = PasswordField("password Confirm", validators = [Required()])
	submit = SubmitField("register")
	
	# validate_  +  变量名 会制动调用校验函数
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')
