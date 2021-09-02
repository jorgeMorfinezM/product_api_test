# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later


PostgreSQL DB backend.

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
    About the Vehicle data on the database to generate CRUD operations from endpoint of the API:
    - Insert data
    - Update data
    - Delete data
    - Search data

"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.H05.1 ($Rev: 2 $)"

import json
import logging
from apps.category.CategoryModel import CategoryModel
from sqlalchemy_filters import apply_filters
from sqlalchemy import Column, Numeric, Integer, Float, String, Date, Time, Boolean, Sequence
from db_controller.database_backend import *
from db_controller import mvc_exceptions as mvc_exc
from utilities.Utility import *

cfg_db = get_config_settings_db()

PRODUCT_ID_SEQ = Sequence('product_seq')  # define sequence explicitly


class ProductModel(Base):
    r"""
    Class to instance the data of MunicipioModel on the database.
    Transactions:
     - Insert: Add data to the database if not exists.
     - Select:
    """

    __tablename__ = 'product'

    product_id = Column('id_product', Integer, PRODUCT_ID_SEQ,
                        primary_key=True, server_default=PRODUCT_ID_SEQ.next_value())
    product_sku = Column('sku_product', String, nullable=False, index=True)
    product_brand = Column('brand_product', String, nullable=False, index=True)
    unit_of_measure = Column('uom_product', String, nullable=False, index=True)
    product_stock = Column('stock_product', Integer, nullable=False, index=True)
    product_name = Column('name_product', String, nullable=False, index=True)
    product_title = Column('title_product', String, nullable=False, index=True)
    product_long_description = Column('description_product', String, nullable=False)
    product_photo = Column('photo_product', String, nullable=False)
    product_price = Column('price_product', Float, nullable=False, index=True)
    product_tax = Column('tax_product', Float, nullable=False)
    product_tax_rate = Column('tax_rate_product', Float, nullable=False)
    product_status = Column('status_product', String, nullable=False, index=True)
    product_published = Column('published_product', Boolean, nullable=False, index=True)
    product_length = Column('length_product', Float, nullable=False)
    product_width = Column('width_product', Float, nullable=False)
    product_height = Column('height_product', Float, nullable=False)
    product_weight = Column('weight_product', Float, nullable=False)
    # Flag to notify id user change data on product (On PUT or DELETE)
    change_made = Column('change_made', Boolean, nullable=False, index=True)
    # Number of times of anonymous user was queried product
    product_queried_count = Column('product_queried_count', Integer, nullable=False, index=True)
    creation_date = Column('creation_date', Date, nullable=False)
    last_update_date = Column('last_update_date', Date, nullable=True)

    category_id = Column(
        'product_id_category',
        Integer,
        ForeignKey('CategoryModel.category_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
        unique=True
        # no need to add index=True, all FKs have indexes
    )

    id_category = relationship(CategoryModel,
                               backref=__tablename__)

    parent_category_id = Column( 'product_id_parent_cat', Integer, nullable=True)

    def __init__(self, data_product):
        self.product_sku = data_product.get('sku_producto')
        self.product_brand = data_product.get('marca_producto')
        self.unit_of_measure = data_product.get('unidad_medida_producto')
        self.product_stock = data_product.get('inventario_producto')
        self.product_name = data_product.get('nombre_producto')
        self.product_title = data_product.get('titulo_producto')
        self.product_long_description = data_product.get('descripcion_larga')
        self.product_photo = data_product.get('url_imagen')
        self.product_price = decimal_formatting(data_product.get('precio_unitario'))
        self.product_tax = decimal_formatting(data_product.get('costo_impuesto'))
        self.product_tax_rate = decimal_formatting(data_product.get('tasa_impuesto'))
        self.product_status = data_product.get('estatus_producto')
        self.product_published = data_product.get('producto_publicado')
        self.product_length = decimal_formatting(data_product.get('volumetria_largo_producto'))
        self.product_width = decimal_formatting(data_product.get('volumetria_ancho_producto'))
        self.product_height = decimal_formatting(data_product.get('volumetria_alto_producto'))
        self.product_weight = decimal_formatting(data_product.get('volumetria_peso_producto'))
        self.category_id = data_product.get('id_categoria_producto')
        self.parent_category_id = data_product.get('id_categoria_padre_producto')

    def check_if_row_exists(self, session, data):
        """
        Validate if row exists on database from dictionary data

        :param session: Session database object
        :param data: Dictionary with data to make validation function
        :return: row_exists: Object with boolean response from db
        """

        row_exists = None
        id_product = 0

        try:
            # for example to check if the insert on db is correct
            row_product = self.get_product_id(session, data)

            if row_product is not None:
                id_product = row_product.product_id
            else:
                id_product = 0

            logger.info('Product Row object in DB: %s', str(id_product))

            row_exists = session.query(ProductModel).filter(ProductModel.product_id == id_product).scalar()

            logger.info('Row to data: {}, Exists: %s'.format(data), str(row_exists))

        except SQLAlchemyError as exc:
            row_exists = None

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.IntegrityError(
                'Row not stored in "{}". IntegrityError: {}'.format(data.get('sku_producto'),
                                                                    str(str(exc.args) + ':' + str(exc.code)))
            )
        finally:
            session.close()

        return row_exists

    def insert_data(self, session, data):
        """
        Function to insert/create new row on database

        :param session: Session database object
        :param data: Dictionary to insert new the data containing on the db
        :return: endpoint_response
        """

        endpoint_response = None

        if not self.check_if_row_exists(session, data):

            try:

                self.creation_date = get_current_date(session)

                data['creation_date'] = self.creation_date

                new_row = ProductModel(data)

                logger.info('New Row Product: %s', str(new_row.product_sku))

                session.add(new_row)

                row_product = self.get_product_id(session, data)

                logger.info('Product ID Inserted: %s', str(row_product.product_id))

                session.flush()

                data['id_product'] = row_product.product_id

                # check insert correct
                row_inserted = self.get_one_product(session, data)

                logger.info('Data Product inserted: %s, Original Data: {}'.format(data), str(row_inserted))

                if row_inserted:
                    endpoint_response = json.dumps({
                        "sku_producto": row_inserted.product_sku,
                        "marca_producto": row_inserted.product_brand,
                        "unidad_medida_producto": row_inserted.unit_of_measure,
                        "inventario_producto": row_inserted.product_stock,
                        "nombre_producto": row_inserted.product_name,
                        "titulo_producto": row_inserted.product_title,
                        "descripcion_larga": row_inserted.product_long_description,
                        "url_imagen": row_inserted.product_photo,
                        "precio_unitario": str(row_inserted.product_price),
                        "costo_impuesto": str(row_inserted.product_tax),
                        "tasa_impuesto": str(row_inserted.product_tax_rate),
                        "estatus_producto": row_inserted.product_status,
                        "producto_publicado": row_inserted.product_published,
                        "volumetria_largo_producto": str(row_inserted.product_length),
                        "volumetria_ancho_producto": str(row_inserted.product_width),
                        "volumetria_alto_producto": str(row_inserted.product_height),
                        "volumetria_peso_producto": str(row_inserted.product_weight),
                        "id_categoria_producto": str(row_inserted.category_id),
                        "id_categoria_padre_producto": str(row_inserted.parent_category_id),
                        "fecha_alta": str(row_inserted.creation_date)
                    })

            except SQLAlchemyError as exc:
                endpoint_response = None
                session.rollback()

                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('sku_producto'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    # Transaction to update Product's data on db to authenticate - PUT
    def update_data(self, session, data):
        r"""
        Transaction to update data by a user authenticated on the API correctly.

        :param session: The product object db session.
        :param data: The dictionary json request on the API to update data values.
        """

        endpoint_response = None

        if self.check_if_row_exists(session, data):

            try:

                row_product = self.get_product_id(session, data)

                logger.info('Product ID Updated: %s', str(row_product.product_id))

                data['id_product'] = row_product.product_id

                if row_product is not None:
                    id_product = row_product.product_id
                else:
                    id_product = 0

                self.last_update_date = get_current_date(session)

                data['last_update_date'] = self.last_update_date

                # update row to database
                session.query(ProductModel).filter(ProductModel.product_id == id_product). \
                    update({"product_sku": data.get('sku_producto'),
                            "product_brand": data.get('marca_producto'),
                            "unit_of_measure": data.get('unidad_medida_producto'),
                            "product_stock": data.get('inventario_producto'),
                            "product_name": data.get('unidad_medida_producto'),
                            "product_title": data.get('unidad_medida_producto'),
                            "product_long_description": data.get('unidad_medida_producto'),
                            "product_photo": data.get('unidad_medida_producto'),
                            "product_price": data.get('unidad_medida_producto'),
                            "product_tax": data.get('unidad_medida_producto'),
                            "product_tax_rate": data.get('unidad_medida_producto'),
                            "product_status": data.get('unidad_medida_producto'),
                            "product_published": data.get('unidad_medida_producto'),
                            "product_length": data.get('unidad_medida_producto'),
                            "product_width": data.get('unidad_medida_producto'),
                            "product_height": data.get('unidad_medida_producto'),
                            "product_weight": data.get('unidad_medida_producto'),
                            "category_id": data.get('unidad_medida_producto'),
                            "parent_category_id": data.get('unidad_medida_producto'),
                            "change_made": "True",
                            "last_update_date": data.get('last_update_date')},
                           synchronize_session='fetch')

                session.flush()

                # check update correct
                row_updated = self.get_one_product(session, data)

                logger.info('Data Product updated: %s, Original Data: {}'.format(data), str(row_updated))

                if row_updated:
                    logger.info('Data Product updated')

                    endpoint_response = json.dumps({
                        "sku_producto": row_updated.product_sku,
                        "marca_producto": row_updated.product_brand,
                        "unidad_medida_producto": row_updated.unit_of_measure,
                        "inventario_producto": row_updated.product_stock,
                        "nombre_producto": row_updated.product_name,
                        "titulo_producto": row_updated.product_title,
                        "descripcion_larga": row_updated.product_long_description,
                        "url_imagen": row_updated.product_photo,
                        "precio_unitario": str(row_updated.product_price),
                        "costo_impuesto": str(row_updated.product_tax),
                        "tasa_impuesto": str(row_updated.product_tax_rate),
                        "estatus_producto": row_updated.product_status,
                        "producto_publicado": row_updated.product_published,
                        "volumetria_largo_producto": str(row_updated.product_length),
                        "volumetria_ancho_producto": str(row_updated.product_width),
                        "volumetria_alto_producto": str(row_updated.product_height),
                        "volumetria_peso_producto": str(row_updated.product_weight),
                        "id_categoria_producto": str(row_updated.category_id),
                        "id_categoria_padre_producto": str(row_updated.parent_category_id),
                        "cambio_realizado": bool(row_updated.change_made),
                        "fecha_alta": str(row_updated.creation_date),
                        "fecha_actualizacion": str(row_updated.last_update_date)
                    })

            except SQLAlchemyError as exc:
                session.rollback()
                endpoint_response = None

                logger.exception('An exception was occurred while execute transactions: %s',
                                 str(str(exc.args) + ':' +
                                     str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('sku_producto'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    # Transaction to delete Product's data on db - DELETE
    def product_inactivate(self, session, data):
        r"""
        Transaction to inactivate Product data on the API correctly.

        :param session: The database object session connect.
        :param data: The data dictionary to inactivate register on the API.
        """

        endpoint_response = None

        if self.check_if_row_exists(session, data):

            try:

                row_product = self.get_product_id(session, data)

                logger.info('Product ID Inactivated: %s', str(row_product.product_id))

                data['id_product'] = row_product.product_id

                if row_product is not None:
                    id_product = row_product.product_id
                else:
                    id_product = 0

                self.last_update_date = get_current_date(session)

                data['last_update_date'] = self.last_update_date

                # update row to database
                session.query(ProductModel).filter(ProductModel.product_id == id_product). \
                    filter(ProductModel.product_status == "activo"). \
                    update({"product_status": "inactivo",
                            "last_update_date": data.get('last_update_date')},
                           synchronize_session='fetch')

                session.flush()

                # check delete correct
                row_deleted = self.get_one_product(session, data)

                logger.info('Data Deleted: %s', str(row_deleted))

                if row_deleted:
                    logger.info('Data Product inactivated')

                    endpoint_response = json.dumps({
                        "sku_producto": row_deleted.product_sku,
                        "marca_producto": row_deleted.product_brand,
                        "unidad_medida_producto": row_deleted.unit_of_measure,
                        "inventario_producto": row_deleted.product_stock,
                        "nombre_producto": row_deleted.product_name,
                        "titulo_producto": row_deleted.product_title,
                        "descripcion_larga": row_deleted.product_long_description,
                        "url_imagen": row_deleted.product_photo,
                        "precio_unitario": str(row_deleted.product_price),
                        "costo_impuesto": str(row_deleted.product_tax),
                        "tasa_impuesto": str(row_deleted.product_tax_rate),
                        "estatus_producto": row_deleted.product_status,
                        "producto_publicado": row_deleted.product_published,
                        "volumetria_largo_producto": str(row_deleted.product_length),
                        "volumetria_ancho_producto": str(row_deleted.product_width),
                        "volumetria_alto_producto": str(row_deleted.product_height),
                        "volumetria_peso_producto": str(row_deleted.product_weight),
                        "id_categoria_producto": str(row_deleted.category_id),
                        "id_categoria_padre_producto": str(row_deleted.parent_category_id),
                        "creation_date": str(row_deleted.creation_date),
                        "last_update_date": str(row_deleted.last_update_date)
                    })

            except SQLAlchemyError as exc:
                session.rollback()
                endpoint_response = None

                logger.exception('An exception was occurred while execute transactions: %s',
                                 str(str(exc.args) + ':' +
                                     str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('sku_producto'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    @staticmethod
    def get_product_id(session, data):
        """
        Get Producto object row registered on database to get the ID

        :param session: Database session object
        :param data: Dictionary with data to get row
        :return: row_product: The row on database registered
        """

        row_product = None

        try:

            row_exists = session.query(ProductModel).\
                filter(ProductModel.product_sku == data.get('sku_producto')).\
                filter(ProductModel.product_name == data.get('nombre_producto')).\
                filter(ProductModel.product_brand == data.get('marca_producto')).scalar()

            logger.info('Row Data Producto Exists on DB: %s', str(row_exists))

            if row_exists:

                row_product = session.query(ProductModel). \
                    filter(ProductModel.product_sku == data.get('sku_producto')). \
                    filter(ProductModel.product_name == data.get('nombre_producto')). \
                    filter(ProductModel.product_brand == data.get('marca_producto')).one()

                logger.info('Row ID Product data from database object: {}'.format(str(row_product)))

        except SQLAlchemyError as exc:

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_producto'), ProductModel.__tablename__, str(str(exc.args) + ':' +
                                                                                  str(exc.code))
                )
            )

        finally:
            session.close()

        return row_product

    @staticmethod
    def get_one_product(session, data):
        row = None

        try:

            row = session.query(ProductModel). \
                filter(ProductModel.product_sku == data.get('sku_producto')). \
                filter(ProductModel.product_name == data.get('nombre_producto')). \
                filter(ProductModel.product_brand == data.get('marca_producto')).one()

            if row:
                logger.info('Data Product on Db: %s',
                            'Nombre: {}, SKU: {}, Marca: {}'.format(row.product_name,
                                                                    row.product_sku,
                                                                    row.product_brand))

        except SQLAlchemyError as exc:
            row = None
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_producto'), ProductModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return row

    @staticmethod
    def get_all_products(session, data):
        """
        Get all Products objects data registered on database.

        :param data: Dictionary contains relevant data to filter Query on resultSet DB
        :param session: Database session
        :return: json.dumps dict
        """

        querying_counter = 0

        all_products = None
        product_data = []

        page = None
        per_page = None

        all_products = session.query(ProductModel).all()

        if 'offset' in data.keys() and 'limit' in data.keys():
            page = data.get('offset')
            per_page = data('limit')

            all_products = session.query(ProductModel).paginate(page=page, per_page=per_page, error_out=False).all()

        for product in all_products:

            if product.product_queried_count is not None:
                querying_counter = int(product.product_queried_count)

            querying_counter += 1

            data['last_update_date'] = get_current_date(session)

            # update row to database
            session.query(ProductModel).filter(ProductModel.product_id == product.id_product). \
                update({"product_queried_count": querying_counter,
                        "last_update_date": data.get('last_update_date')},
                       synchronize_session='fetch')

            session.flush()

            product_data += [{
                "Product": {
                    "sku_producto": product.product_sku,
                    "marca_producto": product.product_brand,
                    "unidad_medida_producto": product.unit_of_measure,
                    "inventario_producto": product.product_stock,
                    "nombre_producto": product.product_name,
                    "titulo_producto": product.product_title,
                    "descripcion_larga": product.product_long_description,
                    "url_imagen": product.product_photo,
                    "precio_unitario": str(product.product_price),
                    "costo_impuesto": str(product.product_tax),
                    "tasa_impuesto": str(product.product_tax_rate),
                    "estatus_producto": product.product_status,
                    "producto_publicado": product.product_published,
                    "volumetria_largo_producto": str(product.product_length),
                    "volumetria_ancho_producto": str(product.product_width),
                    "volumetria_alto_producto": str(product.product_height),
                    "volumetria_peso_producto": str(product.product_weight),
                    "id_categoria_producto": str(product.category_id),
                    "id_categoria_padre_producto": str(product.parent_category_id),
                    "contador_busqueda": str(querying_counter),
                    "fecha_alta": str(product.creation_date),
                    "fecha_actualizacion": str(data.get('last_update_date'))
                }
            }]

        return json.dumps(product_data)

    @staticmethod
    def get_products_by_filters(session, data, filter_spec):
        """
        Get list of Products filtered by options by user request

        :param session: Database session
        :param data: Dictionary contains relevant data to filter Query on resultSet DB
        :param filter_spec: List of options defined by user request
        :return: json.dumps dict
        """

        querying_counter = 0

        page = 1
        per_page = 10

        query_result = None
        product_data = []

        if 'offset' in data.keys() and 'limit' in data.keys():
            page = data.get('offset')
            per_page = data('limit')

        query_result = session.query(ProductModel).all()

        query = session.query(ProductModel)

        filtered_query = apply_filters(query, filter_spec)

        if filter_spec is not None and filtered_query is not None:
            query_result = filtered_query.paginate(page=page, per_page=per_page, error_out=False).all()

        logger.info('Query filtered resultSet: %s', str(query_result))

        for product in query_result:

            if product.product_queried_count is not None:
                querying_counter = int(product.product_queried_count)

            querying_counter += 1

            data['last_update_date'] = get_current_date(session)

            # update row to database
            session.query(ProductModel).filter(ProductModel.product_id == product.id_product). \
                update({"product_queried_count": querying_counter,
                        "last_update_date": data.get('last_update_date')},
                       synchronize_session='fetch')

            session.flush()

            product_data += [{
                "Product": {
                    "sku_producto": product.product_sku,
                    "marca_producto": product.product_brand,
                    "unidad_medida_producto": product.unit_of_measure,
                    "inventario_producto": product.product_stock,
                    "nombre_producto": product.product_name,
                    "titulo_producto": product.product_title,
                    "descripcion_larga": product.product_long_description,
                    "url_imagen": product.product_photo,
                    "precio_unitario": str(product.product_price),
                    "costo_impuesto": str(product.product_tax),
                    "tasa_impuesto": str(product.product_tax_rate),
                    "estatus_producto": product.product_status,
                    "producto_publicado": product.product_published,
                    "volumetria_largo_producto": str(product.product_length),
                    "volumetria_ancho_producto": str(product.product_width),
                    "volumetria_alto_producto": str(product.product_height),
                    "volumetria_peso_producto": str(product.product_weight),
                    "id_categoria_producto": str(product.category_id),
                    "id_categoria_padre_producto": str(product.parent_category_id),
                    "contador_busqueda": str(querying_counter),
                    "fecha_alta": str(product.creation_date),
                    "fecha_actualizacion": str(data.get('last_update_date'))
                }
            }]

        return json.dumps(product_data)

    def __repr__(self):
        return "<MunicipioModel(product_id='%s'" \
               "                product_sku='%s', " \
               "                product_brand='%s', " \
               "                unit_of_measure='%s', " \
               "                product_stock='%s'" \
               "                product_name='%s'" \
               "                product_title='%s'" \
               "                product_long_description='%s'" \
               "                product_photo='%s'" \
               "                product_price='%s'" \
               "                product_tax='%s'" \
               "                product_tax_rate='%s'" \
               "                product_status='%s'" \
               "                product_published='%s'" \
               "                product_length='%s'" \
               "                product_width='%s'" \
               "                product_height='%s'" \
               "                product_weight='%s'" \
               "                category_id='%s'" \
               "                parent_category_id='%s'" \
               "                creation_date='%s'" \
               "                last_update_date='%s')>" % (self.product_id,
                                                            self.product_sku,
                                                            self.product_brand,
                                                            self.unit_of_measure,
                                                            self.product_stock,
                                                            self.product_name,
                                                            self.product_title,
                                                            self.product_long_description,
                                                            self.product_photo,
                                                            self.product_price,
                                                            self.product_tax,
                                                            self.product_tax_rate,
                                                            self.product_status,
                                                            self.product_published,
                                                            self.product_length,
                                                            self.product_width,
                                                            self.product_height,
                                                            self.product_weight,
                                                            self.category_id,
                                                            self.parent_category_id,
                                                            self.creation_date,
                                                            self.last_update_date)
