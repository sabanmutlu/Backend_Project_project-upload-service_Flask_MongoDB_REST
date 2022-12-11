from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
import pymongo
from datetime import datetime
from flask_restful import Api, Resource
import json
from bson import json_util

app = Flask(__name__)
APP_URL = "http://127.0.0.1:5000"

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.project_upload
projects = db.projects

count_doc = projects.find().count()

if count_doc > 0:
    max_id_doc = projects.find().sort('project_id', pymongo.DESCENDING).limit(1)
    for record in max_id_doc:
        current_project_id = int(record['project_id'])
else:
    current_project_id = 0

all_projects = projects.find()

class Projects(Resource):

    def get(self):
        # go to the add-project page
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("add-project.html", homeIsActive=False, addProjectIsActive=True, current_id = current_project_id), 200, headers)


    def post(self):
        # get the fields data
        project_id = int(request.form['project_id'])
        project_name = request.form['project_name']
        company_name = request.form['company_name']
        creation_date = datetime.strptime(request.form['creation_date'], '%Y-%m-%d')
        budget = float(request.form['budget'])
        new_comment = request.form['comments']
        comments = [new_comment]

        # save the record to the database
        projects.insert(
            {
                "project_id": project_id,
                "project_name": project_name,
                "company_name": company_name, 
                "creation_date": creation_date, 
                "budget": budget, 
                "comments": comments
            }
        )

        # redirect to home page
        return redirect("/project")


    def put(self):
        pass


    def delete(self):
        pass


class Index(Resource):
    def get(self):
        # get the notes from the database
        all_projects = list(projects.find({}).sort("project_id",-1));

        # render a view
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("index.html",homeIsActive=True,addProjectIsActive=False,all_projects=all_projects), 200, headers)

"""

        data1 = []
        prj = projects.find().sort('project_id', pymongo.DESCENDING)
        for doc in prj:
            json_doc = json.dumps(doc, default=json_util.default)
            data1.append(json_doc)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', projects = data1, current_id = current_project_id), 200, headers)
"""

api = Api(app)
api.add_resource(Index, "/project", endpoint="index")
api.add_resource(Projects, "/add-project", endpoint="project")
api.add_resource(Projects, "/project", endpoint="add-project")
# api.add_resource(Projects, "/project/ProjectId", endpoint="project")


if __name__ == "__main__":
    app.run(debug=True)


    """
    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            id = data.get('id')
            if id:
                if projects.find_one({"id": id}):
                    return {"response": "project already exists."}
                else:
                    projects.insert(data)
            else:
                return {"response": "id number missing"}

        return redirect(url_for("index"))

    """


"""

    if request.method == 'POST':
        project_id = int(request.form['project_id'])
        project_name = request.form['project_name']
        company_name = request.form['company_name']
        creation_date = datetime.strptime(request.form['creation_date'], '%Y-%m-%d')
        budget = float(request.form['budget'])
        new_comment = request.form['comments']
        comments = [new_comment]
        projects.insert_one({
            'project_id': project_id, 
            'project_name': project_name, 
            'company_name': company_name, 
            'creation_date': creation_date, 
            'budget': budget, 
            'comments': comments
        })

        return redirect(url_for('index'))

    elif request.method=='GET':
        pass

    all_projects = projects.find()
    return render_template('index.html', projects = all_projects, current_id = current_project_id)



@app.route('/project/<project_id>', methods=(['PUT']))
def update_record(project_id):
    get_id_content = projects.find({"project_id": project_id})
    for record in get_id_content:
        old_comment = record['comments']
    project_name = request.form['project_name']
    company_name = request.form['company_name']
    creation_date = datetime.strptime(request.form['creation_date'], '%Y-%m-%d')
    budget = float(request.form['budget'])
    new_comment = request.form['comments']
    comments = old_comment.
    projects.insert_one({
        'project_id': project_id, 
        'project_name': project_name, 
        'company_name': company_name, 
        'creation_date': creation_date, 
        'budget': budget, 
        'comments': comments
    })

    return redirect(url_for('index'))

"""