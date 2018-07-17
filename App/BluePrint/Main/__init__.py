#-*- coding:UTF-8 -*-
from flask import Blueprint

main = Blueprint("main", __name__)

from App.BluePrint.Main import Views, Errors

# jinja模板上下文(这是全局的)
@main.app_context_processor
def inject_permission():
	from App.Models import Permission
	return dict(Permission = Permission)
