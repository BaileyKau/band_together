from band_app.config.mysqlconnection import connectToMySQL
from flask import flash
from band_app.models.user import User

class Band: 
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.genre = data['genre']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def created_by(self):
        data = {
            'id': self.user_id
        }
        return User.user_by_id(data)

    @staticmethod
    def validate_band(data):
        isValid = True
        if len(data['name']) < 2:
            flash("Please include a name at least 2 characters long", "band")
            isValid = False
        if len(data['location']) < 1:
            flash("Please include a location", "band")
            isValid = False
        if len(data['genre']) < 2:
            flash("Please include a genre at least 2 characters long", "band")
            isValid = False
        return isValid
    
    @classmethod
    def get_band(cls, data):
        query = "SELECT * FROM bands WHERE id = %(id)s LIMIT 1"
        result = connectToMySQL('bands_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all_bands(cls):
        query = "SELECT * FROM bands"
        result = connectToMySQL('bands_schema').query_db(query)
        all_bands = []
        for row in result:
            all_bands.append(cls(row))
        return all_bands

    @classmethod
    def new_band(cls, data):
        query = '''
        INSERT INTO bands
        (user_id, name, genre, location)
        VALUES (%(user_id)s, %(name)s, %(genre)s, %(location)s)
        '''
        return connectToMySQL('bands_schema').query_db(query, data)
    
    @classmethod
    def update_band(cls, data):
        query = '''
        UPDATE bands SET name = %(name)s, 
        genre = %(genre)s, location = %(location)s
        WHERE id = %(id)s;
        '''
        return connectToMySQL('bands_schema').query_db(query, data)

    @classmethod 
    def delete_band(cls, data):
        query = "DELETE FROM bands WHERE id = %(id)s"
        connectToMySQL('bands_schema').query_db(query, data)

    @classmethod 
    def get_joined_bands(cls, data):
        query = '''
        SELECT *
        FROM bands 
        JOIN band_members ON bands.id = band_members.band_id
        JOIN users ON band_members.user_id = users.id
        WHERE users.id = %(id)s
        '''
        result = connectToMySQL('bands_schema').query_db(query, data)
        joined_bands = []
        for row in result:
            joined_bands.append(cls(row))
        return joined_bands
