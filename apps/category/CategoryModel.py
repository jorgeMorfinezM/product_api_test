# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later


PostgreSQL DB backend.

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
    About the Category data on the database to generate CRUD operations from endpoint of the API:
    - Insert data
    - Update data
    - Delete data (inactivate)
    - Search all data registered
    - Search data by filter

"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.H28.1 ($Rev: 1 $)"

import json
import logging
from sqlalchemy_filters import apply_filters
from sqlalchemy import Column, Numeric, Integer, String, Date, Time, Sequence
from db_controller.database_backend import *
from db_controller import mvc_exceptions as mvc_exc

cfg_db = get_config_settings_db()

CATEGORY_ID_SEQ = Sequence('category_seq')  # define sequence explicitly


class CategoryModel(Base):

    r"""
    Class to instance the data of CategoryModel on the database.

    Transactions:
     - Create: Add data to the database if not exists.
     - Update:  Update data to the database if exists.
     - Delete:  Inactivate data to the database if exists.
     - Select:  Get data from databases.
    """

    __tablename__ = 'category'

    category_id = Column('id_category', Integer, CATEGORY_ID_SEQ,
                         primary_key=True, server_default=CATEGORY_ID_SEQ.next_value())
    category_name = Column('name_category', String, nullable=False, index=True)
    category_short_description = Column('short_desc_category', String, nullable=False)
    category_status = Column('status_category', String, nullable=False, index=True)
    creation_date = Column('creation_date', Date, nullable=False)
    last_update_date = Column('last_update_date', Date, nullable=True)

    def __init__(self, data_category):
        self.category_name = data_category.get('nombre_categoria')
        self.category_short_description = data_category.get('descrippcion_corta_categoria')
        self.category_status = data_category.get('estatus_categoria')

    def check_if_row_exists(self, session, data):
        """
        Validate if row exists on database from dictionary data

        :param session: Session database object
        :param data: Dictionary with data to make validation function
        :return: row_exists: Object with boolean response from db
        """

        row_exists = None
        id_category = 0

        try:
            # for example to check if the insert on db is correct
            row_category = self.get_category_id(session, data)

            if row_category is not None:
                id_category = row_category.category_id
            else:
                id_category = 0

            logger.info('Category Row object in DB: %s', str(id_category))

            row_exists = session.query(CategoryModel).filter(CategoryModel.category_id == id_category). \
                filter(CategoryModel.category_status == 'activo').scalar()

            logger.info('Row to data: {}, Exists: %s'.format(data), str(row_exists))

        except SQLAlchemyError as exc:
            row_exists = None

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.IntegrityError(
                'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_categoria'),
                                                                    str(str(exc.args) + ':' + str(exc.code)))
            )
        finally:
            session.close()

        return row_exists

    def insert_data(self, session, data):
        """
        Function to insert new row on database

        :param session: Session database object
        :param data: Dictionary to insert new the data containing on the db
        :return: endpoint_response
        """

        endpoint_response = None

        if not self.check_if_row_exists(session, data):

            try:

                self.creation_date = get_current_date(session)

                data['creation_date'] = self.creation_date

                new_row = CategoryModel(data)

                logger.info('New Row Category: %s', str(new_row.category_name))

                session.add(new_row)

                row_category = self.get_category_id(session, data)

                logger.info('Category ID Inserted: %s', str(row_category.category_id))

                session.flush()

                data['id_categoria'] = row_category.category_id

                # check insert correct
                row_inserted = self.get_one_category(session, data)

                logger.info('Data Category inserted: %s, Original Data: {}'.format(data), str(row_inserted))

                if row_inserted:

                    endpoint_response = json.dumps({
                        "id_categoria": str(row_category.category_id),
                        "nombre_categoria": row_category.category_name,
                        "descripcion_categoria": row_category.category_short_description,
                        "estatus_categoria": row_category.category_status
                    })

            except SQLAlchemyError as exc:
                endpoint_response = None
                session.rollback()

                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_categoria'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    # Transaction to update Category's data on db to authenticate - PUT
    def update_data(self, session, data):
        r"""
        Transaction to update data of a user to authenticate on the API correctly.

        :param session: The ciudad name to update password hashed.
        :param data: The password hashed to authenticate on the API.
        """

        endpoint_response = None

        if self.check_if_row_exists(session, data):

            try:

                row_category = self.get_category_id(session, data)

                if row_category is not None:
                    id_category = row_category.category_id
                else:
                    id_category = 0

                self.last_update_date = get_current_date(session)

                data['last_update_date'] = self.last_update_date

                # update row to database
                session.query(CategoryModel).filter(CategoryModel.category_id == id_category). \
                    update({"category_name": data.get('nombre_categoria'),
                            "category_short_description": data.get('descrippcion_corta_categoria'),
                            "category_status": data.get('estatus_categoria'),
                            "last_update_date": data.get('last_update_date')},
                           synchronize_session='fetch')

                session.flush()

                # check update correct
                row_updated = self.get_one_category(session, data)

                logger.info('Data Updated: %s', str(row_updated))

                if row_updated:
                    logger.info('Data Category updated')

                    endpoint_response = json.dumps({
                        "id_categoria": str(row_updated.category_id),
                        "nombre_categoria": row_updated.category_name,
                        "descripcion_categoria": row_updated.category_short_description,
                        "estatus_categoria": row_updated.category_status,
                        "creation_date": row_updated.creation_date,
                        "last_update_date": row_updated.last_update_date
                    })

            except SQLAlchemyError as exc:
                session.rollback()
                endpoint_response = None

                logger.exception('An exception was occurred while execute transactions: %s',
                                 str(str(exc.args) + ':' +
                                     str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_categoria'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    # Transaction to delete category's data on db to authenticate - DELETE
    def category_inactivate(self, session, data):
        r"""
        Transaction to inactivate category data on the API correctly.

        :param session: The database object session connect.
        :param data: The data dictionary to inactivate on the API.
        """

        endpoint_response = None

        if self.check_if_row_exists(session, data):

            try:

                row_category = self.get_category_id(session, data)

                if row_category is not None:
                    id_category = row_category.category_id
                else:
                    id_category = 0

                self.last_update_date = get_current_date(session)

                data['last_update_date'] = self.last_update_date

                # update row to database
                session.query(CategoryModel).filter(CategoryModel.category_id == id_category). \
                    filter(CategoryModel.category_status == "activo"). \
                    update({"category_status": "inactivo",
                            "last_update_date": data.get('last_update_date')},
                           synchronize_session='fetch')

                session.flush()

                # check delete correct
                row_deleted = self.get_one_category(session, data)

                logger.info('Data Deleted: %s', str(row_deleted))

                if row_deleted:
                    logger.info('Data Category inactivated')

                    endpoint_response = json.dumps({
                        "id_categoria": str(row_deleted.category_id),
                        "nombre_categoria": row_deleted.category_name,
                        "descripcion_categoria": row_deleted.category_short_description,
                        "estatus_categoria": row_deleted.category_status,
                        "creation_date": row_deleted.creation_date,
                        "last_update_date": row_deleted.last_update_date
                    })

            except SQLAlchemyError as exc:
                session.rollback()
                endpoint_response = None

                logger.exception('An exception was occurred while execute transactions: %s',
                                 str(str(exc.args) + ':' +
                                     str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_categoria'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    @staticmethod
    def get_category_id(session, data):
        """
        Get Category object row registered on database to get the ID

        :param session: Database session object
        :param data: Dictionary with data to get row
        :return: row_category: The row on database registered
        """

        row_category = None

        try:

            row_exists = session.query(CategoryModel).\
                filter(CategoryModel.category_name == data.get('nombre_categoria')).scalar()

            logger.info('Row Data Category Exists on DB: %s', str(row_exists))

            if row_exists:

                row_category = session.query(CategoryModel). \
                    filter(CategoryModel.category_name == data.get('nombre_categoria')). \
                    filter(CategoryModel.category_status == data.get('estatus_categoria')).one()

                logger.info('Row ID Category data from database object: {}'.format(str(row_category)))

        except SQLAlchemyError as exc:

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_categoria'), CategoryModel.__tablename__, str(str(exc.args) + ':' +
                                                                                   str(exc.code))
                )
            )

        finally:
            session.close()

        return row_category

    @staticmethod
    def get_one_category(session, data):
        row = None

        try:

            row = session.query(CategoryModel).filter(CategoryModel.category_id == data.get('id_categoria')).one()

            if row:
                logger.info('Data Categoria on Db: %s',
                            'Nombre: {}, Estatus: {}'.format(row.category_name,
                                                             row.category_status))

        except SQLAlchemyError as exc:
            row = None
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_categoria'), CategoryModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return row

    @staticmethod
    def get_all_categories(session, data):
        """
        Get all Categories objects data registered on database.

        :param data: Dictionary contains relevant data to filter Query on resultSet DB
        :param session: Database session
        :return: json.dumps dict
        """

        all_categories = None
        category_data = []

        page = None
        per_page = None

        all_categories = session.query(CategoryModel).all()

        if 'offset' in data.keys() and 'limit' in data.keys():
            page = data.get('offset')
            per_page = data('limit')

            all_categories = session.query(CategoryModel).paginate(page=page, per_page=per_page, error_out=False).all()

        for category in all_categories:
            category_id = category.category_id
            category_name = category.category_name
            category_short_desc = category.category_short_description
            category_status = category.category_status

            category_data += [{
                "Categoria": {
                    "id_categoria": str(category_id),
                    "nombre_categoria": category_name,
                    "descripcion_categoria": category_short_desc,
                    "estatus_categoria": category_status,
                    "creation_date": category.creation_date,
                    "last_update_date": category.last_update_date
                }
            }]

        return json.dumps(category_data)

    @staticmethod
    def get_category_by_filters(session, data, filter_spec):
        """
        Get list of States filtered by options by user request

        :param session: Database session
        :param data: Dictionary contains relevant data to filter Query on resultSet DB
        :param filter_spec: List of options defined by user request
        :return: json.dumps dict
        """

        page = 1
        per_page = 10

        query_result = None
        category_data = []

        if 'offset' in data.keys() and 'limit' in data.keys():
            page = data.get('offset')
            per_page = data('limit')

        query_result = session.query(CategoryModel).all()

        query = session.query(CategoryModel)

        filtered_query = apply_filters(query, filter_spec)

        if filter_spec is not None and filtered_query is not None:
            query_result = filtered_query.paginate(page=page, per_page=per_page, error_out=False).all()

        logger.info('Query filtered resultSet: %s', str(query_result))

        for category in query_result:
            category_id = category.category_id
            category_name = category.category_name
            category_short_desc = category.category_short_description
            category_status = category.category_status

            category_data += [{
                "Categoria": {
                    "id_categoria": str(category_id),
                    "nombre_categoria": category_name,
                    "descripcion_categoria": category_short_desc,
                    "estatus_categoria": category_status,
                    "creation_date": category.creation_date,
                    "last_update_date": category.last_update_date
                }
            }]

        return json.dumps(category_data)

    def __repr__(self):
        return "<CategoryModel(category_id='%s', " \
               "               category_name='%s', " \
               "               category_short_description='%s', " \
               "               category_status='%s'," \
               "               creation_date='%s', " \
               "               last_update_date='%s')>" % (self.category_id,
                                                           self.category_name,
                                                           self.category_short_description,
                                                           self.category_status,
                                                           self.creation_date,
                                                           self.last_update_date)
