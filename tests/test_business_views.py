"""Test case for business manipulation view"""
import json
from tests.base_test_file import BaseTestCase
from app import db


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def register_business(self, msg, code, key='message'):
        self.automate('/api/v1/businesses', key, data=self.business_data,
                      code=code, msg=msg)

    def test_business_creation(self):
        """Test create business works correcty"""
        result = json.loads(self.biz_res.data.decode())
        self.assertEqual(result['message'], "Business created successfully")
        self.assertEqual(self.biz_res.status_code, 201)

    def test_create_business_empty_category(self):
        """Test create business empty category"""
        self.business_data['category'] = "  "
        self.register_business(key='category-error', code=422,
                               msg="The category should not be empty")

    def test_not_registered_user(self):
        """Test create business for unregistered user"""
        with self.app.app_context():
            self.header['Authorization'] = 'Bearer ' + self.token
            self.register_business(code=403, msg='Please login to continue')


class TestPutBusiness(BaseTestCase):
    """Test for editing business endpoint"""
    def edit_business(self, msg, code, key='message'):
        self.automate('/api/v1/businesses/1', key, data=self.business_data,
                      method='put', code=code, msg=msg)

    def test_business_can_be_edited(self):
        """Test edit an existing business works as expected"""
        self.business_data['name'] = 'iHub'
        self.edit_business(code=200, msg='Business updated successfully')

    def test_edit_business_empty_data(self):
        """Test update business with no data"""
        self.business_data = {}
        self.edit_business(code=422,
                           msg="Enter atleast one input to update")

    def test_edit_not_existing(self):
        """Test update business with no data"""
        self.automate('/api/v1/businesses/10', data=self.business_data,
                      key='message', method='put', code=200,
                      msg="The business was not found")

    def test_not_own_business(self):
        """Test update not own business"""
        with self.app.app_context():
            self.header['Authorization'] = 'Bearer ' + self.token
            self.edit_business(code=403, msg='The operation is Forbidden')


class TestDeleteBusiness(BaseTestCase):
    """Test for delete business endpoint"""
    def delete_business(self, msg, code, key='message'):
        self.automate('/api/v1/businesses/1', key, method='delete',
                      data=self.reg_data, code=code, msg=msg)

    def test_business_can_be_deleted(self):
        """Test delete an existing business"""
        self.delete_business(code=200, msg='Business deleted successfully')

    def test_missing_password(self):
        """Test delete with missing password"""
        del self.reg_data['password']
        self.delete_business(code=422, key='password-error',
                             msg='The password should not be missing')

    def test_incorrect_password(self):
        """Test delete with incorrect password"""
        self.reg_data['password'] = 'Test12345'
        self.delete_business(code=401, msg='Enter correct password to delete')

    def test_not_exist_business(self):
        """Test delete non existing business"""
        self.automate(url='/api/v1/businesses/10', data=self.reg_data,
                      method='delete', code=404, key='message',
                      msg='The business was not found')

    def test_delete_another_user_business(self):
        """Test delete a business that user did not create"""
        with self.app.app_context():
            self.reg_data['email'] = 'anotheruser@test.com'
            self.make_request('/api/v1/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.delete_business(code=403,
                                 msg='The operation is Forbidden')


class TestGetBusiness(BaseTestCase):
    """Test for get business endpoint"""
    def get_business(self, url):
        res = self.client.get(path=url)
        return json.loads(res.data.decode())

    def test_all_businesses(self):
        """Test get all registered businesses"""
        result = self.get_business('/api/v1/businesses')
        self.assertTrue(result['businesses'])

    def test_empty_businesses(self):
        """Test get all with no registered businesses"""
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            result = self.get_business('/api/v1/businesses')
            self.assertEqual(result['message'],
                             "There are no businesses registered currently")

    def test_filter_businesses_by_category(self):
        """Test get all registered businesses in a category"""
        result = self.get_business('/api/v1/businesses?cat=IT')
        self.assertTrue(result['businesses'])

    def test_filter_businesses_by_location(self):
        """Test get all registered businesses in a location"""
        result = self.get_business('/api/v1/businesses?loc=Nairobi')
        self.assertTrue(result['businesses'])

    def test_filter_category_and_location(self):
        """Test get all registered businesses in a category"""
        result = self.get_business('/api/v1/businesses?cat=IT&loc=Nairobi')
        self.assertTrue(result['businesses'])

    def test_not_found_category(self):
        """Test filter not available category"""
        result = self.get_business('/api/v1/businesses?cat=Farming')
        self.assertEqual(result['message'],
                         'The filter criteria did not match any business')

    def test_business_id(self):
        """Test get single business"""
        result = self.get_business('/api/v1/businesses/1')
        self.assertTrue(result['business'])

    def test_invalid_business_id(self):
        """Test get not available single business"""
        result = self.get_business('/api/v1/businesses/10')
        self.assertTrue(result['message'], 'The business 10 is not available')
