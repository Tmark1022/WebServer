#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-28
# module	: App.Email
#===================================================
from flask import render_template
from flask_mail import  Message
from App import mail
from threading import Thread


def SyncSendMsg(app, msg):
	with app.app_context():
		mail.send(msg)
	
# 发送邮件
def SendMessage(subject, to, template, **kwargs):
	from Manage import app
	msg = Message(subject, to, sender=app.config["MAIL_SENDER"]);

	msg.body = render_template(template + ".txt", **kwargs)
	msg.html = render_template(template + ".html", **kwargs)
	
	# 异步发送邮件
	thr = Thread(target=SyncSendMsg, args=(app, msg))
	thr.start()
	return thr
	