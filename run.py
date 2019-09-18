from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Resource


#region BASIC APP CONFIGURATIONS->DB & CORS

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'


CORS(app)
db  = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()

#endregion

#region JWT CONFIGURATIONS

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

#endregion

import resources

#############################################################################################################
#                                #----------------------------------#                                       #
#                                #           GET METHODS            #                                       #
#                                #----------------------------------#                                       #
#############################################################################################################

#region GET METHODS
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.AllPassengers, '/passengers')
api.add_resource(resources.AllOwners, '/owners')
api.add_resource(resources.AllDrivers, '/drivers')
api.add_resource(resources.AllVehicles, '/vehicles')
api.add_resource(resources.AllTrips, '/trips')
api.add_resource(resources.AllTripStatus, '/trip_status')


					# FEEDBACK GET METHODS #					
api.add_resource(resources.DriverFeedbackbyId, '/get_driver_feedback/<driver_id>')
api.add_resource(resources.PassengerFeedbackbyId, '/get_passenger_feedback/<ps_id>')

					# GET TRIPS FOR OWNERS  #
api.add_resource(resources.SendTripPlanToOwner, '/tripsby_owner/<ow_id>')

					# GET TRIPS DETAILS BY ID #
api.add_resource(resources.TripbyId, '/trip/<trip_id>')

					# GET TRIP STATUS BY ID   #
api.add_resource(resources.TripStatusById, '/trip_status/<trip_id>')

					# GET WAYPOINTS #
api.add_resource(resources.WaypointbyTrip, '/get_waypoints/<trip_id>')

					# GET PICKUPLOCS #
api.add_resource(resources.PickUpLocbyTrip, '/get_pickuplocs/<trip_id>')


					# GET DRIVERS FOR OWNER#
api.add_resource(resources.DriversforOwner, '/get_driversby_owner/<owId>')

#endregion

#############################################################################################################
#                                #----------------------------------#                                       #
#                                #          POST METHODS            #                                       #
#                                #----------------------------------#                                       #
#############################################################################################################

#region POST METHODS

				# TRIP PLAN POST METHODS #
api.add_resource(resources.CreateTripPlan, '/createTrip')
api.add_resource(resources.AddWaypoints, '/add_waypoints')
api.add_resource(resources.AddPickupLocations, '/add_pickuplocs')


					# USER REGISTRATION #
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')

api.add_resource(resources.PassengerRegistration, '/reg_passenger')
api.add_resource(resources.OwnerRegistration, '/reg_owner')

api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')

					# OWNERS POST METHODS #
api.add_resource(resources.AssignDrivers, '/assignDrivers')
api.add_resource(resources.SendBudget, '/sendBudget')

				# FEEDBACK POST METHODS#

api.add_resource(resources.CreatePassengerFeedback, '/set_passenger_feedback')
api.add_resource(resources.CreateDriverFeedback, '/set_driver_feedback')


				# VEHICLE POST METHODS #
#api.add_resource(resources.VehiclesforOwner, '/vehiclesforowner')





#endregion