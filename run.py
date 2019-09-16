from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Resource



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


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


import resources


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
api.add_resource(resources.TripStatusById, '/trip_status/<trip_id>')

api.add_resource(resources.DriverFeedbackbyId, '/driver_feedback/<driver_id>')
api.add_resource(resources.PassengerFeedbackbyId, '/passenger_feedback/<ps_id>')



# TripPlans API #

api.add_resource(resources.SendTripPlanToOwner, '/tripsforowner/<ow_id>')




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
api.add_resource(resources.UserLogoutAccess, '/logout/access')
# api.add_resource(User.UserLogoutRefresh, '/logout/refresh')
# api.add_resource(User.TokenRefresh, '/token/refresh')

api.add_resource(resources.CreateTripPlan, '/createTrip')


