
import pymongo
from bson import json_util
import json
from datetime import datetime


class ProjectRepository:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.project_upload
        self.projects = self.db.projects

    def get_id(self, project_id):
        # Gets the project from id
        project = self.projects.find_one({"project_id": int(project_id)})
        project = json.loads(json_util.dumps(project))
        project["_id"] = project["_id"]["$oid"]
        return project

    def get_max_id(self):
        # Finds the last used (maximum of project ids) project_id
        cnt_doc = self.projects.count_documents({})
        if cnt_doc > 0:
            last_doc = self.projects.find().sort('project_id', pymongo.DESCENDING).limit(1)
            for record in last_doc:
                max_project_id = int(record['project_id'])
        else:
            max_project_id = 0

        return max_project_id

    def get_all(self):
        cursor = self.projects.find({})
        projects = list(cursor)
        projects = json.loads(json_util.dumps(projects))
        for item in projects:
            item["_id"] = item["_id"]["$oid"]
        return projects

    def insert(self, project):
        fields_to_insert = { 
            "project_id": project["project_id"], 
            "project_name": project["project_name"],
            "company_name": project["company_name"], 
            "creation_date": datetime.strptime(project["creation_date"], '%Y-%m-%d'), 
            "budget": project["budget"], 
            "comments": project["comments"]
        }
        inserted_project = self.projects.insert_one(fields_to_insert)
        new_id = json.loads(json_util.dumps(inserted_project.inserted_id))
        return list(new_id.values())[0]

    def update(self, project):
        # Updates project, if comment not same adds as new comment
        fields_to_change = { 
            "project_name": project["project_name"],
            "company_name": project["company_name"], 
            "creation_date": datetime.strptime(project["creation_date"], '%Y-%m-%d'), 
            "budget": project["budget"], 
            "comments": self.prepare_update_comment(project)
        }
        result = self.projects.update_one(
            filter={"project_id": int(project["project_id"])}, update={"$set": fields_to_change }
        )
        return result.modified_count

    def prepare_update_comment(self, project):
        project_id = project["project_id"]

        # Check if the comment changed, if changed add to array
        cursor = self.projects.find({"project_id" : int(project_id)})
        old_project = json.loads(json_util.dumps(list(cursor)))
        old_comments = old_project[0]["comments"]
        same_comment_exist = False
        new_comments = []
        for comment in old_comments:
            new_comments.append(comment)
            if comment == project["comments"][0]:
                same_comment_exist = True
        print(same_comment_exist)
        if not same_comment_exist:
            new_comments.append(project["comments"][0])
        else:
            new_comments = new_comments

        return new_comments


    def delete(self, project):
        result = self.projects.delete_one({"project_id": project})
        return result.deleted_count

    def get_filtered(self, query):
        cursor = self.projects.find(query)
        projects = list(json.loads(json_util.dumps(cursor)))
        for item in projects:
            item["_id"] = item["_id"]["$oid"]
        return projects
