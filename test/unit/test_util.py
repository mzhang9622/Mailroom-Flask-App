from website.util import send_email
import pytest

#Temporarily fails due to transfer of control of API from Ming's email to DeAnna's email
@pytest.mark.skip
def test_send_email():
    response = send_email("Hello", "jhsmit25@colby.edu", "I need help!")
    assert response.status_code == 200
    assert b"Email sent:" in response.data