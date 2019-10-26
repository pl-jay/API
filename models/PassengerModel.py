from datetime import datetime
from run import db
from sqlalchemy.orm import relationship, load_only
from sqlalchemy import Column, Integer, ForeignKey
from flask import jsonify
from passlib.hash import pbkdf2_sha256 as sha256

#############################################################################################################
#										#----------------#													#
#										# Passenger Model#												    #
#										#----------------#													#
#############################################################################################################
#region Passenger Model
class PassengerModel(db.Model):
	
	__tablename__ = 'passenger'
	__table_args__ = {'extend_existing': True}

	ps_id 		   = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ps_token_id    = db.Column(db.String(120),unique=True, nullable=True)
	passenger_name = db.Column(db.String(50), nullable=False)
	passenger_email= db.Column(db.String(120), nullable=False)
	prof_pic 	   = db.Column(db.String(120), nullable=True)
	is_ontrip 	   = db.Column(db.Boolean, default=False)
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

	@classmethod
	def get_passengerId(cls, username):
		return cls.query.filter_by(passenger_email = username).all()[0].ps_id

	@classmethod
	def update_token(cls,psId,token):
		if cls.query.filter_by(ps_id = psId).scalar() is not None:
			new_record = cls.query.filter_by(ps_id = psId).first()
			new_record.ps_token_id = token
			db.session.commit()
			return True
		else:
			return False
#endregion
