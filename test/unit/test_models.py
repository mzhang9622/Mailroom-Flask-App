from website.models import User

def test_user_set_password():
    user = User()
    user.set_password('password')
    assert user.password_hash is not None
    assert user.password_hash != 'password'

def test_user_check_password():
    user = User()
    user.set_password('password')
    assert user.check_password('password')
    assert not user.check_password('wrongpassword')