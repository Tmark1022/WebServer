from flask import Blueprint

auth = Blueprint("auth", __name__)

from App.BluePrint.Auth import Views