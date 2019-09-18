#region IMPORTS
import json
from flask_restful import Resource, reqparse,inputs
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, 
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

from models import (
    PassengerModel,OwnerModel,DriverModel,
    VehicleModel,TripPlanModel,TripStatusModel,
    PickupLocationsModel,WaypointsModel,UserModel,
    DriverFeedbackModel,PassengerFeedbackModel,RevokedTokenModel)

from schemas import (
    PassengerSchema,OwnerSchema,DriverSchema,
    VehicleSchema,TripPlanSchema,TripStatusSchema,
    PickupLocationSchema,WaypointsSchema,UserSchema,
    DriverFeedbackSchema,PassengerFeedbackSchema)
#endregion

#region Schemas
users_schema              = UserSchema(many=True)
passenger_schema          = PassengerSchema(many=True)
owner_schema              = OwnerSchema(many=True)
driver_schema             = DriverSchema(many=True)
vehicle_schema            = VehicleSchema(many=True)
trips_plan_schema          = TripPlanSchema(many=True)
trip_status_schema        = TripStatusSchema(many=True)
pickuploc_schema          = PickupLocationSchema(many=True)
waypoints_schema          = WaypointsSchema(many=True)
driver_feedback_schema    = DriverFeedbackSchema(many=True)
passenger_feedback_schema = PassengerFeedbackSchema(many=True)
#endregion

#############################################################################################################
#                                   #------------------------#                                              #
#                                   #      UserResources     #                                              #  
#                                   #------------------------#                                              #  
#############################################################################################################

#region User Resource
user_schema              = UserSchema()

class UserRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        if not data:
            return {'message':'No input data provided'}, 400

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            user_role = data['user_role']
        )

        try:
            new_user.save_to_db()
            return { 'message': 'success' }

        except Exception as e:
            return {'message': 'Something went wrong','error': e}, 500

class UserLogin(Resource):
    def post(self):
        
        data = request.get_json(force=True)

        username = data['username']
        
        current_user = UserModel.find_by_username(username)

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(username)}

        user_role = UserModel.get_user_role(username)
        
        if user_role == 'passenger':
            userId = PassengerModel.get_passengerId(username)
            print('passenger')
        if user_role == 'driver':
            userId = DriverModel.get_driverIdbyNIC(username)
            print('driver')
        if user_role == 'owner':
            userId = OwnerModel.get_ownerId(username)
            print('owner')       

        if UserModel.verify_hash(data['password'], current_user.password):

            genr_access_token  = create_access_token(identity = username)
            genr_refresh_token = create_refresh_token(identity = username)
            
            UserModel.update_table(username, genr_access_token, genr_refresh_token)
            
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': genr_access_token,
                'refresh_token': genr_refresh_token,
                'user_id': userId
                }
        else:
            return {'message':'wrong password'}
            
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()

            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()

            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Refresh token has not been revoked'}
           
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
class AllUsers(Resource):
    
    def get(self):
        d1  = UserModel().all()
        res = users_schema.dump(d1)
        return { "users": res}

    def delete(self):
        return UserModel.delete_all()
#endregion

#############################################################################################################
#                                        #------------------------#                                         #
#                                        #   Passenger Resource   #                                         #
#                                        #------------------------#                                         #
#############################################################################################################

#region Passenger Resources

class PassengerRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        if not data:
            return {'message':'No data provided'}, 400

        #data = passenger_schema.load(data)
        
        if PassengerModel.find_by_email(data['passenger_email']):
            return {'message': 'User {} already exists'.format(data['passenger_name'])}

        new_passenger = PassengerModel(
            ps_token_id     = data['ps_token_id'],
            passenger_name  = data['passenger_name'],
            passenger_email = data['passenger_email'],
            prof_pic        = data['prof_pic'],
            is_ontrip       = data['is_ontrip']
        )

        try:
            new_passenger.save_to_db()
            return {'message': 'passenger {} created'.format(data['passenger_name'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e}, 500

class AllPassengers(Resource):
    def get(self):
        d1 = PassengerModel().all()
        print(d1)
        res = passenger_schema.dump(d1)
        return { 'passengers': res}

class PassengerConfirmation(Resource):
    def get(self,tsId):
        return TripStatusModel().passenger_confirmed(tsId)

#endregion

#############################################################################################################
#                                            #------------------------#                                     #
#                                            #     Owner Resource     #                                     #
#                                            #------------------------#                                     #
#############################################################################################################

#region Owner Resources

class OwnerRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)

        if not data:
            return {'message':'No data provided'}, 400

        if OwnerModel.find_by_nic(data['owner_nic']):
            return {'message': 'Owner {} already exists'.format(data['owner_nic'])}

        new_owner = OwnerModel(
            ow_token_id  = data['ow_token_id'],
            owner_name   = data['owner_name'],
            owner_nic    = data['owner_nic'],
            contact_num  = data['contact_num'],
            address      = data['address'],
            area         = data['area'],
            service_type = data['service_type'],
            company_name = data['company_name'],
            prof_pic     = data['prof_pic']
        )
        
        print(new_owner)

        try:
            new_owner.save_to_db()
            return {'message': 'owner {} created'.format(data['owner_name'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_owner}, 500


class AllOwners(Resource):
    def get(self):
        res = owner_schema.dump(OwnerModel().return_all())
        return { 'owners': res}

class AreaforOwner(Resource):
    def get(self, ow_id):
        d1 = OwnerModel().get_area(ow_id)
        return {'area': d1}

class DriversforOwner(Resource):
    def get(self, owId):

        return_data = []

        if not driver_schema.dump(DriverModel().get_driversby_ownerId(owId)):
            return{'message':'no drivers available this moment'}

        for driver in driver_schema.dump(DriverModel().get_driversby_ownerId(owId)):
            
            for vehicle in vehicle_schema.dump(VehicleModel().vehicle_detailby_driver(driver['dr_id'])):
                return_data.append({
                    'driver':driver['dr_id'],
                    'no_of_passengers':vehicle['no_of_passengers'],
                    'v_type':vehicle['vehicle_type'],
                    'ac_condition':vehicle['ac_condition'],
                    'availability':vehicle['is_ontrip']
                    })

        return return_data

#endregion


#############################################################################################################
#                                        #------------------------#                                         #
#                                        #     Driver Resource    #                                         #
#                                        #------------------------#                                         #
#############################################################################################################

#region Driver Resources

class DriverRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        print(data)

        if not data:
            return {'message':'No data provided'}, 400

        
        
        if DriverModel.find_by_email(data['driver_email']):
            return {'message': 'Driver {} already exists'.format(data['driver_email'])}

        new_driver = DriverModel(
            dr_token_id  = data['dr_token_id'],
            driver_name   = data['driver_name'],
            driver_email    = data['driver_email'],
            owner_id  = data['owner_id'],
            license      = data['license'],
            driver_nic         = data['driver_nic'],
            contact_num = data['contact_num'],
            is_ontrip = data['is_ontrip'],
            prof_pic     = data['prof_pic']
        )
        
        print(new_driver)

        try:
            new_driver.save_to_db()
            return {'message': 'owner {} created'.format(data['driver_name'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_driver}, 500


class AllDrivers(Resource):
    def get(self):
        res = driver_schema.dump(DriverModel().return_all())
        return { 'drivers': res}

class DriverConfirmation(Resource):
    def get(self, tsId, drId):
        if(DriverModel().set_isOnTrip(drId,True,False)
            and VehicleModel().set_isOnTrip(drId,True,False)
            and TripStatusModel().driver_confirmed(tsId)):

            return True
        else:
            return False

class GetAssingedTripsStatus(Resource):
    def get(self, drId):

        if TripStatusModel().trips_available_for_driver(drId):
            return {
            'trip_status_id':TripStatusModel().tripstatus_for_driver(drId),
            'trip_id':TripStatusModel().trip_id_for_driver(drId)}
        else:
            print('else')
            return{'message':'no trips for you !'}

class GetTripDetails(Resource):
    def get(self, tripId):
        return trips_plan_schema.dump(TripPlanModel().find_by_trip_id(tripId))

class FinishTrip(Resource):
    def get(self, tsId, drId):
        if (TripStatusModel().set_trip_status(tsId,False,True) 
            and DriverModel().set_isOnTrip(drId,False,True)
            and VehicleModel().set_isOnTrip(drId,False,True)):
            return True
        else:
            return False

class StartTrip(Resource):
    def get(self, tsId):
        if TripStatusModel().set_trip_status(tsId,True,False):
            return True
        else:
            return False

#endregion Driver Resource

#############################################################################################################
#                                        #------------------------#                                         #
#                                        #     Vehicle Resource   #                                         #    
#                                        #------------------------#                                         #
#############################################################################################################

#region Vehicle Resources

class VehiclRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)

        if not data:
            return {'message':'No data provided'}, 400

        
        if VehicleModel.find_by_vehicle_reg_number(data['vehicle_reg_number']):
            return {'message': 'Vehicle {} already exists'.format(data['vehicle_reg_number'])}

        new_vehicle = VehicleModel(
            vehicle_reg_number  = data['vehicle_reg_number'],
            owner_id   = data['owner_id'],
            ac_condition    = data['ac_condition'],
            vehicle_brand  = data['vehicle_brand'],
            vehicle_type      = data['vehicle_type'],
            no_of_passengers         = data['no_of_passengers'],
            insurance_data = data['insurance_data'],
            is_ontrip = data['is_ontrip']
        )

        try:
            new_vehicle.save_to_db()
            return {'message': 'Vehicle {} created'.format(data['vehicle_reg_number'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_vehicle}, 500


class AllVehicles(Resource):
    def get(self):
        d1 = VehicleModel().return_all()
        print(d1)
        res = vehicle_schema.dump(d1)
        return { 'vehicle': res}


#endregion

#############################################################################################################
#                                        #------------------------#                                         #
#                                        #     TripPlan Resource  #                                         #
#                                        #------------------------#                                         #
#############################################################################################################

#region Triop Plan Resources

trip_plan_schema          = TripPlanSchema()

class CreateTripPlan(Resource):
    def post(self):
        data = request.get_json(force=True)

        if not data:
            return {'message':'No data provided'}, 400

        new_trip = TripPlanModel(
            vehicle_type  = data['vehicle_type'],
            no_of_passengers   = data['no_of_passengers'],
            date_from    = data['date_from'],
            date_to  = data['date_to'],
            pickup_loc      = data['pickup_loc'],
            ac_condition = data['ac_condition'],
            destination = data['destination'],
            passenger_id = data['passenger_id'],
            description = data['description']
        )
        
        try:
            new_trip.save_to_db()
            return {'message': 'Trip Plan created for here {}'.format(data['destination'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_trip}, 500

class AllTrips(Resource):
    def get(self):
        res = trip_plan_schema.dump(TripPlanModel().return_all())
        return { 'trip_plans': res}

class TripbyId(Resource):
    def get(self, trip_id):
        res = trips_plan_schema.dump(TripPlanModel().find_by_trip_id(trip_id))
        return {'trip_plan': res}

class SendTripPlanToOwner(Resource):
    def get(self, ow_id):

        trips_detail = []

        if OwnerModel().is_owner(ow_id):
            result = self.owner_suitsfor_trip(ow_id)
            print('Results',result)

            for item in result:
                if item['is_ok']:    
                    res2 = trips_plan_schema.dump(TripPlanModel().find_by_trip_id(item['trip']))
                    trips_detail.append({'trip':res2})
                
            return jsonify(trips_detail)
        else:
            return {'message':'No trips for you !'}


    def get_tripDetails(self, trip_id):
        return trips_plan_schema.dump(TripPlanModel().find_by_trip_id(trip_id))

    def owner_suitsfor_trip(self, owId):

        area = OwnerModel().get_area(owId)

        trip_by_area = TripPlanModel().trip_detailsbyArea(area)

        trip_plan_json = trips_plan_schema.dump(trip_by_area)

        return_data = []

        for trip in trip_plan_json:
            trip_details = self.get_tripDetails(trip['trip_id'])
            
            for details in trip_details:
                if (VehicleModel().driver_has_vehicle_byLoad(owId, details['no_of_passengers']) and 
                    VehicleModel().driver_has_vehicle_byAC(owId, details['ac_condition']) and 
                    VehicleModel().driver_has_vehicle_byType(owId, details['vehicle_type'])):

                    return_data.append({
                        'is_ok': True,
                        'trip': trip['trip_id']
                    })
                    break                    
                else:
                    return_data.append({
                        'is_ok': False,
                        'trip': trip['trip_id']
                    })
                    break

        return return_data

#endregion

#############################################################################################################
#                                           #-------------------------#                                     #
#                                           #   TripStatus Resource   #                                     #
#                                           #-------------------------#                                     #    
#############################################################################################################

#region Trip Status Resources

class CreateTripStatus(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        if not data:
            return {'message':'No data provided'}, 400

        new_trip_status = TripStatusModel(
            trip_id                 = data['trip_id'],
            trip_budget             = data['trip_budget'],
            assigned_driver         = data['assigned_driver'],
            is_confirmed_passenger  = data['is_confirmed_passenger'],
            is_confirmed_driver     = data['is_confirmed_driver'],
            trip_started            = data['trip_started'],
            vehicle_no              = data['vehicle_no']
        )

        try:
            new_trip_status.save_to_db()
            return {'message': 'Trip Status {} created for '.format(data['trip_id'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_trip_status}, 500


class AllTripStatus(Resource):
    def get(self):
        d1 = TripStatusModel().return_all()
        print(d1)
        res = trip_status_schema.dump(d1)
        return { 'trip_status': res}

class TripStatusById(Resource):
    def get(self, trip_id):
        d1 = TripStatusModel.find_by_tripId(trip_id)
        res = trip_status_schema.dump(d1)
        return { 'trip_status': res}

class AssignDrivers(Resource):
    def post(self):
        data = request.get_json(force=True)

        trip_status_id = data['ts_id']
        new_driver     = data['driver_id']

        if not data:
            return {'message':'No data provided'}, 400

        if TripStatusModel.is_tripstatus(trip_status_id):
            TripStatusModel.update_tableforAssignDriver(trip_status_id,new_driver)
            return{'message':'success', 'trip_status': data['ts_id']}
        else:
            return{'message':'no trip status'}

class SendBudget(Resource):
    def post(self):
        data = request.get_json(force=True)

        if not data:
            return {'message':'No data provided'}, 400

        if TripStatusModel.find_by_newBudget(data['ts_id'],data['trip_id'],data['owner_id']):
            
            TripStatusModel.update_tableforSetBudget(data['ts_id'],data['trip_id'],data['budget'])
            
            trip_status_id = TripStatusModel.get_tripstatus_idbyRecord(data['trip_id'],data['owner_id'],data['budget'])

            return {'message':'Trip budget is set','trip_status_id': trip_status_id}
        else:
            new_entry = TripStatusModel(
                trip_id     = data['trip_id'],
                trip_budget = data['budget'],
                owner_id    = data['owner_id']
                )
            try:
                new_entry.save_to_db()
                trip_status_id = TripStatusModel.get_tripstatus_idbyRecord(data['trip_id'],data['owner_id'],data['budget'])
                return {'message':'Trip budget is assinged','trip_status_id': trip_status_id}
            except Exception as e:
                return {'message':'Something went wrong', 'error':e}

#endregion

#############################################################################################################
#                                        #-------------------------------#                                  #
#                                        #     PickupLocations Resource  #                                  #
#                                        #-------------------------------#                                  #    
#############################################################################################################

#region Pickup Locations Resources

class AddPickupLocations(Resource):
    def post(self):
        data = request.get_json(force=True)

        if not data:
            return {'message':'No data provided'}, 400

        new_pickuploc = PickupLocationsModel(
            trip_id  = data['trip_id'],
            pickup_loc   = data['pickup_loc']
        )
        
        try:
            new_pickuploc.save_to_db()
            return {'message': 'PickupLocations {} created for '.format(data['trip_id'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_pickuploc}, 500


class PickUpLocbyTrip(Resource):
    def get(self, trip_id):
        d1 = PickupLocationsModel().find_by_tripId(trip_id)
        if not d1:
            return {'message':'no pickup locations for this trip'}
        res = pickuploc_schema.dump(d1)
        return { 'pickup_loc': res}

#endregion

#############################################################################################################
#                                        #-------------------------#                                        #
#                                        #     Waypoints Resource  #                                        #
#                                        #-------------------------#                                        #
#############################################################################################################

#region Waypoints Resources

class AddWaypoints(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        if not data:
            return {'message':'No data provided'}, 400

        new_waypoint = WaypointsModel(
            trip_id  = data['trip_id'],
            waypoint   = data['waypoint']
        )

        try:
            new_waypoint.save_to_db()
            return {'message': 'Waypoints {} created for '.format(data['trip_id'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_waypoint}, 500


class WaypointbyTrip(Resource):
    def get(self, trip_id):
        d1 = WaypointsModel().find_by_tripId(trip_id)
        if not d1:
            return {'message':'no waypoints for this trip'}
        res = waypoints_schema.dump(d1)
        return { 'waypoint': res}

#endregion

#############################################################################################################
#                                #-------------------------------#                                          #
#                                #     Driver Feedback Resource  #                                          #
#                                #-------------------------------#                                          #
#############################################################################################################

#region Driver Resources

class CreateDriverFeedback(Resource):
    def post(self):
        data = request.get_json(force=True)
        
        if not data:
            return {'message':'No data provided'}, 400

        new_dr_feedback = DriverFeedbackModel(
            driver_id  = data['driver_id'],
            passenger_id   = data['passenger_id'],
            feedback   = data['feedback']
        )
        
        print(new_dr_feedback)

        try:
            new_dr_feedback.save_to_db()
            return {'message': 'Driver Feedback {} created for '.format(data['driver_id'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_dr_feedback}, 500


class DriverFeedbackbyId(Resource):
    def get(self, driver_id):
        d1 = DriverFeedbackModel().find_by_driverId(driver_id)
        print(d1)
        res = driver_feedback_schema.dump(d1)
        return { 'driver_feedback': res}

#endregion

#############################################################################################################
#                                #----------------------------------#                                       #
#                                #     Passenger Feedback Resource  #                                       #
#                                #----------------------------------#                                       #
#############################################################################################################

#region Passenger Feedback Resources

class CreatePassengerFeedback(Resource):
    def post(self):
        data = request.get_json(force=True)
        

        if not data:
            return {'message':'No data provided'}, 400

        
        new_psng_feedback = PassengerFeedbackModel(
            driver_id  = data['driver_id'],
            passenger_id   = data['passenger_id'],
            feedback   = data['feedback']
        )
        
        print(new_psng_feedback)

        try:
            new_psng_feedback.save_to_db()
            return {'message': 'Passenger Feedback {} created for '.format(data['passenger_id'])}
        except Exception as e:
            return {'message': 'Something went wrong', 'error': e, 'data': new_psng_feedback}, 500


class PassengerFeedbackbyId(Resource):
    def get(self, ps_id):
        d1 = PassengerFeedbackModel().find_by_passengerId(ps_id)
        print(d1)
        res = passenger_feedback_schema.dump(d1)
        return { 'passenger_feedback': res}

#endregion

#############################################################################################################
#                                       #------------------------#                                          #
#                                       #         end            #                                          #
#                                       #------------------------#                                          #
#############################################################################################################
