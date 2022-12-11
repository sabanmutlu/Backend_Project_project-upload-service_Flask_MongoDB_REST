
from distutils.filelist import findall
import json
from urllib import response
from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
import pymongo
from datetime import datetime
from flask_restful import Api, Resource
from bson import json_util, ObjectId

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.project_upload
projects = db.projects

count_doc = projects.count_documents({})
all_projects = projects.find({})

if count_doc > 0:
    max_id_doc = projects.find().sort('project_id', pymongo.DESCENDING).limit(1)
    for record in max_id_doc:
        current_project_id = int(record['project_id'])
else:
    current_project_id = 0


class Project(Resource):
    # Add, see, edit, delete the project
    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get(self, project_id=None, budget=None):
        if project_id:
            # direct to edit project page
            prj = projects.find_one({"project_id": int(project_id)})
            return make_response(
                render_template('edit-project.html', homeIsActive=False, project=prj), 
                200, 
                self.headers
            )
        
        elif request.args.get('form'):
                        
            # get the _id of the project to edit
            projectFormId = request.args.get('form')

            # get the project details from the db
            prj = projects.find_one({"_id":ObjectId(projectFormId)})
            
            # direct to edit project page
            return make_response(
                render_template('edit-project.html', homeIsActive=False, project=prj), 
                200, 
                self.headers
            )
            
        else:
            # go to the add-project page
            return make_response(
                render_template("add-project.html", homeIsActive=False, addProjectIsActive=True, current_id = current_project_id), 
                200, 
                self.headers
            )


    def post(self, project_id=None):
        if request.endpoint == "budget":
            pass
        else:
                
            # get the fields data
            project_id = int(request.form['project_id'])
            project_name = request.form['project_name']
            company_name = request.form['company_name']
            creation_date = datetime.strptime(request.form['creation_date'], '%Y-%m-%d')
            budget = float(request.form['budget'])
            new_comment = request.form['comments']
            
            if project_id:
                # save the record to the database
                comments = []
                comments.append(new_comment)
                projects.update_one( {"project_id": project_id}, 
                    { 
                        "$set" : {
                        "project_id": project_id,
                        "project_name": project_name,
                        "company_name": company_name, 
                        "creation_date": creation_date, 
                        "budget": budget, 
                        "comments": comments
                        }
                    }
                )

                # redirect to home page
                return redirect("/project")
            else:

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


    def delete(self, project_id):
        # delete from the database
        projects.delete_one({ 'project_id': int(project_id) })

        # redirect to home page
        return make_response(
            render_template("index.html", homeIsActive=True, addProjectIsActive=True, projects=all_projects), 
            200, 
            self.headers
        )


class Projects(Resource):

    def __init__(self):
        self.headers = {'Content-Type': 'text/html'}

    def get(self, budget=None):
        if budget == None:
            # get the projects from the database
            all_projects = list(projects.find({}).sort("project_id",-1))

            # render home page for all projects
            return make_response(
                render_template("index.html", homeIsActive=True, addProjectIsActive=False, projects=all_projects), 
                200, 
                self.headers
            )
        
        else :
            
            if request.endpoint == "greater":
                query = { "budget": { "$gt": int(budget) } }
                result = projects.find(query)
                return make_response(
                    render_template('index.html', homeIsActive=False, projects=result), 
                    200, 
                    self.headers
                )
            elif request.endpoint == "less":
                query = { "budget": { "$lt": int(budget) } }
                result = projects.find(query)
                return make_response(
                    render_template('index.html', homeIsActive=False, projects=result), 
                    200, 
                    self.headers
                )
            else:
                pass
                # go to the result page
    def post(self):
        budget_min = request.form['budgetMin']
        budget_max = request.form['budgetMax']
        query = {"budget": {"$gt": int(budget_min)}, "budget": {"$lt": int(budget_max)}}
        result = projects.find(query)
        return make_response(
            render_template('index.html', homeIsActive=False, projects=result), 
            200, 
            self.headers
        )


api = Api(app)
api.add_resource(Projects, "/project", endpoint="index")
api.add_resource(Projects, "/project/budget/greater/<budget>", endpoint="greater")
api.add_resource(Projects, "/project/budget/less/<budget>", endpoint="less")
api.add_resource(Projects, "/project/budget", endpoint="budget")
api.add_resource(Project, "/project/add", endpoint="add")
api.add_resource(Project, "/project/<project_id>", endpoint="edit")
api.add_resource(Project, "/project/<project_id>", endpoint="delete")
api.add_resource(Project, "/project/<project_id>", endpoint="view")


if __name__ == "__main__":
    app.run(debug=True)


"""

        data1 = []
        prj = projects.find().sort('project_id', pymongo.DESCENDING)
        for doc in prj:
            json_doc = json.dumps(doc, default=json_util.default)
            data1.append(json_doc)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', projects = data1, current_id = current_project_id), 200, headers)


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