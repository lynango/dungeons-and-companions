from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Profession:
    db_name = "d&c_database"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.health = data['health']
        self.strength = data['strength']
        self.defense = data['defense']
        self.luck = data['luck']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    #get stats
    @classmethod
    def get_stats(cls, data):
        query = "SELECT * FROM classes WHERE name=%(name)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    
    #alternative method in case something goes wrong    
    # #get health
    # @classmethod
    # def get_health(cls, data):
    #     query = "SELECT health FROM classes WHERE name=%(name)s"
    #     result = connectToMySQL(cls.db_name).query_db(query, data)
    #     return result
    
    # #get strength
    # @classmethod
    # def get_strength(cls, data):
    #     query = "SELECT strength FROM classes WHERE name=%(name)s"
    #     result = connectToMySQL(cls.db_name).query_db(query, data)
    #     return result
    
    # #get defense
    # @classmethod
    # def get_defense(cls, data):
    #     query = "SELECT defense FROM classes WHERE name=%(name)s"
    #     result = connectToMySQL(cls.db_name).query_db(query, data)
    #     return result
    
    # #get luck
    # @classmethod
    # def get_luck(cls, data):
    #     query = "SELECT luck FROM classes WHERE name=%(name)s"
    #     result = connectToMySQL(cls.db_name).query_db(query, data)
    #     return result