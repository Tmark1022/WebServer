#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Views
#===================================================
import os
from App.BluePrint.Main import main
from flask import redirect, url_for, render_template, flash
from flask import current_app, g, request, session, abort, send_file, send_from_directory
from App.Models import Permission
from App.Decorators import permission_required, admin_required
from App.Models import User, Post
from flask_login import login_required, current_user
from App.BluePrint.Main.Form import EditProfileForm, UploadFileForm, PostForm
from App import db, header_file

@main.route("/", methods = ['GET', 'POST'])
def Index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data, author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('main.Index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html', form=form, posts=posts, header_file = header_file)

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
	posts = user.posts.order_by(Post.timestamp.desc()).all()
	return render_template("user_info.html", user = user, header_file = header_file, posts = posts)

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
	return render_template("normalform.html", form = form, header_text = "Edit your Profile")

## 用于查看
#@main.route("/upload/<filename>")
#def upload_file(filename):
#	return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename, as_attachment = True)

@main.route("/upload/header", methods = ['GET', 'POST'])
@login_required
def UploadHeaderFile():
	form  = UploadFileForm()
	if form.validate_on_submit():
		# 删除原本的文件
		if current_user.header_picutre:
			del_file_name_path = header_file.path(current_user.header_picutre)
			if os.path.exists(del_file_name_path):
				os.remove(del_file_name_path)
		current_user.header_picutre = header_file.save(form.file.data, name = "p%s.jpg" % current_user.user_id)
		db.session.add(current_user)
		flash("上传头像成功")
		return redirect(url_for("main.UserInfo", username = current_user.user_name))
	return render_template("normalform.html", form = form, header_text = "Modify Header Picture")


