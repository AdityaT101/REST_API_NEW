from flask import Flask , request
from flask_restful import Api , Resource , reqparse ,abort , fields, marshal_with , original_flask_make_response
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
import json
import datetime
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt


app = Flask(__name__)
api = Api(app)


db_connect = create_engine( 'mysql+pymysql://root:Netflix@123@localhost/sakila' )

sakila_args = reqparse.RequestParser() #*******
sakila_args.add_argument( "id", type=str )



class sakila1(Resource):
    print("aditya")

    def get(self):

        args = sakila_args.parse_args()

        if args['id'] is None:
            print( args['id'] )

            payload =  {
                    "status": 400,
                    "error": "Bad Request",
                    "message": "Parameter not sent"
            }

            response = original_flask_make_response( jsonify( message=payload ) , 400 )
            abort(response)


        conn = db_connect.connect()  # connect to database

        if conn is None:
            payload = {
                "status": 503,
                "error": "Service is not Available",
                "message": "Service is not Available"
            }

            abort( 503, message=payload )

        query = conn.execute( """select *  from category where category_id = %s""", args['id'] )

        payload = []

        for result in query:
            content = {'category_id': result[0], 'name': result[1]  , 'free': result[3]  }
            payload.append(content)
            print( content )


        if not payload :
            payload = {
                "status": 404,
                "error": "Invalid request",
                "message": "id does not exists"
            }

            abort( 404, message= payload )


        return (payload)


api.add_resource( sakila1, "/sakila1")


if __name__ == '__main__':
    app.run(debug=True)