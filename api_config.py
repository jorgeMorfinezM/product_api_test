# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ API Configuration script with 
                  dependency injection"""
__version__ = "1.21.H28.1 ($Rev: 1 $)"

import threading
import time
from flask import Flask
from flask_jwt_extended import JWTManager
from apps.api_authentication.view_endpoints import authorization_api
from apps.category.view_endpoints import category_api
from apps.product.view_endpoints import product_api
from utilities.Utility import *

cfg_db = get_config_settings_db()
cfg_app = get_config_settings_app()


def create_app():
    app_api = Flask(__name__, static_url_path='/static')

    app_api.config['JWT_SECRET_KEY'] = cfg_app.api_key.__str__()
    app_api.config['JWT_BLACKLIST_ENABLED'] = cfg_app.jwt_blacklist_enabled
    app_api.config['JWT_BLACKLIST_TOKEN_CHECKS'] = cfg_app.jwt_blacklist_token_check
    app_api.config['JWT_ERROR_MESSAGE_KEY'] = cfg_app.jwt_error_message.__str__()
    app_api.config['JWT_ACCESS_TOKEN_EXPIRES'] = cfg_app.jwt_access_token_expires
    app_api.config['PROPAGATE_EXCEPTIONS'] = cfg_app.jwt_propagate_exceptions

    if not 'development' == cfg_app.flask_api_env:
        app_api.config['SQLALCHEMY_DATABASE_URI'] = cfg_db.Production.SQLALCHEMY_DATABASE_URI.__str__()

    app_api.config['SQLALCHEMY_DATABASE_URI'] = cfg_db.Development.SQLALCHEMY_DATABASE_URI.__str__()

    # USER
    app_api.register_blueprint(authorization_api, url_prefix='/api/v' + cfg_app.api_version + '/manager/user/')

    # PRODUCT
    app_api.register_blueprint(product_api, url_prefix='/api/v' + cfg_app.api_version + '/manager/product')

    # CATEGORY
    app_api.register_blueprint(category_api, url_prefix='/api/v' + cfg_app.api_version + '/manager/product/category')

    jwt_manager = JWTManager(app_api)

    jwt_manager.init_app(app_api)

    return app_api
