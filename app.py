from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
toolbar = DebugToolbarExtension(app)

if __name__ == '__main__':
    app.run()
