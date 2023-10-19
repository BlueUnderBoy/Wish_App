from wish_app.config.mysqlconnection import connectToMySQL

class Grant:
    def __init__(self, data):
        self.grant_id = data['grant_id']
        self.user_id = data['user_id']
        self.wish_id = data['wish_id']

        
    @classmethod
    def save(cls, data):
        query = """INSERT INTO granted (user_id, wish_id)
                    VALUES (%(user_id)s, %(wish_id)s);"""
        
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results 

    @classmethod
    def user_grant(cls, data):
        query = """SELECT * FROM granted WHERE user_id = %(user_id)s AND wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        ugrant = []
        if not results:
            count = len(ugrant)
            return count
        else: 
            for x in results:
                ugrant.append(cls(x))
        count = len(ugrant)
        return count
    
    @classmethod
    def get_mine(cls, data):
        query = """SELECT * FROM wish
                    JOIN granted ON wish.wish_id = granted.wish_id
                    JOIN user ON user.user_id = granted.user_id
                    WHERE wish.user_id = %(user_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        mgwishes = []
        if not results:
            return mgwishes
        else:
            for x in results:
                mgwishes.append(x)
        print(results)
        return mgwishes
    
    @classmethod
    def get_other(cls, data):
        query = """SELECT * FROM user
                    JOIN granted ON user.user_id = granted.user_id
                    JOIN wish ON wish.wish_id = granted.wish_id
                    WHERE user.user_id != %(user_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        getother = []
        if not results:
            return getother
        for x in results:
            getother.append(x)
        print(getother)
        return getother
    
    @classmethod
    def get_grants(cls, data):
        query = """SELECT * FROM granted WHERE wish_id = %(wish_id)s;"""
        results = connectToMySQL("wl_schema").query_db(query, data)
        count = []
        if not results:
            return len(count)
        else:
            for x in results:
                count.append(cls(x))
        return len(count)
    
    @classmethod
    def gaw(cls):
        query = """SELECT * FROM wish
                    JOIN granted ON wish.wish_id = granted.wish_id
                    JOIN user ON user.user_id = granted.user_id;"""
        results = connectToMySQL('wl_schema').query_db(query)
        gaw = []
        print(results)
        if not results:
            return gaw
        for x in results:
            gaw.append(x)
        return gaw
        
    @classmethod
    def deletegrant(cls, data):
        query = """DELETE FROM granted WHERE wish_id = %(wish_id)s AND user_id = %(user_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, wish_id):
        query = """DELETE FROM granted WHERE wish_id = %(wish_id)s;"""
        data = {'wish_id' : wish_id}
        results = connectToMySQL('wl_schema').query_db(query, data)
        if not results:
            pass
        return results