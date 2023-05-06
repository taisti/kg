from flask import Flask
from flask_restful import Resource, Api, request

from src.lexmapr_api import run
from flask import render_template, request

import requests
import json
app = Flask(__name__)
api = Api(app)


###API
class LexMapr(Resource):
    def post(self) -> dict:
        csv_input = request.data.decode("utf-8")
        output_data = run(csv_input)
        return output_data

api.add_resource(LexMapr, "/api/lexmapr")

###WEB APP
@app.route("/",methods=["GET"])
def index():
    """
    [Web Method]
    HTTP methods: GET
    Used template: index.html

    The default index web method. It displays a prompt for uploading a file to analyze. 
    Once the file is uploaded, Lexmapr performs entity linking on the contents of the file.
    """
    return render_template("index.html", context=[])
@app.route("/",methods=["POST"])
def index_post():
    """
    [Web Method]
    HTTP methods: POST
    Used template: index.html

    Default method for displaying an output of lexmapr. The analysis is done via the REST API. 
    The method calls an API function and displays the output rendered with a bootstrap template.
    """
    data = request.files['input_file'].stream.read()
    resp = requests.post(request.url_root + "/api/lexmapr",data=data)
    resp_json = json.loads(resp.content)
    return render_template("index.html",context=resp_json)   


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
