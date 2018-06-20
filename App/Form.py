#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# XRLAM("App.Form")
#===============================================================================
# 表单模块
#===============================================================================
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import Required


class RegisterForm(FlaskForm):
	user_id = StringField("id:", validators = [Required()])
	password = PasswordField("password:", validators = [Required()])
	text_mark = TextAreaField("mark:", validators = [Required()])
	submit = SubmitField("submit")

