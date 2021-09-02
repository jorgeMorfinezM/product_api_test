# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.H05.1 ($Rev: 2 $)"

from flask import Blueprint, json, request
from flask_jwt_extended import JWTManager, jwt_required
from db_controller.database_backend import *
from .CategoryModel import CategoryModel
from handler_controller.ResponsesHandler import ResponsesHandler as HandlerResponse
from handler_controller.messages import SuccessMsg, ErrorMsg
from logger_controller.logger_control import *
from utilities.Utility import *

cfg_app = get_config_settings_app()
category_api = Blueprint('category_api', __name__)
jwt = JWTManager(category_api)
logger = configure_logger('ws')


@category_api.route('/', methods=['POST', 'PUT', 'GET', 'DELETE'])
@jwt_required
def endpoint_manage_category_data():
    conn_db, session_db = init_db_connection()

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return HandlerResponse.request_unauthorized(ErrorMsg.ERROR_REQUEST_UNAUTHORIZED, auth)
    else:

        if request.method == 'POST':

            data = request.get_json(force=True)

            category_model = CategoryModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Category to Manage on DB: %s', str(data))

            category_response = category_model.insert_data(session_db, data)

            logger.info('Data Category to Register on DB: %s', str(data))

            if not category_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, category_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_CREATED_RECORD, category_response)

        elif request.method == 'PUT':

            data = request.get_json(force=True)

            category_model = CategoryModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Category to Manage on DB: %s', str(data))

            category_response = category_model.update_data(session_db, data)

            logger.info('Data Driver to Update on DB: %s', str(data))

            if not category_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, category_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_UPDATED_RECORD, category_response)

        elif request.method == 'DELETE':

            data = request.get_json(force=True)

            category_model = CategoryModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Category to Manage on DB: %s', str(data))

            category_response = category_model.category_inactivate(session_db, data)

            logger.info('Data Driver to Update on DB: %s', str(data))

            if not category_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, category_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_DELETED_RECORD, category_response)

        elif request.method == 'GET':
            data = dict()
            states_on_db = None

            data['offset'] = request.args.get('offset', 1)
            data['limit'] = request.args.get('limit', 10)

            category_model = CategoryModel(data)

            states_on_db = category_model.get_all_categories(session_db, data)

            if not bool(states_on_db) or not states_on_db or "[]" == states_on_db:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, states_on_db)

            return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, states_on_db)

        else:
            return HandlerResponse.request_not_found(ErrorMsg.ERROR_METHOD_NOT_ALLOWED)


@category_api.route('/filter', methods=['GET'])
def get_looking_for_category():
    conn_db, session_db = init_db_connection()

    data = dict()

    query_string = request.query_string.decode('utf-8')

    if request.method == 'GET':

        state_on_db = None

        filter_spec = []

        data['offset'] = request.args.get('offset', 1)
        data['limit'] = request.args.get('limit', 10)

        if 'nombre_categoria' in query_string:
            category_name = request.args.get('nombre_categoria')

            data['nombre_categoria'] = category_name

            filter_spec.append({'field': 'category_name', 'op': 'ilike', 'value': category_name})
            # filter_spec.append({'field': 'nombre_estado', 'op': '==', 'value': category_name})

        if 'estatus_categoria' in query_string:
            category_status = request.args.get('estatus_categoria')

            data['estatus_categoria'] = category_status

            filter_spec.append({'field': 'category_status', 'op': '==', 'value': category_status})

        category_model = CategoryModel(data)

        state_on_db = category_model.get_category_by_filters(session_db, data, filter_spec)

        if not bool(state_on_db) or not state_on_db or "[]" == state_on_db:
            return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, state_on_db)

        return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, state_on_db)

    else:
        return HandlerResponse.request_not_found(ErrorMsg.ERROR_METHOD_NOT_ALLOWED)

