from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

NAME_OF_STORE = "Macys"

class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel(NAME_OF_STORE)
        self.assertIsNotNone(store)
        self.assertEqual(store.name, NAME_OF_STORE)
