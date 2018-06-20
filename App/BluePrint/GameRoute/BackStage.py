#-*- coding:UTF-8 -*-
#===================================================
# author	: Tmark
# date 		: 2018-5-29
# module	: App.BluePrint.GameRoute.BackStage
#===================================================
from App.BluePrint.GameRoute import gameRoute



@gameRoute.route("/game/backstage/<action_id>")
def GameActionHandler(action_id):
	return action_id

