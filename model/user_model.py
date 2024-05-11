import mysql.connector 
import json
from flask import make_response

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
        self.cur.execute(f"INSERT INTO uses(name,email,phone,role,password) VALUES ('{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}')")
        # return {"message":'New Data Added'}
        return make_response({"message":'New Data Added'}, 201) #201 for created
        
    def user_update(self, data):
        self.cur.execute(f"UPDATE uses SET name= '{data['name']}' , email='{data['email']}' , phone='{data['phone']}', role='{data['role']}' ,password='{data['password']}' WHERE id='{data['id']}'") 
        if self.cur.rowcount > 0:
            # return {"message":'User Updated Successfully'}
            return make_response({"message":'New Data Added'}, 201)
        
        # return {"message":'No changes made!'} 
        return make_response({"message": 'No changes made!'}, 202)#202- Accepted but nothing to process
        
    def user_delete(self, id):
        self.cur.execute(f"DELETE from uses WHERE id='{id}'")
        if self.cur.rowcount > 0:
            # return {"message":'User Deleted Successfully'}

            return make_response({"message":'User Deleted Successfully'}, 200)
        # return {"message":'No data Deleted!'} 
        return make_response({"message": 'No data Deleted!'}, 202)