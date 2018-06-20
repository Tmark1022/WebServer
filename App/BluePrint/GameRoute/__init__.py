from flask import Blueprint

gameRoute = Blueprint("gameRoute", __name__)

from App.BluePrint.GameRoute import BackStage

