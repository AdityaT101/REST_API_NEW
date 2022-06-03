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

auth = HTTPBasicAuth()

db_connect = create_engine( 'mysql+pymysql://root:Netflix@123@localhost/sakila' )

sakila_args = reqparse.RequestParser()
sakila_args.add_argument( "id", type=str )



@auth.get_password
def get_password( username ):
   if username == 'Aditya':
      return 'Netflix@123'
   return None



@auth.error_handler
def unauthorized():
    payload = {
        "status": 401,
        "error": "Invalid Username or Password",
        "message": "You are not authorized to access this resource"
    }

    response = original_flask_make_response( jsonify( message=payload ), 401 )
    return response



@app.route( '/sakila/get_category_by_id' , methods=['GET'] )
@auth.login_required
def get_category_by_id():
    args = sakila_args.parse_args()

    if args['id'] is None:
        print( args['id'] )

        payload = {
            "status": 400,
            "error": "Bad Request",
            "message": "Parameter not sent"
        }

        response = original_flask_make_response( jsonify(message=payload), 400 )
        abort( response )

    conn = db_connect.connect()

    if conn is None:
        payload = {
            "status": 503,
            "error": "Service is not Available",
            "message": "Service is not Available"
        }

        response = original_flask_make_response( jsonify(message=payload), 503 )
        abort(response)

    query = conn.execute( """select *  from category where category_id = %s""", args['id'] )

    payload = []

    for result in query:
        content = {'category_id': result[0], 'name': result[1], 'free': result[2]}
        payload.append(content)
        print(content)

    if not payload:
        payload = {
            "status": 404,
            "error": "No Data Present",
            "message": "id category does not exists"
        }

        response = original_flask_make_response( jsonify(message=payload), 404 )
        abort( response )

    return( jsonify(payload) )




@app.route( '/sakila/get_all_categories' , methods=['GET'] )
@auth.login_required
def get_all_categories():

    print('abc')

    conn = db_connect.connect()

    if conn is None:
        payload = {
            "status": 503,
            "error": "Service is not Available",
            "message": "Service is not Available"
        }

        response = original_flask_make_response( jsonify(message=payload), 503 )
        abort(response)

    query = conn.execute( """select *  from category""" )

    payload = []

    for result in query:
        content = {'category_id': result[0], 'name': result[1], 'free': result[2]}
        payload.append(content)
        #print(content)

    if not payload:
        payload = {
            "status": 404,
            "error": "No Data Present",
            "message": "id category does not exists"
        }

        response = original_flask_make_response( jsonify(message=payload), 404 )
        abort( response )

    return( jsonify(payload) )




@app.route( '/sakila/post_category_info' , methods=['POST'] )
@auth.login_required
def post_category_info():

    print('xyz')

    conn = db_connect.connect()

    if conn is None:
        payload = {
            "status": 503,
            "error": "Service is not Available",
            "message": "Service is not Available"
        }

        response = original_flask_make_response( jsonify(message=payload), 503 )
        abort(response)

    args = request.json

    if( (  not 'category_id' in args ) or ( not 'name' in args ) or ( not 'free' in args ) ):
        payload = {
            "status": 400,
            "error": "Bad request",
            "message": "request is not proper"
        }

        response = original_flask_make_response(jsonify(message=payload), 400)
        abort(response)

    if( ( args["category_id"] is None ) or ( args["name"] is None ) or ( args["free"] is None ) ):
        payload = {
            "status": 204,
            "message": "No Content"
        }

        response = original_flask_make_response( jsonify(message=payload), 204 )
        abort(response)


    iq = """INSERT INTO category_copy1 values ( {} , '{}', {} )""".format( args["category_id"] ,   args["name"] , args["free"] )

    conn.execute( iq )

    payload = {
        "status": 200,
        "message": "Success"
    }

    response = original_flask_make_response( jsonify( message=payload ), 200 )
    abort(response)









if __name__ == '__main__':
    app.run(debug=True)