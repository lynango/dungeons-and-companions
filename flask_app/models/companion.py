from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.breed import Breed
from flask_app.models.profession import Profession
from flask_app.models.weapon import Weapon

class Companion:
    db_name = "d&c_database"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.breed = data['breed']
        self.profession = data['profession']
        self.weapon = data['weapon']
        self.ability1 = data['ability1']
        self.ability2 = data['ability2']
        self.ability3 = data['ability3']
        self.picture = data['picture']
        self.story = data['story']
        self.health = data['health']
        self.strength = data['strength']
        self.defense = data['defense']
        self.luck = data['luck']
        self.score = data['score']
        self.level = data['level']
        self.win = data['win']
        self.loss = data['loss']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    #create character
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO companions (name, breed, profession, weapon, ability1, ability2, ability3, picture, story, health, strength, defense, luck, score, level, win, loss, user_id)
        VALUES (%(name)s, %(breed)s, %(profession)s, %(weapon)s, %(ability1)s, %(ability2)s, %(ability3)s, %(picture)s, %(story)s, %(health)s, %(strength)s, %(defense)s, %(luck)s, 0, 1, 0, 0, %(user_id)s)
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #get character data
    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM companions WHERE id=%(id)s
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
    
    #get all characters of user
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM companions WHERE user_id=%(user_id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    #update character information
    @classmethod
    def update_info(cls, data):
        query = """
        UPDATE companions 
        SET name=%(name)s, picture=%(picture)s, story=%(story)s
        WHERE id=%(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    #update character stats
    @classmethod
    def update_stat(cls, data):
        query = """
        UPDATE companions 
        SET health=%(health)s, strength=%(strength)s, defense=%(defense)s, luck=%(luck)s, level=%(level)s
        WHERE id=%(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    #update character score
    @classmethod
    def update_score(cls, data):
        query = """
        UPDATE companions 
        SET score=%(score)s, level=%(level)s, win=%(win)s, loss=%(loss)s
        WHERE id=%(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    #delete character
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM companions WHERE id=%(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)