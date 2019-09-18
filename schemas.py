from marshmallow import Schema, fields

class PassengerSchema(Schema):
        ps_id           = fields.Number()
        ps_token_id     = fields.Str()
        passenger_name  = fields.Str()
        passenger_email = fields.Str()
        prof_pic        = fields.Str()
        is_ontrip       = fields.Str()
        created         = fields.Str()
        updated         = fields.Str()

class OwnerSchema(Schema):
    ow_id        = fields.Number()
    ow_token_id  = fields.Str()
    owner_name   = fields.Str()
    owner_nic    = fields.Str()
    owner_email  = fields.Str()
    contact_num  = fields.Number()
    address      = fields.Str()
    area         = fields.Str()
    service_type = fields.Str()
    company_name = fields.Str()
    prof_pic     = fields.Str()
    created      = fields.Str()
    updated      = fields.Str()

class DriverSchema(Schema):
    dr_id       = fields.Number()
    dr_token_id = fields.Str()
    driver_name = fields.Str()
    driver_email= fields.Email()
    owner_id    = fields.Number()
    license     = fields.Str()
    driver_nic  = fields.Str()
    prof_pic    = fields.Str()
    contact_num = fields.Number()
    is_ontrip   = fields.Bool()
    created      = fields.Str()
    updated      = fields.Str()

class VehicleSchema(Schema):
    v_id               = fields.Number()
    vehicle_reg_number = fields.Str()
    owner_id           = fields.Number()
    driver_id          = fields.Number()
    ac_condition       = fields.Bool()
    vehicle_brand      = fields.Str()
    vehicle_type       = fields.Str()
    no_of_passengers   = fields.Number()
    insurance_data     = fields.Str()
    is_ontrip          = fields.Bool()
    created      = fields.Str()
    updated      = fields.Str()

class TripPlanSchema(Schema):
    trip_id          = fields.Number()
    vehicle_type     = fields.Str()
    no_of_passengers = fields.Number()
    date_from        = fields.Str()
    date_to          = fields.Str()
    pickup_loc   = fields.Str()
    ac_condition     = fields.Bool()
    destination      = fields.Str()
    passenger_id     = fields.Number()
    description      = fields.Str()
    created      = fields.Str()
    updated      = fields.Str()

class TripStatusSchema(Schema):
    ts_id                   = fields.Number()
    trip_id                 = fields.Number()
    trip_budget             = fields.Float()
    assigned_driver         = fields.Number()
    is_confirmed_passenger  = fields.Bool()
    is_confirmed_driver     = fields.Bool()
    trip_started            = fields.Bool()
    trip_finished           = fields.Bool()
    vehicle_no              = fields.Number()
    created      = fields.Str()
    updated      = fields.Str()

class PickupLocationSchema(Schema):
    pl_id           = fields.Number()
    trip_id         = fields.Number()
    pickup_loc  = fields.Str()
    created      = fields.Str()
    updated      = fields.Str()

class WaypointsSchema(Schema):
    wp_id    = fields.Number()
    trip_id  = fields.Number()
    waypoint = fields.Str()
    created      = fields.Str()
    updated      = fields.Str()

class UserSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    user_role = fields.Str()
    access_token = fields.Str()
    refresh_token = fields.Str()

class DriverFeedbackSchema(Schema):
    fdb_id      = fields.Number()
    driver_id   = fields.Number()
    feedback    = fields.Str()
    created      = fields.Str()
    updated      = fields.Str()
    
class PassengerFeedbackSchema(Schema):
    fdb_id       = fields.Number()
    passenger_id = fields.Number()
    feedback     = fields.Str()
    created      = fields.Str()
    updated      = fields.Str()
