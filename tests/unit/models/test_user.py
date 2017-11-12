from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("jose", "1234")
        self.assertEqual(user.username, 'jose')
        self.assertEqual(user.password, '1234')
