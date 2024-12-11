'''
app.py
'''

from website import create_app
import os
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == '__main__':
    if os.environ.get('CONFIG_TYPE') == "PRODUCTION":
        app.run(debug=False)
    else:
        app.run(debug=True)
