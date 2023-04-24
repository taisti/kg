from flask import Flask
from flask_restful import Resource, Api, request

from src.lexmapr import run

app = Flask(__name__)
api = Api(app)


class LexMapr(Resource):
    def post(self) -> dict:
        csv_input = request.data.decode("utf-8")
        json = run(csv_input)
        return json


api.add_resource(LexMapr, "/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
