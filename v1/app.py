from flask import Flask, jsonify, request
from projectRepository import ProjectRepository
import json
from webargs.flaskparser import use_args
from webargs import fields

app = Flask(__name__)
repo = ProjectRepository()


@app.route('/project', methods=['GET'])
def get_projects():
    projects = repo.get_all()
    response = jsonify(projects)
    response.status_code = 200
    return response


@app.route('/project/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = repo.get_id(project_id)
    response = jsonify(project)
    response.status_code = 200
    return response


@app.route('/project', methods=['POST'])
def add_project():
    project_dict = json.loads(request.get_data())
    new_id = repo.get_max_id()
    project_dict['project_id'] = new_id + 1
    repo.insert(project_dict)
    response = repo.get_id(project_dict['project_id'])
    response["status_code"] = 201
    return response


@app.route('/project/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project_dict = json.loads(request.get_data())
    updated = repo.update(project_dict)
    if updated >= 1:
        response = jsonify(repo.get_id(project_id))
        response.status_code = 200
    else:
        response = jsonify({"status_code": 404})
    return response


@app.route('/project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    deleted = repo.delete(project_id)
    if deleted >= 1:
        response = jsonify({"status_code": 200})
    else:
        response = jsonify({"status_code": 404})
    return response


@app.route('/project/budget/greater/<int:budget>', methods=['GET'])
def get_greater_budget(budget):
    query = { "budget": { "$gt": budget } }
    projects = jsonify(repo.get_filtered(query))
    return projects


@app.route('/project/budget/less/<int:budget>', methods=['GET'])
def get_less_budget(budget):
    query = { "budget": { "$lt": budget } }
    projects = jsonify(repo.get_filtered(query))
    return projects


@app.route('/project/budget', methods=['GET'])
@use_args({"greater": fields.Int(required=True), "less": fields.Int(required=True)}, location="query")
def get_filtered_budget(args):
    query = { "$and": [ { "budget": { "$gt": args["greater"]}}, { "budget": { "$lt": args["less"]}} ]}
    projects = jsonify(repo.get_filtered(query))
    return projects


if __name__ == '__main__':
    app.run(debug=True)
