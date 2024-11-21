from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import session
from flask import abort
from models import db
from models import User
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests
import os
import requests

auth_blueprint = Blueprint('auth', __name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

flow = Flow.from_client_config(
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": ["http://127.0.0.1:5000/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },

    scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri = os.environ.get('REDIRECT')
)

@auth_blueprint.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_blueprint.route('/callback')
def callback():
    flow.fetch_token(authorization_response = request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session = cached_session)
    id_info = id_token.verify_oauth2_token(id_token = credentials._id_token, request = token_request, audience = GOOGLE_CLIENT_ID)
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    user = User.query.filter_by(email = id_info.get("email")).first()
    
    if user:
        login_user(user)
        return redirect(url_for('main.index'))
    else:
        flash('ERROR: Invalid email address', 'error')
        return redirect(url_for('auth.login'))