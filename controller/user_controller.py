from app import app
from model.user_model import user_model
from flask import request

object = user_model()

@app.route('/user/getall')
def user_getall_controller():
    return object.user_get_all()

@app.route('/user/addone', methods = ['POST'])
def user_addone_controller():
    return object.user_addone(request.form)

@app.route('/user/update', methods = ['PUT'])
def user_update_controller():
    # print(request.form)
    return object.user_update(request.form)

@app.route('/user/update/patch/<id>', methods = ['PATCH'])
def user_update_patch_controller(id):
    return object.user_patch(request.form , id)

@app.route('/user/delete/<id>', methods = ['DELETE'])
def user_delete_controller(id):
    return object.user_delete(id)