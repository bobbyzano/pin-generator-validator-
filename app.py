from flask import Flask,request,jsonify,session
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from model import generate
import random
import string
import os

# instantiating the Flask class into app
app = Flask(__name__)

# instantiating the Api Class
api = Api(app)

# app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "sqlite:///generate.sqlite3"
app.config['SECRET_KEY'] = "ABCD 12345"



# instantiating the SQL *Class in db 
db=SQLAlchemy(app)


class generate_pin(Resource):

    def get(self):

        # the random funtion generates random 15 digits
        pin = ''.join([random.choice(string.digits) for n in range (15)])
        serial_number = ''.join([random.choice(string.digits) for n in range(12)])

        # creating a variable data and saving the value of the randomly generated pin
        data = generate(serial_number,pin)

        # adding the pin to the database
        db.session.add(data)

        # commiting the new added item
        db.session.commit()

        # querying a column by the pin and saving it to the variable result
        result = generate.query.filter_by(pin = pin).first()
        
        # fetching the id of the particular pin and saving in s_N
        s_n = result.serial_number
        return {'pin': pin, "SN":s_n }
        
 



api.add_resource(generate_pin, '/') 

class validate_pin(Resource):
    def get(self, sn):

        #searches for serial number in db
        result = generate.query.filter_by(serial_number = sn).first()

        #if serial number is found it returns valid pin
        if result:
            return{'message': 'valid pin'}

        #if pin is not valid it returns invalid pin
        else:
            return{'message':'invalid pin'}
        

api.add_resource(validate_pin, '/<string:sn>')         
    




if  __name__ == "__main__":
    app.run(debug=True)