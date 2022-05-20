from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import session
from flask_app.models.character import Character
from flask_app.models.companion import Companion

#roll the dice
@app.route('/roll_dice')
def roll_dice():
    data = {
        'id' : session['companion_id']
    }
    luck = Companion.get_one(data).luck
    if Character.roll_dice(luck):
        pass
    else:
        pass