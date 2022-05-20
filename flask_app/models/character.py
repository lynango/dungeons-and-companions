from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import session
import random
from flask_app.models.companion import Companion

class Character:
    def __init__(self, data):
        self.health = data['health']
        self.strength = data['strength']
        self.defense = data['defense']
        self.luck = data['luck']
    
    #Calls this function each turn
    @classmethod
    def roll_dice(luck):
        roll = random.randint(1+luck, 100+luck)
        if roll > 50:
            return True
        else:
            return False