import logging

import werkzeug
from flask import Flask
from flask_restx import Resource, Api, fields, reqparse
from backend.lexmapr_api import run


app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('csv', required=True, type=werkzeug.datastructures.FileStorage, location='files')


# API
@api.route("/api/lexmapr")
class LexMapr(Resource):
    @staticmethod
    @api.doc(parser=parser)
    @api.marshal_with(fields.String)
    def post() -> dict:
        args = parser.parse_args()
        csv_input: str = args['csv']\
            .read()\
            .decode('utf-8')
        output_data = run(csv_input)
        logging.debug(output_data)
        return output_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
