#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-6-27
# module	: App.BluePrint.Auth.Forms
#===================================================
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email

class LoginForm(FlaskForm):
	email = StringField("email", validators = [Required(), Length(1, 64), Email()])
	passwrod = 	PasswordField("password", validators = [Required()])
	remember_me = BooleanField("自动登录")
	submit = SubmitField("log in")