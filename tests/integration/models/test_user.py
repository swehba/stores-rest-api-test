from models.user import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest


class UserTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('Steve', 'amdg')
            self.assertIsNone(UserModel.find_by_username('Steve'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username('Steve'))
            self.assertIsNotNone(UserModel.find_by_id(1))

            user.delete_from_db()
            self.assertIsNone(UserModel.find_by_username('Steve'))
            self.assertIsNone(UserModel.find_by_id(1))
