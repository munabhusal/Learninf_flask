from app import app
from model.user_model import user_model
from model.auth_model import auth_model

from flask import request, send_file
from datetime import datetime

object = user_model()
auth = auth_model()

@app.route('/user/getall')
@auth.token_auth('/user/getall')
def user_getall_controller():
    return object.user_get_all()

@app.route('/user/addone', methods = ['POST'])
@auth.token_auth('/user/addone')
def user_addone_controller():
    return object.user_addone(request.form)

@app.route('/user/update', methods = ['PUT'])
@auth.token_auth('/user/update')
def user_update_controller():
    # print(request.form)
    return object.user_update(request.form)

@app.route('/user/update/patch/<id>', methods = ['PATCH'])
def user_update_patch_controller(id):
    return object.user_patch(request.form , id)

@app.route('/user/delete/<id>', methods = ['DELETE'])
def user_delete_controller(id):
    return object.user_delete(id)

@app.route('/user/getall/limit/<limit>/page/<page>', methods = ['GET'])
def user_pagination_controller(limit, page):
    return object.user_pagination(limit , page)

@app.route('/user/create/avatar/<id>', methods = ['PUT'])
def user_create_avatar_controller(id):
    avatar = request.files['avatar']

    # Saving Avatar with its original name
    # avatar.save(f"avatars/{avatar.filename}")

    #Saving Avatar with diffrent name - name will be generated with respect to the current time
    unique_filename = str(datetime.now().timestamp()).replace(".", "")
    ext = avatar.filename.split('.')[-1]
    file_path ='avatars/'+unique_filename+'.'+ext    
    avatar.save(f"{file_path}")

    return object.create_avatar(id, file_path)


@app.route('/avatars/<filename>', methods = ['GET'])
def user_get_avatar_controller(filename):
    return send_file(f"avatars/{filename}")

@app.route('/user/login/', methods = ['POST'])
def user_login_controller():
    # user_login_model
    # request.form
    return object.user_login_model(request.form)