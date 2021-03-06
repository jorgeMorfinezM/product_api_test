# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.H28.1 ($Rev: 1 $)"

import re
import time
import threading
from flask import Blueprint, json, request, render_template, redirect
from flask_jwt_extended import jwt_required
from db_controller.database_backend import *
from .UsersAuthModel import UsersAuthModel
from handler_controller.ResponsesHandler import ResponsesHandler as HandlerResponse
from handler_controller.messages import SuccessMsg, ErrorMsg
from auth_controller.api_authentication import *
from logger_controller.logger_control import *
from utilities.Utility import *
from datetime import datetime

cfg_app = get_config_settings_app()
authorization_api = Blueprint('authorization_api', __name__)
# jwt = JWTManager(bancos_api)
logger = configure_logger('ws')


# Se inicializa la App con un hilo para evitar problemas de ejecución
# (Falta validacion para cuando ya exista hilo corriendo)
def activate_job():
    def run_job():
        while True:
            time.sleep(2)

    thread = threading.Thread(target=run_job)
    thread.start()


# Contiene la llamada al HTML que soporta la documentacion de la API,
# sus metodos, y endpoints con los modelos de datos I/O
# @authorization_api.before_app_first_request(activate_job())
@authorization_api.route('/doc')
def main():
    return render_template('api_manage_product.html')


@authorization_api.route('/logout/')
def logout():
    return redirect('/')


@authorization_api.route('/login/', methods=['POST'])
def get_authentication():
    conn_db, session_db = init_db_connection()

    data = dict()
    json_token = dict()

    if request.method == 'POST':
        data = request.get_json(force=True)

        if not data or str(data) is None:
            return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

        user_name = data['username']
        password = data['password']
        is_super_user = data['is_superuser']

        regex_username = r"^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$"

        regex_passwd = r"^[(A-Za-z0-9\_\-\.\$\#\&\*)(A-Za-z0-9\_\-\.\$\#\&\*)]+"

        match_username = re.match(regex_username, user_name, re.M | re.I)

        match_passwd = re.match(regex_passwd, password, re.M | re.I)

        if match_username and match_passwd and bool(is_super_user):

            password = user_name + '_' + password + '_' + cfg_app.api_key

            data['password'] = password

            json_token = user_registration(session_db, data)

        else:
            return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

        logger.info('Data User to Register on DB: %s', str(data))

        if not json_token:
            return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, json_token)

        return HandlerResponse.response_resource_created(SuccessMsg.MSG_CREATED_RECORD, json_token)

    else:
        return HandlerResponse.request_not_found(ErrorMsg.ERROR_REQUEST_NOT_FOUND)


@authorization_api('/', methods=['PUT', 'DELETE'])
@jwt_required
def manage_user_data():
    conn_db, session_db = init_db_connection()

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return HandlerResponse.request_unauthorized(ErrorMsg.ERROR_REQUEST_UNAUTHORIZED, auth)
    else:
        data = dict()

        if request.method == 'PUT':

            data = request.get_json(force=True)

            is_super_user = data['is_superuser']

            user_model = UsersAuthModel(data)

            if not data or str(data) is None and (bool(is_super_user) is False):
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json User to Manage on DB: %s', str(data))

            user_response = user_model.user_update(session_db, data)

            logger.info('Data User to Update on DB: %s', str(data))

            if not user_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, user_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_UPDATED_RECORD, user_response)

        elif request.method == 'DELETE':

            data = request.get_json(force=True)

            user_model = UsersAuthModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Driver to Manage on DB: %s', str(data))

            user_response = user_model.user_inactivate(session_db, data)

            logger.info('Data User to Update on DB: %s', str(data))

            if not user_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, user_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_DELETED_RECORD, user_response)

        else:
            return HandlerResponse.request_not_found(ErrorMsg.ERROR_REQUEST_NOT_FOUND)


@authorization_api.route('/list', methods=['GET'])
@jwt_required
def get_list_users_auth():
    conn_db, session_db = init_db_connection()

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return HandlerResponse.request_unauthorized(ErrorMsg.ERROR_REQUEST_UNAUTHORIZED, auth)
    else:
        data = dict()
        json_token = dict()

        if request.method == 'GET':
            # To GET ALL Data of the Users:

            data['offset'] = request.args.get('offset', 1)
            data['limit'] = request.args.get('limit', 10)

            users_on_db = None

            user_model = UsersAuthModel(data)

            users_on_db = user_model.get_all_users(session_db, data)

            if not bool(users_on_db) or not users_on_db or "[]" == users_on_db:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, users_on_db)

            return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, users_on_db)

        else:
            return HandlerResponse.request_not_found(ErrorMsg.ERROR_REQUEST_NOT_FOUND)
