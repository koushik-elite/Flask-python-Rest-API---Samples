from flask import Flask, request, redirect, url_for
from flask_restful import Api, Resource, reqparse
import os
import io
from werkzeug.utils import secure_filename
import csv
import boto3
import uuid
import time

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]

# dynamodb = boto3.resource('dynamodb')

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age", type=str)
        parser.add_argument("occupation", type=str)
        args = parser.parse_args()
        file = request.files['file']
        print(args)

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200
        
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
      
class UploadExcel(Resource):
    def get(self):
        s3 = boto3.resource('s3')
        message = []
        for bucket in s3.buckets.all():
            # print(bucket.name)
            message.append(bucket.name)
        return message, 200
    def post(self):
        print('UploadExcel loaded')
        # table = dynamodb.Table('openpositions')
        result = {
            'message': 'File Uploaded successfully'
        }
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
        else:
            try:
                stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
                csv_input = csv.reader(stream)
                # file.save(os.path.join('./data', filename))
                for row in csv_input:
                    # print([unicode(cell, 'utf-8') for cell in row])
                    print(getPutItemDBParams(row))
            except Exception as e:
                result['message'] = e
                return result, 500
                # print(e)

        # print(args)
        
        return result, 201

def getPutItemDBParams(data):
    return {
        'serialno': str(uuid.uuid1()),
        'code':data[1],
        'position':data[2],
        'description':data[3],
        'mandatoryskills':data[4],
        'softskills':data[5],
        'experience':data[6],
        'level1':data[7],
        'level2':data[8],
        'status':data[9],
        'createdat': str(time.time()),
        'updatedat': str(time.time())
    }

# ['1', 'QA-AX-1', 'QA Engineer (AX)', 'Selenium Automation Test Engineer for AffinityX', 'Selenium (Java), Understanding of Agile Process, SDLC, JIRA', 'Excellent English Speaking Skills, Overlap 50% US timings', '>4 yrs', 'Sundar', 'AffinityX Team', 'Open']
api.add_resource(User, "/user/<string:name>")
api.add_resource(UploadExcel, "/upload")

app.run(debug=True)