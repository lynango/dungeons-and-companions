from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import session
import random
from flask_app.models.companion import Companion

class Battle:
    def __init__(self, data):
        self.health = data['health']
        self.strength = data['strength']
        self.defense = data['defense']
        self.luck = data['luck']
    
    #Dice roll for each turn
    @classmethod
    def roll_dice(cls, luck=0):
        roll = random.randint(1+luck, 100+luck)
        if roll > 50:
            return True
        else:
            return False
        
    #pick random ability
    @classmethod
    def skill(cls):
        num = random.randint(1, 3)
        ability = f'ability{num}'
        return ability