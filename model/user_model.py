import mysql.connector 
import json
import jwt
from flask import make_response
from datetime import datetime, timedelta

class user_model():
    def __init__(self):
        #connection establishment
        try:
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root", 
                password = "",
                database = "learning_flask")
            
            self.cur = self.conn.cursor(dictionary = True)

            self.conn.autocommit= True
            
            print('Connection Established!')
        except:
            print('Some Error')


    def user_get_all(self):
        self.cur.execute("SELECT * FROM uses")
        data = self.cur.fetchall()
        if(len(data)>0):
            #this is string -> Content type text/HTML
            # return json.dumps(data)
        
            #this is dict -> Content type application/json
            # return {"payload":data}
        
            #return response with response code  along with Content type application/json
            return make_response({"payload": data}, 200)
        else:  
            # return "No Data Found!" #this will return string with header- content type: text/html
            
            # return {"message":'No Data Found!'} #this will return dict whose header is application/json
            return make_response({"message": 'No Data Found!'}, 204) #204- if 204, message wont be carried forward
    
        
    def user_addone(self, data):
        self.cur.execute(f"INSERT INTO uses(name,email,phone,password) VALUES ('{data['name']}','{data['email']}','{data['phone']}','{data['password']}')")
        # return {"message":'New Data Added'}
        return make_response({"message":'New Data Added'}, 201) #201 for created
        
    def user_update(self, data):
        self.cur.execute(f"UPDATE uses SET name= '{data['name']}' , email='{data['email']}' , phone='{data['phone']}' ,password='{data['password']}' WHERE id='{data['id']}'") 
        if self.cur.rowcount > 0:
            # return {"message":'User Updated Successfully'}
            return make_response({"message":'Data Updated'}, 201)
        
        # return {"message":'No changes made!'} 
        return make_response({"message": 'No changes made!'}, 202)#202- Accepted but nothing to process
    
    def user_patch(self, data , id):
        query = "UPDATE uses SET "
        print(data)
        for key in data:
            query = query + f"{key} = '{data[key]}',"        
        query = query[:-1] + f" WHERE id={id}"

        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return make_response({"message":'Data Updated'}, 201)
        return make_response({"message": 'No changes made!'}, 202)#202- Accepted but nothing to process
        
    def user_delete(self, id):
        self.cur.execute(f"DELETE from uses WHERE id='{id}'")
        if self.cur.rowcount > 0:
            # return {"message":'User Deleted Successfully'}

            return make_response({"message":'User Deleted Successfully'}, 200)
        # return {"message":'No data Deleted!'} 
        return make_response({"message": 'No data Deleted!'}, 202)
    
    def user_pagination(self, limit, page):
        page = int(page)
        limit = int(limit)
        start = (page*limit)-limit

        self.cur.execute(f"SELECT * FROM uses LIMIT {start},{limit}")
        result = self.cur.fetchall()

        if len(result) > 0:
            return make_response({"payload":result, "page":page , 'limit':limit}, 200)
        
        return make_response({"message": 'No data Found!'}, 202)

    def create_avatar(self, id, path):
        self.cur.execute(f"UPDATE uses SET avatar='{path}' WHERE id='{id}'") 
        if self.cur.rowcount > 0:
            return make_response({"message":'User Avatar Updated Successfully'}, 200)
        return make_response({"message": 'Nothing has been changed!!'}, 202)
    
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id,name,email, phone, role_id FROM uses WHERE email = '{data['email']}' and password = '{data['password']}' ")
        userdata = self.cur.fetchall()[0]
        exp_time = int((datetime.now()+ timedelta(minutes = 15)).timestamp())
        payload = {
            'payload':userdata,
            'exp': exp_time
            }
        token = jwt.encode(payload, 'thisisthekey', algorithm = 'HS256')
        return make_response({'token': token}, 200)