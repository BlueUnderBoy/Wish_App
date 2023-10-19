from flask import flash
from datetime import datetime
from wish_app.config.mysqlconnection import connectToMySQL

class Wish:
    def __init__(self, data):
        self.wish_id = data['wish_id']
        self.item = data['item']
        self.dateadd = data['dateadd']
        self.dategrant = data['dategrant']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.realda = data['realda']
        self.realdg = data['realdg']
        self.likes = data['likes']

    def __repr__(self):
        return self.item
    
    @classmethod
    def validation_wish(cls, data):
        is_valid = True
        if len(data['item']) < 3:
            flash('The wish must consist of at least 3 characters.', 'create')
            is_valid = False
        if len(data['description']) < 1:
            flash('Description must be provided', 'create')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO wish (item, dateadd, description, user_id, created_at, updated_at, realda)
                    VALUES (%(item)s, %(dateadd)s, %(description)s, %(user_id)s, %(created_at)s, %(updated_at)s, %(realda)s);"""

        results = connectToMySQL('wl_schema').query_db(query, data)
        return results
    
    @classmethod
    def joined(cls, data):
        query = """INSERT INTO follow (user_id, wish_id)
                    VALUES (%(user_id)s, %(wish_id)s);"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results
    
    @classmethod
    def update(cls, data):
        query = """UPDATE wish
                    SET item = %(item)s, dateadd = %(dateadd)s, description = %(description)s, updated_at = %(updated_at)s
                    WHERE wish_id = %(wish_id)s;"""
        
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results 
    
    @classmethod
    def gdate(cls, data):
        query = """UPDATE wish
                    SET dategrant = %(dategrant)s, updated_at = NOW()
                    WHERE wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results 

    @classmethod
    def get_one(cls, wish_id):
        query = """SELECT * FROM wish WHERE wish_id = %(wish_id)s"""
        data = {'wish_id': wish_id}
        results = connectToMySQL('wl_schema').query_db(query, data)
        fav = cls(results[0])
        return fav
    
    @classmethod
    def get_mine(cls, data):
        query = """SELECT * FROM wish WHERE user_id = %(user_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        mwishes = []
        lr = len(results)
        if not results:
            return mwishes
        else:
            for x in range(0, lr):
                mwishes.append(results[x])
        return mwishes
    
    @classmethod
    def get_others(cls, data):
        query = """SELECT * FROM wish WHERE user_id != %(user_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        owishes = []
        lr = len(results)
        if not results:
            return owishes
        else:
            for x in range(0, lr):
                owishes.append(results[x])
        return owishes


    @classmethod
    def get_all(cls):
        query = """SELECT * FROM wish;"""
        results = connectToMySQL('wl_schema').query_db(query)
        favs = []
        for x in results:
            favs.append(cls(x))
        return favs

    @classmethod
    def allinfo(cls, data):
        query = """SELECT * FROM wish
                    JOIN user ON user.user_id = wish.user_id
                    WHERE wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        userwish = results[0]
        print(userwish)
        return userwish
    
    @classmethod
    def ulike(cls, data):
        query = """UPDATE wish
                    SET likes = %(likes)s, updated_at = NOW()
                    WHERE wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results
        
    
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM wish WHERE wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results

    
