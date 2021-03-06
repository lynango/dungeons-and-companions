from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import session, flash
from flask_app.models.breed import Breed
from flask_app.models.profession import Profession
from flask_app.models.weapon import Weapon
from flask_app.models import user

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
        self.creator = None
        
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
        SELECT * FROM companions WHERE id=%(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_health(cls, data):
        query = "Select health from comapnions WHERE id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    #get all characters of user
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM companions WHERE user_id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        companions = []
        for companion in results:
            companions.append(cls(companion))
        return companions

    #update character information
    @classmethod
    def update_info(cls, data):
        query = """
        UPDATE companions 
        SET name=%(name)s, ability1=%(ability1)s, ability2=%(ability2)s, ability3=%(ability3)s, picture=%(picture)s, story=%(story)s,
        updated_at=NOW() WHERE id=%(id)s
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #update character stats
    @classmethod
    def update_stat(cls, data):
        query = """
        UPDATE companions 
        SET health= health+%(health)s, strength= strength+%(strength)s, defense= defense+%(defense)s, luck= luck+%(luck)s
        WHERE id=%(id)s
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #update character score
    @classmethod
    def update_score(cls, data):
        query = """
        UPDATE companions 
        SET score= score + %(score)s, level= level + %(level)s, win= win + %(win)s, loss= loss + %(loss)s
        WHERE id=%(id)s
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #delete character
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM companions WHERE id=%(id)s
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    #get best score of all users (top 20)
    @classmethod
    def leaderboard(cls):
        query = """
    #New MYSQL Query
        WITH added_row_number AS (
        SELECT users.first_name, users.last_name, users.id, companions.score as highscore, companions.name, companions.picture, companions.level, companions.win, companions.loss, companions.updated_at,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY score DESC) AS row_numbe
        FROM companions, users 
        WHERE companions.user_id=users.id
        ORDER BY companions.score DESC
        )
        SELECT *
        FROM added_row_number
        WHERE row_numbe = 1
        LIMIT 20;
    #Old MYSQL Query
        # SELECT users.first_name, users.last_name, users.id, companions.name, companions.picture, companions.level, companions.win, companions.loss, companions.updated_at, 
        # MAX(companions.score) OVER (PARTITION BY companions.user_id) AS highscore
        # FROM users, companions 
        # WHERE companions.user_id=users.id
        # GROUP BY user_id
        # ORDER BY highscore DESC
        # LIMIT 20;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        scores = results
        print(type(scores))
        return scores
    
# Retrieve all messages with creator
    @classmethod
    def get_all_companions_with_creator(cls):
        query = """
        SELECT * FROM companions 
        JOIN users ON companions.user_id = users.id 
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        all_companions = []
        for row in results:
            one_companion = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row ['first_name'],
                "last_name": row ['last_name'],
                "email": row ['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            author = user.User(user_data)
            # Associate the Companion class instance with the User class instance by filling in the empty creator attribute in the Companion class
            one_companion.creator = author
            all_companions.append(one_companion)
        return all_companions        

    #validate create companion
    @staticmethod
    def validate_create(companion):
        is_valid = True
        if len(companion['name']) < 2:
            flash("Name must be at least 2 characters")
            is_valid= False
        if companion['breed'] == '0':
            flash("Please select a breed")
            is_valid= False
        if companion['profession'] == '0':
            flash("Please select a profession")
            is_valid= False
        if companion['weapon'] == '0':
            flash("Please select a weapon")
            is_valid= False
        if companion['ability1'] == '0':
            flash("Please select first ability")
            is_valid= False
        if companion['ability2'] == '0':
            flash("Please select second ability")
            is_valid= False
        if companion['ability3'] == '0':
            flash("Please select third ability")
            is_valid= False
        return is_valid
    
    #validate update companion
    @staticmethod
    def validate_update(companion):
        is_valid = True
        if len(companion['name']) < 2:
            flash("Name must be at least 2 characters")
            is_valid= False
        return is_valid