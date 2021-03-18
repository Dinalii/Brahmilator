import os
from flask import Flask, redirect, url_for, request, jsonify, Response, abort, json
import filetype
import services
from util import make_response

app = Flask(__name__)

input_data = "input_data"
pre_process_data = "pre_process_data"

@app.route("/api/getLetters", methods=["POST"])
def translateLetters():
    try:
        image = request.files["image"]
        image_name = image.filename
        image.save(os.path.join(input_data, image_name))
        if filetype.is_image(os.path.join(input_data, image_name)):
            classify_letters = services.classify_letters()
            result = {'letter': classify_letters}
            response = make_response(result,True,200)
            os.remove(os.path.join(input_data, image_name))
            return Response(response=response, status=200, mimetype='application/json')
        else:
            response = make_response('The file is NOT an Image', False, 200)
            return Response(response=response, status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        response = make_response('The file is NOT FOUND', False, 404)
        return Response(response=response, status=404, mimetype='application/json')


@app.route("/api/preProcess", methods=["POST"])
def preProcessImage():
    try:
        image = request.files["image"]
        image_name = image.filename
        image.save(os.path.join(input_data, image_name))
        if filetype.is_image(os.path.join(input_data, image_name)):
            services.pre_process()
            result = {'pre-process success'}
            response = make_response(result, True, 200)
            os.remove(os.path.join(input_data, image_name))
            return Response(response=response, status=200, mimetype='application/json')
        else:
            response = make_response('The file is NOT an Image', False, 200)
            return Response(response=response, status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        response = make_response('The file is NOT FOUND', False, 404)
        return Response(response=response, status=404, mimetype='application/json')

if __name__ == '__main__':
    app.run()
