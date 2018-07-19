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
from flask_wtf.file import FileField, FileAllowed, FileRequired
from App import header_file

class EditProfileForm(FlaskForm):
	location = StringField("location", validators = [Length(0, 64)])
	about_me = TextAreaField("about me")
	submit = SubmitField("Edit")

class UploadFileForm(FlaskForm):
	file = FileField("选择图片(jpg,jpe,jpeg,png,gif,svg,bmp)", validators = [FileAllowed(header_file, u"文件格式不正确"), FileRequired()])
	submit = SubmitField("uploads")




#class EditProfileAdminForm(FlaskForm):
#	
#	location = StringField("location", validators = [Length(0, 64)])
#	about_me = TextAreaField("about me")
#	submit = SubmitField("Edit")


