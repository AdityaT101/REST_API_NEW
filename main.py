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

app.config['SECRET_KEY'] = 'eduCBA'

api = Api(app)


basicAuth = HTTPBasicAuth()


users = {
            "AdityaT101": generate_password_hash("Netflix@123"),
            "PoojaT101": generate_password_hash("Pooja@123")
}



@basicAuth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash( users.get(username), password ):
       print("auh=")
       return username


db_connect = create_engine('mysql+pymysql://root:Netflix@123@localhost/sakila')



sakila_args = reqparse.RequestParser() #*******
sakila_args.add_argument("id", type=str , help="argument not sent")


class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')







@app.route('/login')
def login():
    userAuth = request.authorization

    if userAuth and userAuth.password == "secret":
        print("secret")
        token = jwt.encode( { 'user': userAuth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12) },app.config['SECRET_KEY'] )

        return jsonify({'token' : token })

    return original_flask_make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'} )




def token_required(f):
    @wraps(f)
    def token_dec(*args, **kwargs):
        print('adi ')
        token = request.args.get('token')

        if not token:
            return "Missing Token!"
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return "Invalid Token"

        return f(*args, **kwargs)

    return token_dec


resource_fields = {
	'category_id': fields.Integer,
	'name': fields.String,
	'last_update': DateFormat,
	'free': fields.Integer
}

#
# class sakila(Resource):
#     print("aditya")
#
#     @token_required
#     @marshal_with(resource_fields)
#     def get(self):
#         args = sakila_args.parse_args()
#
#         #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoic2VjcmV0IiwiZXhwIjoxNjQ0NDk2NDk3fQ.Ky9mQvmj_u3NG8kO2ZIqhquOBcit-vUYJGkOVKAP3B0
#
#         if args['id'] is None:
#             print(args['id'])
#             payload =  {
#                     "timestamp": datetime.now(),
#                     "status": 400,
#                     "error": "Bad Request",
#                     "message": "Parameter not sent",
#                     "path": ( "sakila?id=None" )
#             }
#
#             response = original_flask_make_response(jsonify(message=payload), 400)
#             abort(response)
#
#
#         conn = db_connect.connect()  # connect to database
#
#         if conn is None:
#             abort(503, message=" Service is not Available ")
#
#         query = conn.execute("""select *  from category where category_id =  %s  """, args['id'] )
#
#         payload = []
#         content = {}
#         temp =[]
#         for result in query:
#             content = {'category_id': result[0], 'name': result[1] , 'last_update': result[2] , 'free': result[3]  }
#             temp.append(result[0])
#             payload.append(content)
#             content = {}
#
#         if not payload :
#             abort(404, message="id does not exists")
#
#         return (payload)
#
#
#     def post(self):
#         return {'request': 'POST'}
#

api.add_resource( sakila, "/sakila")


if __name__ == '__main__':
    app.run(debug=True)
