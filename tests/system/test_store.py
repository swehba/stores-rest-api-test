from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Macys')
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Macys'))
                expected = {'id': 1, 'name': 'Macys', 'items': []}
                actual = json.loads(response.data)
                self.assertEqual(actual, expected)

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Macys')
                response = client.post('/store/Macys')
                self.assertEqual(response.status_code, 400)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Macys')
                response = client.delete('/store/Macys')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data),
                                 {'message': 'Store deleted.'})
                self.assertIsNone(StoreModel.find_by_name('Macys'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Macys')
                response = client.get('/store/Macys')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data),
                                 {'id': 1, 'name': 'Macys', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/Macys')
                self.assertEqual(response.status_code, 404)
                self.assertEqual(json.loads(response.data),
                                 {'message': 'Store not found.'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Macys')
                client.post('/item/chair', data={'price': 19.99, 'store_id': 1})
                response = client.get('/store/Macys')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data),
                                 {'id': 1,
                                  'name': 'Macys',
                                  'items': [
                                     {'name': 'chair',
                                      'price': 19.99
                                      }
                                  ]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store1').save_to_db()
                StoreModel('store2').save_to_db()
                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data), {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'store1',
                            'items': []
                        },
                        {
                            'id': 2,
                            'name': 'store2',
                            'items': []
                        }
                    ]
                })

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store1').save_to_db()
                ItemModel('item1', 1.23, 1).save_to_db()
                StoreModel('store2').save_to_db()
                ItemModel('item2', 4.56, 2).save_to_db()
                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.data), {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'store1',
                            'items': [{'name': 'item1', 'price': 1.23}]
                        },
                        {
                            'id': 2,
                            'name': 'store2',
                            'items': [{'name': 'item2', 'price': 4.56}]
                        }
                    ]
                })
