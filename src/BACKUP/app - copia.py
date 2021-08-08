from operator import methodcaller
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.fields import Method

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Eragon_14368@localhost:4000/Project2021'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS:']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model): #Create table if not exists
    comp_id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String(30), unique=True)

    def __init__(self, comp_name):
        self.comp_name = comp_name

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('comp_id', 'comp_name')
    
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():

    name = request.json["comp_name"]

    new_task = Task(name)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<comp_id>', methods=['GET'])
def get_task(comp_id):
    comp_result = Task.query.get(comp_id)
    return task_schema.jsonify(comp_result)

@app.route('/tasks/<comp_id>', methods=["PUT"])
def update_task(comp_id):
    task = Task.query.get(comp_id)

    comp_name = request.json['comp_name']

    task.comp_name = comp_name

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<comp_id>', methods=['DELETE'])
def delete_task(comp_id):
    task = Task.query.get(comp_id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : 'Welcome to our API!'})

if __name__ == "__main__":
    app.run(debug=True)
