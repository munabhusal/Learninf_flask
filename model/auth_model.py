import mysql.connector 
import json
import jwt
import re
from flask import make_response, request
from functools import wraps

from config.config import db_config

class auth_model():
    def __init__(self):
        #connection establishment
        try:
            self.conn = mysql.connector.connect(
                host = db_config['host'],
                user = db_config['user'], 
                password = db_config['password'],
                database = db_config['database'])
            
            self.cur = self.conn.cursor(dictionary = True)
            self.conn.autocommit= True            
            print('Connection Established!')
        except:
            print('Some Error')



    def token_auth(self, endpoint=''):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                print(endpoint)
                authorization_val = (request.headers.get('Authorization'))
                if re.match('^Bearer *([^ ]+) *$', authorization_val, flags=0):
                    token = authorization_val.split(' ')[1]        
                    try:
                        decoded_jwt = jwt.decode(token, 'thisisthekey', algorithms= 'HS256')
                    except jwt.ExpiredSignatureError:
                        return make_response({'Error': 'Signature Expired!'}, 401)
                    role_id = decoded_jwt['payload']['role_id']
                    self.cur.execute(f"SELECT roles FROM accessibility_views WHERE endpoint = '{endpoint}'")
                    result = self.cur.fetchall()
                    if (len(result)>0):
                        auth_role = json.loads(result[0]['roles'])
                        if role_id in auth_role:
                            pass
                        else:
                            return make_response({'Error': 'Invalid Role!'}, 401)
                    else:
                        return make_response({'Error': 'Unknown Endpoint!'}, 404)
                    return func(*args)
                else:
                    return make_response({'Error': 'Invalid Token!'}, 401)
            return inner2
        return inner1
