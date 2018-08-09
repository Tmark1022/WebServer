#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.Main.Views
#===================================================
import os
from App.BluePrint.Main import main
from flask import redirect, url_for, render_template, flash, make_response
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
	# 当前页(no.)
	page = request.args.get('page', 1, type=int)
	
	show_followed = False
	if current_user.is_authenticated:
		# 如果登录了就看下有没有要求显示关注者
		show_followed = bool(request.cookies.get('show_followed', ''))
	
	if show_followed:
		# 显示关注者文章
		query = current_user.followed_posts
	else:
		# 显示所有文章
		query = Post.query
	pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
	# 只显示当前页的文章
	posts = pagination.items
	return render_template('index.html', form=form, posts=posts, header_file = header_file, pagination=pagination, show_followed = show_followed)

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
	return render_template("normalform.html", form = form, header_file = header_file, header_text = "Edit your Profile")

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
	return render_template("normalform.html", form = form, header_file = header_file, header_text = "Modify Header Picture")

@main.route('/post/<int:id>')
def ShowPost(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', posts=[post], header_file = header_file)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def EditPost(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and not current_user.can(Permission.ADMINISTER):
		# 权限不够
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash('文章修改成功')
		return redirect(url_for('main.ShowPost', id=post.post_id))
	form.body.data = post.body
	return render_template('edit_post.html', form=form, header_file = header_file, header_text = "Edit Post")


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def Follow(username):
	user = User.query.filter_by(user_name=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('main.Index'))
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('main.UserInfo', username=username))
	current_user.follow(user)
	flash('You are now following %s.' % username)
	return redirect(url_for('main.UserInfo', username=username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def Unfollow(username):
	user = User.query.filter_by(user_name=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('main.Index'))
	if not current_user.is_following(user):
		flash('You are not following this user.')
		return redirect(url_for('main.UserInfo', username=username))
	current_user.unfollow(user)
	flash('You are not following %s anymore.' % username)
	return redirect(url_for('main.UserInfo', username=username))

@main.route('/followers/<username>')
def Followers(username):
	user = User.query.filter_by(user_name=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('main.Index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'], error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
	return render_template('followers.html', user=user, title="的粉丝", endpoint='main.Followers', pagination=pagination, follows=follows, header_file = header_file)

@main.route('/followed-by/<username>')
def Followed_by(username):
	user = User.query.filter_by(user_name=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followed.paginate(page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'], error_out=False)
	follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
	return render_template('followers.html', user=user, title="关注的", endpoint='main.Followed_by', pagination=pagination, follows=follows, header_file = header_file)


@main.route('/all')
@login_required
def ShowAll():
	response = make_response(redirect(url_for('main.Index')))
	response.set_cookie('show_followed', '', max_age=30*24*60*60)
	return response

@main.route('/followed')
@login_required
def ShowFollowed():
	resp = make_response(redirect(url_for('main.Index')))
	resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
	return resp

