#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# XRLAM("App.Form")
#===============================================================================
# 表单模块
#===============================================================================
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import Required, Length, Email, EqualTo
from App.Models import User

class EditProfileForm(FlaskForm):
	location = StringField("location", validators = [Length(0, 64)])
	about_me = TextAreaField("about me")
	submit = SubmitField("Edit")

#class EditProfileAdminForm(FlaskForm):
#	
#	location = StringField("location", validators = [Length(0, 64)])
#	about_me = TextAreaField("about me")
#	submit = SubmitField("Edit")


