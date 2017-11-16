from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.store = StoreModel("Macys")

    def test_initial_item_list(self):
        self.assertEqual(self.store.items.all(), [])

    def test_json(self):
        with self.app_context():
            actual = self.store.json()
            expected = {
                "name": "Macys",
                "items": []
            }
            self.assertEqual(actual, expected)

            item = self.add_item_to_store("chair", 123.45)
            actual = self.store.json()
            expected = {
                "name": "Macys",
                "items": [
                    {
                        "id": 1,
                        "name": item.name,
                        "price": item.price
                    }
                ]
            }
            self.assertEqual(actual, expected)

    def test_find_by_name(self):
        with self.app_context():
            self.store.save_to_db()
            s = StoreModel.find_by_name("Macys")
            self.assertIsNotNone(s)

    def test_crud(self):
        with self.app_context():
            s = StoreModel.find_by_name("Macys")
            self.assertIsNone(s)
            self.store.save_to_db()
            s = StoreModel.find_by_name("Macys")
            self.assertIsNotNone(s)
            self.store.delete_from_db()
            s = StoreModel.find_by_name("Macys")
            self.assertIsNone(s)

    def test_store_relationships(self):
        with self.app_context():
            self.store.save_to_db()
            item = self.add_item_to_store("chair", 99.99)
            item.save_to_db()
            self.assertEqual(self.store.items.count(), 1)
            self.assertEqual(self.store.items.first().name, 'chair')

    def add_item_to_store(self, item_name, item_price):
        """
        Create an item and associate it with self.store. Must be called within an app context.

        :param item_name: The name of the item.
        :type item_name: str
        :param item_price: The price of the item.
        :type item_price: float
        :return: The item that was added.
        :rtype: ItemModel
        """
        self.store.save_to_db()
        item = ItemModel(item_name, item_price, self.store.id)
        item.save_to_db()
        return item
