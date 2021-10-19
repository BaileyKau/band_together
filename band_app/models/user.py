from band_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User: 
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']    
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @property
    def full_name(self):
        return (f"{self.first_name} {self.last_name}")
    
    @staticmethod
    def validate_credentials(data):
        isValid = True
        if User.user_by_email(data):
            flash("Email is already in use", "register")
            isValid = False
        if len(data['first_name']) < 2 or data['first_name'].isdigit():
            flash("Invalid First Name", "register")
            isValid = False
        if len(data['last_name']) < 2 or data['last_name'].isdigit():
            flash("Invalid Last Name", "register")
            isValid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address", "register")
            isValid = False
        if len(data['password']) < 8:
            flash("Password must be 8 characters", "register")
            isValid = False
        if data['password'] != data['confirm']:
            flash("Confirm Password must match your password", "register")
            isValid = False
        return isValid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('bands_schema').query_db(query, data)

    @classmethod 
    def user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('bands_schema').query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('bands_schema').query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def join_band(cls, data):
        query = '''
        INSERT INTO band_members 
        (user_id, band_id)
        VALUES (%(user_id)s, %(band_id)s);
        '''
        return connectToMySQL('bands_schema').query_db(query, data)

    @classmethod
    def quit_band(cls, data):
        query = '''
        DELETE FROM band_members
        WHERE user_id = %(user_id)s AND band_id = %(band_id)s
        '''
        connectToMySQL('bands_schema').query_db(query, data)