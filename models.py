from datetime import datetime
from run import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from flask import jsonify

#############################################################################################################
#										#----------------#													#
#										# Passenger Model#												    #
#										#----------------#													#
#############################################################################################################

class PassengerModel(db.Model):
    
	__tablename__ = 'passenger'
	__table_args__ = {'extend_existing': True}

	ps_id 		   = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ps_token_id    = db.Column(db.String(120),unique=True, nullable=False)
	passenger_name = db.Column(db.String(50),unique=True, nullable=False)
	passenger_email= db.Column(db.String(120),unique=True, nullable=False)
	prof_pic 	   = db.Column(db.String(120),unique=True, nullable=True)
	is_ontrip 	   = db.Column(db.Boolean, nullable=True, default=False)
	created 	   = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	   = db.Column(db.String(50), default=datetime.now(),nullable=True)

	
	tripplan		  = relationship('TripPlanModel')
	passengerfeedback = relationship("PassengerFeedbackModel")
	driverfeedback    = relationship("DriverFeedbackModel")

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		def to_json(x):
			return {
				'token': x.ps_token_id,
				'passenger_name': x.passenger_name,
				'passenger_email': x.passenger_email,
				'prof_pic': x.prof_pic,
				'is_ontrip': x.is_ontrip,
				'created':	x.created,
				'updated': x.updated
			}
		return { 'passengers': list(map(lambda x: to_json(x), PassengerModel.query.all()))}

	@classmethod
	def all(cls):
    		return PassengerModel.query.all()		

	@classmethod
	def find_by_email(cls, email):
		return cls.query.filter_by(passenger_email = email).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#												#----------------#											#
#												#   Owner Model  #											#
#												#----------------#											#
#############################################################################################################

class OwnerModel(db.Model):
    
	__tablename__ = 'owner'
	__table_args__ = {'extend_existing': True}

	ow_id 		 = db.Column(db.Integer,primary_key=True, autoincrement=True)
	ow_token_id  = db.Column(db.String(120))
	owner_name   = db.Column(db.String(100), nullable=False)
	owner_nic	 = db.Column(db.String(20), nullable=False)
	contact_num  = db.Column(db.Integer, unique=True)
	address 	 = db.Column(db.String(120), unique=True, nullable=False)
	area 		 = db.Column(db.String(50), unique=True, nullable=False)
	service_type = db.Column(db.String(60), unique=True, nullable=False)
	company_name = db.Column(db.String(100),unique=True, nullable=False)
	prof_pic     = db.Column(db.String(100),unique=True, nullable=True)
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	driver 		 = relationship("DriverModel")
	vehicle		 = relationship("VehicleModel")

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return OwnerModel.query.all()

	@classmethod
	def find_by_nic(cls, nic):
		return cls.query.filter_by(owner_nic = nic).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#												#----------------#										    #
#												#  Driver Model  #											#
#												#----------------#											#
#############################################################################################################

class DriverModel(db.Model):
    
	__tablename__ = 'driver'
	__table_args__ = {'extend_existing': True}

	dr_id 		= db.Column(db.Integer, primary_key=True, autoincrement=True)
	dr_token_id = db.Column(db.String(120))
	driver_name = db.Column(db.String(100),unique=True, nullable=False)
	driver_email= db.Column(db.String(100), unique=True, nullable=False)
	owner_id 	= db.Column(db.Integer, ForeignKey('owner.ow_id'))
	license 	= db.Column(db.String(50),unique=True, nullable=False)
	driver_nic	= db.Column(db.String(50),unique=True, nullable=False)
	prof_pic	= db.Column(db.String(50),unique=True, nullable=True)
	contact_num	= db.Column(db.Integer,unique=True, nullable=False)
	is_ontrip	= db.Column(db.Boolean, default=False)
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	vehicle 	= relationship("VehicleModel",uselist=False, back_populates='driver')
	
	tripstatus  = relationship("TripStatusModel")
	
	driverfeedback = relationship("DriverFeedbackModel")
	driverfeedback = relationship("PassengerFeedbackModel")

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return DriverModel.query.all()

	@classmethod
	def find_by_email(cls, email):
    		return cls.query.filter_by(driver_email = email).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#												#----------------#										    #
#												# Vehicle Model  #											#
#												#----------------#											#
#############################################################################################################

class VehicleModel(db.Model):

	__tablename__ = 'vehicle'

	v_id 			   = db.Column(db.Integer, primary_key=True, autoincrement=True)
	vehicle_reg_number = db.Column(db.String(100),unique=True, nullable=False)
	owner_id		   = db.Column(db.Integer, ForeignKey('owner.ow_id'))
	driver_id          = db.Column(db.Integer, ForeignKey('driver.dr_id'))
	ac_condition       = db.Column(db.Boolean)
	vehicle_brand      = db.Column(db.String(100),unique=True, nullable=False)
	vehicle_type       = db.Column(db.String(100),unique=True, nullable=False)
	no_of_passengers   = db.Column(db.Integer)
	insurance_data     = db.Column(db.String(100),unique=True, nullable=False)
	is_ontrip          = db.Column(db.Boolean, default=False)
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	driver 	   = relationship("DriverModel", back_populates='vehicle')
	tripstatus = relationship("TripStatusModel", uselist=False, back_populates='vehicle')


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return VehicleModel.query.all()

	@classmethod
	def find_by_vehicle_reg_number(cls, vehicle_reg_number):
    		return cls.query.filter_by(vehicle_reg_number = vehicle_reg_number).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#												#----------------#											#
#												#  TripPlanModel #											#
#												#----------------#											#
#############################################################################################################

class TripPlanModel(db.Model):
    
	__tablename__ = 'tripplan'

	trip_id			 = db.Column(db.Integer, primary_key=True, autoincrement=True)
	vehicle_type     = db.Column(db.String(100),unique=True, nullable=False)
	no_of_passengers = db.Column(db.Integer)
	date_from		 = db.Column(db.String(50))
	date_to			 = db.Column(db.String(50))
	pickup_loc	 	 = db.Column(db.String(50))
	ac_condition	 = db.Column(db.Boolean)
	destination		 = db.Column(db.String(120))
	passenger_id	 = db.Column(db.Integer, ForeignKey('passenger.ps_id'))
	description		 = db.Column(db.String(120))
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	tripstatus 	 	 = relationship("TripStatusModel",uselist=False,back_populates='tripplan')
	
	waypoints 		 = relationship("WaypointsModel")
	pickuplocations  = relationship("PickupLocationsModel")
	

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return TripPlanModel.query.all()

	@classmethod
	def find_by_trip_id(cls, trip_id):
    		return TripPlanModel.query.filter_by(trip_id = trip_id).all()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#											#-----------------#												#
#											# TripStatusModel #											    #
#											#-----------------#												#
#############################################################################################################

class TripStatusModel(db.Model):
    
	__tablename__ = 'tripstatus'

	ts_id					= db.Column(db.Integer, primary_key=True, autoincrement=True)
	trip_id 				= db.Column(db.Integer, ForeignKey('tripplan.trip_id'))
	trip_budget				= db.Column(db.Float)
	assigned_driver			= db.Column(db.Integer, ForeignKey('driver.dr_id'))
	is_confirmed_passenger	= db.Column(db.Boolean)
	is_confirmed_driver		= db.Column(db.Boolean)
	trip_started			= db.Column(db.Boolean)
	vehicle_no				= db.Column(db.Integer, ForeignKey('vehicle.v_id'))
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	tripplan = relationship("TripPlanModel", back_populates='tripstatus')
	vehicle = relationship("VehicleModel", back_populates='tripstatus')

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return TripStatusModel.query.all()

	@classmethod
	def find_by_tripId(cls, tripId):
    		return cls.query.filter_by(trip_id = tripId).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}


#############################################################################################################
#										#---------------------#												#
#										# DriverFeedbackModel #												#
#										#---------------------#												#
#############################################################################################################

class DriverFeedbackModel(db.Model):
    
	__tablename__ = 'driverfeedback'
	__table_args__ = {'extend_existing': True}

	fdb_id		= db.Column(db.Integer, primary_key=True, autoincrement=True)
	driver_id	= db.Column(db.Integer, ForeignKey('driver.dr_id'))
	passenger_id = db.Column(db.Integer, ForeignKey('passenger.ps_id'))
	feedback 	= db.Column(db.String(120))
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return jsonify(PassengerModel.query.all())

	@classmethod
	def find_by_driverId(cls, driverId):
    		return cls.query.filter_by(driver_id = driverId).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#									#------------------------#												#
#									# PassengerFeedbackModel #												#
#									#------------------------#												#
#############################################################################################################

class PassengerFeedbackModel(db.Model):
    
	__tablename__ = 'passengerfeedback'

	fdb_id		 = db.Column(db.Integer, primary_key=True, autoincrement=True)
	passenger_id = db.Column(db.Integer, ForeignKey('passenger.ps_id'))
	driver_id	 = db.Column(db.Integer, ForeignKey('driver.dr_id'))
	feedback 	 = db.Column(db.String(120))
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return jsonify(PassengerFeedbackModel.query.all())

	@classmethod
	def find_by_passengerId(cls, ps_id):
    		return cls.query.filter_by(passenger_id = ps_id).first()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#											#------------------------#										#
#											# PickupLocationsModel   #										#
#											#------------------------#										#
#############################################################################################################

class PickupLocationsModel(db.Model):
    
	__tablename__ = 'pickuplocations'

	pl_id			= db.Column(db.Integer, primary_key=True, autoincrement=True)
	trip_id 		= db.Column(db.Integer, ForeignKey('tripplan.trip_id'))
	pickup_loc		= db.Column(db.String(50))
	created 	 	= db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 	= db.Column(db.String(50), default=datetime.now(),nullable=True)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return PickupLocationsModel.query.all()

	@classmethod
	def find_by_tripId(cls, tripId):
    		return PickupLocationsModel.query.filter_by(trip_id = tripId).all()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#										#------------------------#											#
#										#     WaypointsModel     #											#
#										#------------------------#											#
#############################################################################################################

class WaypointsModel(db.Model):
    
	__tablename__ = 'waypoints'

	wp_id	 = db.Column(db.Integer, primary_key=True, autoincrement=True)
	trip_id	 = db.Column(db.Integer, ForeignKey('tripplan.trip_id'))
	waypoint = db.Column(db.String(50))
	created 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)
	updated 	 = db.Column(db.String(50), default=datetime.now(),nullable=True)

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def return_all(cls):
		return WaypointsModel.query.all()

	@classmethod
	def find_by_tripId(cls, tripId):
    		return WaypointsModel.query.filter_by(trip_id = tripId).all()

	@classmethod
	def delete_all(cls):
		try:
			num_rows_deleted = db.session.query(cls).delete()
			db.session.commit()
			return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
		except:
			return {'message': 'Something went wrong'}

#############################################################################################################
#									#------------------------#												#
#									#     UserModel          #												#
#									#------------------------#												#
#############################################################################################################

class UserModel(db.Model):
    __tablename__ = 'users'

    id 			  = db.Column(db.Integer, primary_key = True)
    username 	  = db.Column(db.String(120), unique = True, nullable = False)
    password 	  = db.Column(db.String(120), nullable = False)
    user_role	  = db.Column(db.String(10), nullable = False)
    access_token  = db.Column(db.String(120), unique = True, nullable = True, default='as' )
    refresh_token = db.Column(db.String(120), unique = True, nullable = True, default='as' )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def update_table(cls, username, access_token, refresh_token):
    	new_record = cls.query.filter_by(username = username).first()

    	new_record.access_token  = access_token
    	new_record.refresh_token = refresh_token

    	db.session.commit()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'access_token': x.access_token,
                'refresh_token': x.refresh_token,
				'user_role': x.user_role
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}
    
    @classmethod
    def all(cls):
    	return UserModel.query.all()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

#############################################################################################################
#									#------------------------#												#
#									#     RevokedTokenModel  #												#
#									#------------------------#												#
#############################################################################################################

class RevokedTokenModel(db.Model):

    __tablename__ = 'revoked_tokens'
    __table_args__ = {'extend_existing': True}
    
    id  = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

#############################################################################################################
#									#------------------------#												#
#									#        End             #												#
#									#------------------------#												#
#############################################################################################################