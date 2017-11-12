from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    This function gets called when a user calls the /auth endpoint with his username and password.
    :param username: The user's username.
    :type username: str
    :param password: The user's un-encrypted password.
    :type password: str
    :return A user if successful. None otherwise.
    :rtype UserModel
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    """
    This function gets called when a user has already authenticated and Flask-JWT verified that his authorization
    header is correct.
    :param payload: A dictionary with 'identity' key which is the user id.
    :return A user if successful, None otherwise.
    :rtype UserModel
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
