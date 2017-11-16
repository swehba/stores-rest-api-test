from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def setUp(self):
        super().setUp()

    def test_initial_item_list(self):
        store = StoreModel("Macys")
        self.assertEqual(store.items.all(), [])

    def test_json(self):
        with self.app_context():
            store = StoreModel("Macys")
            store.save_to_db()
            actual = store.json()
            expected = {
                "id": 1,
                "name": "Macys",
                "items": []
            }
            self.assertEqual(actual, expected)

            item = ItemModel("chair", 123.45, store.id)
            item.save_to_db()
            actual = store.json()
            expected = {
                "id": 1,
                "name": "Macys",
                "items": [
                    {
                        "name": item.name,
                        "price": item.price
                    }
                ]
            }
            self.assertEqual(actual, expected)

    def test_find_by_name(self):
        with self.app_context():
            StoreModel("Macys").save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name("Macys"))

    def test_crud(self):
        with self.app_context():
            store1 = StoreModel.find_by_name("Macys")
            self.assertIsNone(store1)
            store1 = StoreModel("Macys")
            store1.save_to_db()
            store2 = StoreModel.find_by_name("Macys")
            self.assertIsNotNone(store2)
            store1.delete_from_db()
            store2 = StoreModel.find_by_name("Macys")
            self.assertIsNone(store2)

    def test_store_relationships(self):
        with self.app_context():
            store = StoreModel("Macys")
            store.save_to_db()
            item = ItemModel("chair", 99.99, store.id)
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'chair')

