from enum import unique
from operator import methodcaller
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow.fields import Integer, Method
from sqlalchemy.orm import backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Eragon_14368@localhost:4000/Project2021'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS:']=False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Company(db.Model): #Create table if not exists
    __tablename__ = 'Company'
    comp_id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String(30), unique=True, nullable=False)
    structure = db.relationship('Structure', backref='Company', lazy=True)

class Structure(db.Model):  
    __tablename__ = 'Structure'
    stru_id = db.Column(db.Integer, primary_key=True)
    stru_name = db.Column(db.String(25), unique=False, nullable=False)
    stru_condition = db.Column(db.Integer, nullable=False)
    stru_description = db.Column(db.String(10), nullable=False)
    stru_icon = db.Column(db.String(256), nullable=False)
    
    stru_comp_id = db.Column(db.Integer, db.ForeignKey('Company.comp_id'), nullable=False)
    zone = db.relationship('Zone', backref='Structure', lazy=True)


class Zone(db.Model):
    __tablename__ = 'Zone'
    zone_id = db.Column(db.Integer, primary_key=True)
    zone_name = db.Column(db.String(25), unique=False, nullable=False)
    zone_floor = db.Column(db.Integer, nullable=False)
    zone_time = db.Column(db.DateTime, nullable=False)
    zone_condition = db.Column(db.Integer, nullable=False) 
    zone_description = db.Column(db.String(10), nullable=False)
    zone_icon = db.Column(db.String(256), nullable=False)

    zone_bend = db.Column(db.Integer, nullable=False)           # Sublevel - data
    zone_temperature = db.Column(db.Integer, nullable=False)    # Sublevel - data

    zone_stru_id = db.Column(db.Integer, db.ForeignKey('Structure.stru_id'), nullable=False)


    

    def __init__(self, comp_name, stru_name, stru_condition, stru_description, stru_icon, stru_comp_id, zone_name, zone_floor, zone_time, zone_condition, zone_description, zone_icon, zone_color, zone_bend, zone_temperature, zone_stru_id):

        #company
        self.comp_name = comp_name

        #structure
        self.stru_name = stru_name
        self.stru_condition = stru_condition
        self.stru_description = stru_description
        self.stru_icon = stru_icon

        self.stru_comp_id = stru_comp_id

        #zone
        self.zone_name = zone_name
        self.zone_floor = zone_floor
        self.zone_time = zone_time
        self.zone_condition = zone_condition
        self.zone_description = zone_description
        self.zone_icon = zone_icon

        self.zone_bend = zone_bend                  # Sublevel - values
        self.zone_temperature = zone_temperature    # Sublevel - values

        self.zone_stru_id = zone_stru_id
        
    db.create_all()



    
#SCHEMA CONSTRUCTOR (zone)
class ZoneSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('zone_id', 'zone_name', 'zone_floor', 'zone_values', 
        'zone_condition', 'zone_icon','zone_description',
        'zone_time', 'zone_bend', 'zone_temperature')

#SCHEMA CONSTRUCTOR (Structure)
class StructureSchema(ma.Schema):
    zone = fields.Nested(ZoneSchema, many=True)
    class Meta:
        ordered = True
        fields = ('stru_id', 'stru_name', 'stru_design',
                  'stru_description', 'stru_icon', 'zone')

#CORE SCHEMA CONSTRUCTOR (company)
class CompanySchema(ma.Schema):
    structure = fields.Nested(StructureSchema, many=True)
    class Meta:
        ordered = True
        fields = ('comp_id', 'comp_name', 'structure')


#COMPANY SCHEME
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

#STRUCTURE SCHEME
structure_schema = StructureSchema()
structures_schema = StructureSchema(many=True)

    #SCHEMA Structure/design

#ZONE SCHEME
zones_schema = ZoneSchema()
zones_schema = ZoneSchema(many=True)

    #SCHEMA zone/design


    #SCHEMA zone/values


@app.route('/companies', methods=['GET'])
def get_companies():
    all_companies = Company.query.all()
    
    result_C = companies_schema.dump(all_companies)
    return jsonify(result_C)

@app.route('/companies/<comp_id>', methods=['GET'])
def get_company(comp_id):
    comp_result = Company.query.get(comp_id)
    return company_schema.jsonify(comp_result)

@app.route('/companies', methods=['POST'])
def create_company():

    name = request.json["comp_name"]

    new_company = Company(name)
    db.session.add(new_company)
    db.session.commit()

    return company_schema.jsonify(new_company)

@app.route('/companies/<comp_id>', methods=["PUT"])
def update_company(comp_id):
    company = Company.query.get(comp_id)

    comp_name = request.json['comp_name']

    company.comp_name = comp_name

    db.session.commit()
    return company_schema.jsonify(company)

@app.route('/companies/<comp_id>', methods=['DELETE'])
def delete_company(comp_id):
    company = Company.query.get(comp_id)
    db.session.delete(company)
    db.session.commit()

    return company_schema.jsonify(company)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'Welcome to our API!'})

if __name__ == "__main__":
    app.run(debug=True)
