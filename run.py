from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Resource



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

CORS(app)
db  = SQLAlchemy(app)
jwt = JWTManager(app)

db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)

import models, resources


#############################################################################################################
#                                #----------------------------------#                                       #
#                                #           GET METHODS            #                                       #
#                                #----------------------------------#                                       #
#############################################################################################################

api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.AllPassengers, '/passengers')
api.add_resource(resources.AllOwners, '/owners')
api.add_resource(resources.AllDrivers, '/drivers')
api.add_resource(resources.AllVehicles, '/vehicles')
api.add_resource(resources.AllTrips, '/trips')
api.add_resource(resources.AllTripStatus, '/trip_status')

#############################################################################################################
#                                #----------------------------------#                                       #
#                                #           GET with Query Param   #                                       #
#                                #----------------------------------#                                       #
#############################################################################################################


api.add_resource(resources.PickUpLocbyTrip, '/pickuploc/<trip_id>')
api.add_resource(resources.WaypointbyTrip, '/waypoint/<trip_id>')
api.add_resource(resources.TripbyId, '/trip/<trip_id>')

#############################################################################################################
#                                #----------------------------------#                                       #
#                                #          POST METHODS            #                                       #
#                                #----------------------------------#                                       #
#############################################################################################################

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')

api.add_resource(resources.PassengerRegistration, '/reg_passenger')
api.add_resource(resources.OwnerRegistration, '/reg_owner')


# 
# api.add_resource(User.UserLogoutAccess, '/logout/access')
# api.add_resource(User.UserLogoutRefresh, '/logout/refresh')
# api.add_resource(User.TokenRefresh, '/token/refresh')



