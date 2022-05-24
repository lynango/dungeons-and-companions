from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import session
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
    # @classmethod
    # def update_info(cls, data):
    #     query = """
    #     UPDATE companions 
    #     SET name=%(name)s, picture=%(picture)s, story=%(story)s
    #     WHERE id=%(id)s
    #     """
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    
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
        SELECT MAX(score), companions.name, companions.win, companions.loss, companions.level, companions.updated_at, users.first_name, users.last_name, user_id
        FROM companions JOIN users ON companions.user_id=users.id 
        GROUP BY user_id ORDER BY MAX(score) desc LIMIT 20
        """
        return connectToMySQL(cls.db).query_db(query)
    
    #SCRATCH THAT
    # #calculate INITIAL stats from user choices(concept)
    # @classmethod
    # def calc_stat(cls, breed, profession, weapon):
    #     #assuming breed/profession/weapon data passed in is all in dictionary format
    #     total_stats = { 
    #         'id' : session['character_id'], #define in controller
    #         'health' : Breed.get_stats(breed).health + Profession.get_stats(profession).health + Weapon.get_stats(weapon).health,
    #         'strength' : Breed.get_stats(breed).strength + Profession.get_stats(profession).strength + Weapon.get_stats(weapon).strength,
    #         'defense' : Breed.get_stats(breed).defense + Profession.get_stats(profession).defense + Weapon.get_stats(weapon).defense,
    #         'luck' : Breed.get_stats(breed).luck + Profession.get_stats(profession).luck + Weapon.get_stats(weapon).luck,
    #         'level' : 1
    #     }
    #     Companion.update_stat(total_stats)
    #     #no return statement required(?)
        
    # data = {
    #     'health' : Breed.get_stats(request.form).health + Profession.get_stats(request.form).health + Weapon.get_stats(request.form).health,
    #     'strength' : Breed.get_stats(request.form).strength + Profession.get_stats(request.form).strength + Weapon.get_stats(request.form).strength,
    #     'defense' : Breed.get_stats(request.form).defense + Profession.get_stats(request.form).defense + Weapon.get_stats(request.form).defense,
    #     'luck' : Breed.get_stats(request.form).luck + Profession.get_stats(request.form).luck + Weapon.get_stats(request.form).luck
    # }
    
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
                "password": row['password'],
                "first_name": row ['first_name'],
                "last_name": row ['last_name'],
                "email": row ['email'],
            }
            author = user.User(user_data)
            # Associate the Message class instance with the User class instance by filling in the empty creator attribute in the Message class
            one_companion.creator = author
            all_companions.append(one_companion)
        return all_companions        