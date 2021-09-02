# -*- coding: utf-8 -*-
"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.I02.1 ($Rev: 1 $)"

import os
import unittest
import json
from tests.BaseCase import BaseCase
from tests.UserAuthenticationTest import TestUserLogin


class TestManageCategory(BaseCase):
    test_user_obj = TestUserLogin()

    token_login = test_user_obj.test_successful_login()

    def test_manage_category_create(self):

        payload = json.dumps({
            "nombre_categoria": "Gaming",
            "descrippcion_corta_categoria": "Articulos perifericos Gamer",
            "estatus_categoria": "activo"
        })

        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        response_create = self.app.post('/api/v1.0/manager/product/category/', data=payload, headers=header_request)

        # When
        category_response = json.loads(response_create.get_data(as_text=True))

        print("Response endpoint: ", category_response)

        # Then
        self.assertEqual(200, response_create.status_code)
        self.assertEqual(str, type(category_response["id_categoria"]))
        self.assertEqual(str, type(category_response["nombre_categoria"]))
        self.assertEqual(str, type(category_response["descripcion_categoria"]))
        self.assertEqual(str, type(category_response["estatus_categoria"]))

    def test_manage_category_update(self):
        payload = json.dumps({
            "nombre_categoria": "Perifericos Gaming",
            "descrippcion_corta_categoria": "Articulos perifericos Gamer",
            "estatus_categoria": "activo"
        })

        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        response_update = self.app.put('/api/v1.0/manager/product/category/', data=payload, headers=header_request)

        # When
        category_response = json.loads(response_update.get_data(as_text=True))

        print("Response endpoint: ", category_response)

        # Then
        self.assertEqual(200, response_update.status_code)
        self.assertEqual(str, type(category_response["id_categoria"]))
        self.assertEqual(str, type(category_response["nombre_categoria"]))
        self.assertEqual(str, type(category_response["descripcion_categoria"]))
        self.assertEqual(str, type(category_response["estatus_categoria"]))
        self.assertEqual(str, type(category_response["creation_date"]))
        self.assertEqual(str, type(category_response["last_update_date"]))

    def test_manage_category_delete(self):
        payload = json.dumps({
            "nombre_categoria": "Perifericos Gaming",
            "descrippcion_corta_categoria": "Articulos perifericos Gamer",
            "estatus_categoria": "activo"
        })

        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        response_delete = self.app.delete('/api/v1.0/manager/product/category/', data=payload, headers=header_request)

        # When
        category_response = json.loads(response_delete.get_data(as_text=True))

        print("Response endpoint: ", category_response)

        # Then
        self.assertEqual(200, response_delete.status_code)
        self.assertEqual(str, type(category_response["id_categoria"]))
        self.assertEqual(str, type(category_response["nombre_categoria"]))
        self.assertEqual(str, type(category_response["descripcion_categoria"]))
        self.assertEqual(str, type(category_response["estatus_categoria"]))
        self.assertEqual(str, type(category_response["creation_date"]))
        self.assertEqual(str, type(category_response["last_update_date"]))

    def test_manage_category_get_all(self):
        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        # When
        response = self.app.get('/api/v1.0/manager/product/category/', headers=header_request)

        category_response = json.loads(response.get_data(as_text=True))

        # Then
        self.assertEqual(str, type(category_response['Categoria']["id_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["nombre_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["descripcion_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["estatus_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["creation_date"]))
        self.assertEqual(str, type(category_response['Categoria']["last_update_date"]))
        self.assertEqual(200, response.status_code)

    def test_search_category_filter(self):
        payload = json.dumps({
            "nombre_categoria": "Gaming",
            "estatus_categoria": "activo"
        })

        # When
        response = self.app.get('/api/v1.0/manager/product/category/filter',
                                headers={"Content-Type": "application/json"},
                                data=payload)

        category_response = json.loads(response.get_data(as_text=True))

        # Then
        self.assertEqual(str, type(category_response['Categoria']["id_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["nombre_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["descripcion_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["estatus_categoria"]))
        self.assertEqual(str, type(category_response['Categoria']["creation_date"]))
        self.assertEqual(str, type(category_response['Categoria']["last_update_date"]))
        self.assertEqual(200, response.status_code)
