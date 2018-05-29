from flask import Blueprint

main = Blueprint("main", __name__)

from App.BluePrint.Main import Views, Errors