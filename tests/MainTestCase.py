import unittest
from tests.UserAuthenticationTest import TestUserLogin
from tests.ManageCategoryTest import TestManageCategory
from tests.ManageProductTest import TestManageProduct


class MyTestCase(unittest.TestCase):
    user_test_obj = None
    category_test_obj = None
    product_test_obj = None

    def test_manage_users(self):
        self.user_test_obj = TestUserLogin()

        self.user_test_obj.test_successful_login()
        self.user_test_obj.test_login_already_existing_user()
        self.user_test_obj.test_login_with_invalid_username()
        self.user_test_obj.test_login_with_invalid_password()
        self.user_test_obj.test_login_get_users()
        self.user_test_obj.test_user_update_data()
        self.user_test_obj.test_user_delete_data()

    def test_manage_categories(self):
        self.category_test_obj = TestManageCategory()

        self.category_test_obj.test_manage_category_create()
        self.category_test_obj.test_manage_category_update()
        self.category_test_obj.test_manage_category_delete()
        self.category_test_obj.test_manage_category_get_all()
        self.category_test_obj.test_search_category_filter()

    def test_manage_products(self):
        self.product_test_obj = TestManageProduct()

        self.product_test_obj.test_manage_product_create()
        self.product_test_obj.test_manage_product_update()
        self.product_test_obj.test_manage_product_delete()
        self.product_test_obj.test_manage_product_get_all()
        self.product_test_obj.test_search_product_filter()


if __name__ == '__main__':
    unittest.main()
