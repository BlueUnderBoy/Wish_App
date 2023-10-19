from wish_app.config.mysqlconnection import connectToMySQL

class Aime:
    def __init__(self, data):
        self.aime_id = data['aime_id']
        self.user_id = data['user_id']
        self.wish_id = data['wish_id']

        
    @classmethod
    def save(cls, data):
        query = """INSERT INTO aime (user_id, wish_id)
                    VALUES (%(user_id)s, %(wish_id)s);"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results

    @classmethod
    def user_like(cls, data):
        query = """SELECT * FROM aime WHERE user_id = %(user_id)s AND wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        ulike = []
        if not results:
            count = len(ulike)
            return count
        else: 
            for x in results:
                ulike.append(cls(x))
        count = len(ulike)
        return count
    
    @classmethod
    def get_likes(cls, data):
        query = """SELECT * FROM aime WHERE wish_id = %(wish_id)s;"""
        results = connectToMySQL("wl_schema").query_db(query, data)
        count = []
        if not results:
            return len(count)
        else:
            for x in results:
                count.append(cls(x))
        return len(count)
    
    @classmethod
    def gal(cls, data):
        query = """SELECT * FROM wish
                    JOIN aime ON wish.wish_id = aime.wish_id
                    JOIN user ON user.user_id = aime.user_id
                    WHERE wish.wish_id = %(wish_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        gal = []
        print(results)
        if not results:
            return gal
        for x in results:
            gal.append(x)
        print(gal)
        return gal
        
    
    @classmethod
    def deletelike(cls, data):
        query = """DELETE FROM aime WHERE wish_id = %(wish_id)s AND user_id = %(user_id)s;"""
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, wish_id):
        query = """DELETE FROM aime WHERE wish_id = %(wish_id)s;"""
        data = {'wish_id' : wish_id}
        results = connectToMySQL('wl_schema').query_db(query, data)
        return results