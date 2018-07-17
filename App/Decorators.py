#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-7-17
# module	: App.Decorators
#===================================================
from functools import wraps
from flask import abort
from flask_login import current_user
from App.Models import Permission

#====================================================
# 角色权限装饰器
#====================================================
def permission_required(permission):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if not current_user.can(permission):
				abort(403)
			return func(*args, **kwargs)
		return wrapper
	return decorator

def admin_required(func):
	return permission_required(Permission.ADMINISTER)(func)
