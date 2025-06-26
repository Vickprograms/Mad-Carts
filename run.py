from flask import Flask
from flask_cors import CORS
from app.routes.products import product_routes


app = Flask(__name__)
app.register_blueprint(product_routes)
CORS(app)


if __name__ == '__main__':
    app.run(port = 5555 ,debug=True)
