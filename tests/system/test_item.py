from models.user import UserModel
from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest

import json


class ItemTest(BaseTest):
    def setUp(self):
        super().setUp()
        with self.app() as client:
            with self.app_context():
                user = UserModel('test', '1234')
                user.save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': user.username, 'password': user.password}),
                                            headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_response.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 500)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/items/test', headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('a_store')
                store.save_to_db()
                item = ItemModel('an_item', 19.99, store.id)
                item.save_to_db()
                self.assertIsNotNone(ItemModel.find_by_name(item.name))
                response = client.get(f'/item/{item.name}', headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('a_store')
                store.save_to_db()
                item = ItemModel('an_item', 19.99, store.id)
                item.save_to_db()
                response = client.delete(f'/item/{item.name}')
                self.assertEqual(response.status_code, 200)
                item = ItemModel.find_by_name(item.name)
                self.assertIsNone(item)

    def test_create_item(self):
        pass

    def test_create_duplicate_item(self):
        pass

    def test_put_item(self):
        pass

    def test_put_update_item(self):
        pass

    def test_item_list(self):
        pass
