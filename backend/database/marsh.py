from marshmallow import Schema, fields

class add_company(Schema):
    company_name = fields.String(required = True)
    country= fields.String(required = True)
    state= fields.String(required = True)
    city= fields.String(required = True)
    pincode= fields.String(required = True)
    department= fields.String(required = True)
    branch= fields.String(required = True)
    address= fields.String(required = True)