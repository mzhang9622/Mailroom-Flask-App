from flask import Flask
from views import main_blueprint


website = Flask(__name__)

website.register_blueprint(main_blueprint)

if __name__ == '__main__':
    website.run(debug=True)
