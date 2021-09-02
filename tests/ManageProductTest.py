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


class TestManageProduct(BaseCase):
    test_user_obj = TestUserLogin()

    token_login = test_user_obj.test_successful_login()

    def test_manage_product_create(self):
        payload = json.dumps({
            "sku_producto": "",
            "marca_producto": "",
            "unidad_medida_producto": "",
            "inventario_producto": "",
            "nombre_producto": "",
            "titulo_producto": "",
            "descripcion_larga": "",
            "url_imagen": "",
            "precio_unitario": "",
            "costo_impuesto": "",
            "tasa_impuesto": "",
            "estatus_producto": "",
            "producto_publicado": "",
            "volumetria_largo_producto": "",
            "volumetria_ancho_producto": "",
            "volumetria_alto_producto": "",
            "volumetria_peso_producto": "",
            "id_categoria_producto": "",
            "id_categoria_padre_producto": ""
        })

        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        response_create = self.app.post('/api/v1.0/manager/product/', data=payload, headers=header_request)

        # When
        product_response = json.loads(response_create.get_data(as_text=True))

        print("Response endpoint: ", product_response)

        # Then
        self.assertEqual(200, response_create.status_code)
        self.assertEqual(str, type(product_response["sku_producto"]))
        self.assertEqual(str, type(product_response["marca_producto"]))
        self.assertEqual(str, type(product_response["unidad_medida_producto"]))
        self.assertEqual(str, type(product_response["inventario_producto"]))
        self.assertEqual(str, type(product_response["nombre_producto"]))
        self.assertEqual(str, type(product_response["titulo_producto"]))
        self.assertEqual(str, type(product_response["descripcion_larga"]))
        self.assertEqual(str, type(product_response["url_imagen"]))
        self.assertEqual(str, type(product_response["precio_unitario"]))
        self.assertEqual(str, type(product_response["costo_impuesto"]))
        self.assertEqual(str, type(product_response["tasa_impuesto"]))
        self.assertEqual(str, type(product_response["estatus_producto"]))
        self.assertEqual(str, type(product_response["producto_publicado"]))
        self.assertEqual(str, type(product_response["volumetria_largo_producto"]))
        self.assertEqual(str, type(product_response["volumetria_ancho_producto"]))
        self.assertEqual(str, type(product_response["volumetria_alto_producto"]))
        self.assertEqual(str, type(product_response["volumetria_peso_producto"]))
        self.assertEqual(str, type(product_response["id_categoria_producto"]))
        self.assertEqual(str, type(product_response["id_categoria_padre_producto"]))
        self.assertEqual(str, type(product_response["cambio_realizado"]))
        self.assertEqual(str, type(product_response["contador_busqueda"]))
        self.assertEqual(str, type(product_response["fecha_alta"]))
        self.assertEqual(str, type(product_response["fecha_actualizacion"]))

    def test_manage_product_update(self):
        payload = json.dumps({
            "sku_producto": "",
            "marca_producto": "",
            "unidad_medida_producto": "",
            "inventario_producto": "",
            "nombre_producto": "",
            "titulo_producto": "",
            "descripcion_larga": "",
            "url_imagen": "",
            "precio_unitario": "",
            "costo_impuesto": "",
            "tasa_impuesto": "",
            "estatus_producto": "",
            "producto_publicado": "",
            "volumetria_largo_producto": "",
            "volumetria_ancho_producto": "",
            "volumetria_alto_producto": "",
            "volumetria_peso_producto": "",
            "id_categoria_producto": "",
            "id_categoria_padre_producto": ""
        })

        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        response_update = self.app.put('/api/v1.0/manager/product/', data=payload, headers=header_request)

        # When
        product_response = json.loads(response_update.get_data(as_text=True))

        print("Response endpoint: ", product_response)

        # Then
        self.assertEqual(200, response_update.status_code)
        self.assertEqual(str, type(product_response["sku_producto"]))
        self.assertEqual(str, type(product_response["marca_producto"]))
        self.assertEqual(str, type(product_response["unidad_medida_producto"]))
        self.assertEqual(str, type(product_response["inventario_producto"]))
        self.assertEqual(str, type(product_response["nombre_producto"]))
        self.assertEqual(str, type(product_response["titulo_producto"]))
        self.assertEqual(str, type(product_response["descripcion_larga"]))
        self.assertEqual(str, type(product_response["url_imagen"]))
        self.assertEqual(str, type(product_response["precio_unitario"]))
        self.assertEqual(str, type(product_response["costo_impuesto"]))
        self.assertEqual(str, type(product_response["tasa_impuesto"]))
        self.assertEqual(str, type(product_response["estatus_producto"]))
        self.assertEqual(str, type(product_response["producto_publicado"]))
        self.assertEqual(str, type(product_response["volumetria_largo_producto"]))
        self.assertEqual(str, type(product_response["volumetria_ancho_producto"]))
        self.assertEqual(str, type(product_response["volumetria_alto_producto"]))
        self.assertEqual(str, type(product_response["volumetria_peso_producto"]))
        self.assertEqual(str, type(product_response["id_categoria_producto"]))
        self.assertEqual(str, type(product_response["id_categoria_padre_producto"]))
        self.assertEqual(str, type(product_response["cambio_realizado"]))
        self.assertEqual(str, type(product_response["contador_busqueda"]))
        self.assertEqual(str, type(product_response["fecha_alta"]))
        self.assertEqual(str, type(product_response["fecha_actualizacion"]))

    def test_manage_product_delete(self):
        payload = json.dumps({
            "sku_producto": "",
            "marca_producto": "",
            "unidad_medida_producto": "",
            "inventario_producto": "",
            "nombre_producto": "",
            "titulo_producto": "",
            "descripcion_larga": "",
            "url_imagen": "",
            "precio_unitario": "",
            "costo_impuesto": "",
            "tasa_impuesto": "",
            "estatus_producto": "",
            "producto_publicado": "",
            "volumetria_largo_producto": "",
            "volumetria_ancho_producto": "",
            "volumetria_alto_producto": "",
            "volumetria_peso_producto": "",
            "id_categoria_producto": "",
            "id_categoria_padre_producto": ""
        })

        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        response_delete = self.app.delete('/api/v1.0/manager/product/', data=payload, headers=header_request)

        # When
        product_response = json.loads(response_delete.get_data(as_text=True))

        print("Response endpoint: ", product_response)

        # Then
        self.assertEqual(200, response_delete.status_code)
        self.assertEqual(str, type(product_response["sku_producto"]))
        self.assertEqual(str, type(product_response["marca_producto"]))
        self.assertEqual(str, type(product_response["unidad_medida_producto"]))
        self.assertEqual(str, type(product_response["inventario_producto"]))
        self.assertEqual(str, type(product_response["nombre_producto"]))
        self.assertEqual(str, type(product_response["titulo_producto"]))
        self.assertEqual(str, type(product_response["descripcion_larga"]))
        self.assertEqual(str, type(product_response["url_imagen"]))
        self.assertEqual(str, type(product_response["precio_unitario"]))
        self.assertEqual(str, type(product_response["costo_impuesto"]))
        self.assertEqual(str, type(product_response["tasa_impuesto"]))
        self.assertEqual(str, type(product_response["estatus_producto"]))
        self.assertEqual(str, type(product_response["producto_publicado"]))
        self.assertEqual(str, type(product_response["volumetria_largo_producto"]))
        self.assertEqual(str, type(product_response["volumetria_ancho_producto"]))
        self.assertEqual(str, type(product_response["volumetria_alto_producto"]))
        self.assertEqual(str, type(product_response["volumetria_peso_producto"]))
        self.assertEqual(str, type(product_response["id_categoria_producto"]))
        self.assertEqual(str, type(product_response["id_categoria_padre_producto"]))
        self.assertEqual(str, type(product_response["cambio_realizado"]))
        self.assertEqual(str, type(product_response["contador_busqueda"]))
        self.assertEqual(str, type(product_response["fecha_alta"]))
        self.assertEqual(str, type(product_response["fecha_actualizacion"]))

    def test_manage_product_get_all(self):
        header_request = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(self.token_login)
        }

        # When
        response = self.app.get('/api/v1.0/manager/product/', headers=header_request)

        product_response = json.loads(response.get_data(as_text=True))

        # Then
        self.assertEqual(str, type(product_response['Product']["sku_producto"]))
        self.assertEqual(str, type(product_response['Product']["marca_producto"]))
        self.assertEqual(str, type(product_response['Product']["unidad_medida_producto"]))
        self.assertEqual(str, type(product_response['Product']["inventario_producto"]))
        self.assertEqual(str, type(product_response['Product']["nombre_producto"]))
        self.assertEqual(str, type(product_response['Product']["titulo_producto"]))
        self.assertEqual(str, type(product_response['Product']["descripcion_larga"]))
        self.assertEqual(str, type(product_response['Product']["url_imagen"]))
        self.assertEqual(str, type(product_response['Product']["precio_unitario"]))
        self.assertEqual(str, type(product_response['Product']["costo_impuesto"]))
        self.assertEqual(str, type(product_response['Product']["tasa_impuesto"]))
        self.assertEqual(str, type(product_response['Product']["estatus_producto"]))
        self.assertEqual(str, type(product_response['Product']["producto_publicado"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_largo_producto"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_ancho_producto"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_alto_producto"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_peso_producto"]))
        self.assertEqual(str, type(product_response['Product']["id_categoria_producto"]))
        self.assertEqual(str, type(product_response['Product']["id_categoria_padre_producto"]))
        self.assertEqual(str, type(product_response['Product']["cambio_realizado"]))
        self.assertEqual(str, type(product_response['Product']["contador_busqueda"]))
        self.assertEqual(str, type(product_response['Product']["fecha_alta"]))
        self.assertEqual(str, type(product_response['Product']["fecha_actualizacion"]))
        self.assertEqual(200, response.status_code)

    def test_search_product_filter(self):
        payload = json.dumps({
            "sku_producto": "",
            "marca_producto": "",
            "nombre_producto": "",
            "titulo_producto": "",
            "estatus_producto": ""
        })

        # When
        response = self.app.get('/api/v1.0/manager/product/filter',
                                headers={"Content-Type": "application/json"},
                                data=payload)

        product_response = json.loads(response.get_data(as_text=True))

        # Then
        self.assertEqual(str, type(product_response['Product']["sku_producto"]))
        self.assertEqual(str, type(product_response['Product']["marca_producto"]))
        self.assertEqual(str, type(product_response['Product']["unidad_medida_producto"]))
        self.assertEqual(str, type(product_response['Product']["inventario_producto"]))
        self.assertEqual(str, type(product_response['Product']["nombre_producto"]))
        self.assertEqual(str, type(product_response['Product']["titulo_producto"]))
        self.assertEqual(str, type(product_response['Product']["descripcion_larga"]))
        self.assertEqual(str, type(product_response['Product']["url_imagen"]))
        self.assertEqual(str, type(product_response['Product']["precio_unitario"]))
        self.assertEqual(str, type(product_response['Product']["costo_impuesto"]))
        self.assertEqual(str, type(product_response['Product']["tasa_impuesto"]))
        self.assertEqual(str, type(product_response['Product']["estatus_producto"]))
        self.assertEqual(str, type(product_response['Product']["producto_publicado"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_largo_producto"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_ancho_producto"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_alto_producto"]))
        self.assertEqual(str, type(product_response['Product']["volumetria_peso_producto"]))
        self.assertEqual(str, type(product_response['Product']["id_categoria_producto"]))
        self.assertEqual(str, type(product_response['Product']["id_categoria_padre_producto"]))
        self.assertEqual(str, type(product_response['Product']["cambio_realizado"]))
        self.assertEqual(str, type(product_response['Product']["contador_busqueda"]))
        self.assertEqual(str, type(product_response['Product']["fecha_alta"]))
        self.assertEqual(str, type(product_response['Product']["fecha_actualizacion"]))
        self.assertEqual(200, response.status_code)
