# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ Blueprint to View endpoints for Product Model 
                  catalog to manage and search data """
__version__ = "1.21.H05.1 ($Rev: 2 $)"

from flask import Blueprint, json, request
from flask_jwt_extended import JWTManager, jwt_required
from db_controller.database_backend import *
from .ProductModel import ProductModel
from apps.api_authentication.UsersAuthModel import UsersAuthModel
from handler_controller.ResponsesHandler import ResponsesHandler as HandlerResponse
from handler_controller.messages import SuccessMsg, ErrorMsg
from logger_controller.logger_control import *
from utilities.Utility import *
from utilities.send_email_notification import *

cfg_app = get_config_settings_app()
product_api = Blueprint('product_api', __name__)
jwt = JWTManager(product_api)
logger = configure_logger('ws')


@product_api.route('/', methods=['POST', 'PUT', 'GET', 'DELETE'])
@jwt_required
def endpoint_manage_state_data():
    conn_db, session_db = init_db_connection()

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return HandlerResponse.request_unauthorized(ErrorMsg.ERROR_REQUEST_UNAUTHORIZED, auth)
    else:

        if request.method == 'POST':

            data = request.get_json(force=True)

            product_model = ProductModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Product to Manage on DB: %s', str(data))

            product_response = product_model.insert_data(session_db, data)

            logger.info('Data Product to Register on DB: %s', str(data))

            if not product_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, product_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_CREATED_RECORD, product_response)

        elif request.method == 'PUT':

            data = request.get_json(force=True)

            product_model = ProductModel(data)

            email_recipients = []

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Product to Manage on DB: %s', str(data))

            product_response = product_model.update_data(session_db, data)

            logger.info('Data Driver to Update on DB: %s', str(data))

            if not product_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, product_response)

            email_recipients = UsersAuthModel.get_users_recipients(session_db)

            cfg_app.email_recipients = email_recipients

            # Notifying by email about the product change to all the users
            email_notifier(data.get('sku_producto'), data.get('nombre_producto'), product_response, email_recipients)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_UPDATED_RECORD, product_response)

        elif request.method == 'DELETE':

            data = request.get_json(force=True)

            product_model = ProductModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Product to Manage on DB: %s', str(data))

            product_response = product_model.product_inactivate(session_db, data)

            logger.info('Data Driver to Update on DB: %s', str(data))

            if not product_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, product_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_DELETED_RECORD, product_response)

        elif request.method == 'GET':
            data = dict()
            product_on_db = None

            data['offset'] = request.args.get('offset', 1)
            data['limit'] = request.args.get('limit', 10)

            product_model = ProductModel(data)

            product_on_db = product_model.get_all_products(session_db, data)

            if not bool(product_on_db) or not product_on_db or "[]" == product_on_db:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, product_on_db)

            return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, product_on_db)

        else:
            return HandlerResponse.request_not_found(ErrorMsg.ERROR_METHOD_NOT_ALLOWED)


@product_api.route('/filter', methods=['GET'])
def get_looking_for_state():
    conn_db, session_db = init_db_connection()

    data = dict()

    query_string = request.query_string.decode('utf-8')

    if request.method == 'GET':

        product_on_db = None

        filter_spec = []

        data['offset'] = request.args.get('offset', 1)
        data['limit'] = request.args.get('limit', 10)

        if 'sku_producto' in query_string:
            product_sku = request.args.get('sku_producto')

            data['sku_producto'] = product_sku

            filter_spec.append({'field': 'product_sku', 'op': '==', 'value': product_sku})
            # filter_spec.append({'field': 'product_sku', 'op': 'ilike', 'value': product_sku})

        if 'marca_producto' in query_string:
            product_brand = request.args.get('marca_producto')

            data['marca_producto'] = product_brand

            filter_spec.append({'field': 'product_brand', 'op': 'ilike', 'value': product_brand})

        if 'nombre_producto' in query_string:
            product_name = request.args.get('nombre_producto')

            data['nombre_producto'] = product_name

            filter_spec.append({'field': 'product_name', 'op': 'ilike', 'value': product_name})

        if 'titulo_producto' in query_string:
            product_title = request.args.get('titulo_producto')

            data['titulo_producto'] = product_title

            filter_spec.append({'field': 'product_title', 'op': 'ilike', 'value': product_title})

        if 'estatus_producto' in query_string:
            product_status = request.args.get('estatus_producto')

            data['estatus_producto'] = product_status

            filter_spec.append({'field': 'product_status', 'op': '==', 'value': product_status})

        product_model = ProductModel(data)

        product_on_db = product_model.get_products_by_filters(session_db, data, filter_spec)

        if not bool(product_on_db) or not product_on_db or "[]" == product_on_db:
            return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, product_on_db)

        return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, product_on_db)

    else:
        return HandlerResponse.request_not_found(ErrorMsg.ERROR_METHOD_NOT_ALLOWED)

