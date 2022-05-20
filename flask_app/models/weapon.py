from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Weapon:
    db_name = "d&c_database"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
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