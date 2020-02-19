from flask import Flask
from api.api import api

#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask

app = Flask(__name__)
app.config["DEBUG"] = True
app.register_blueprint(api, url_prefix='/api')

if __name__=='__main__':
    app.run()