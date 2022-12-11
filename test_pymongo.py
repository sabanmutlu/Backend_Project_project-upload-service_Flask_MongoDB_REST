import json
import pymongo
from bson import json_util
# from flask import Flask, jsonify, request

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.project_upload
projects = db.projects

cursor = projects.find({"project_id" : 18})

# Check if the comment changed, if changed add to array
old_project = json.loads(json_util.dumps(list(cursor)))
old_comments = old_project[0]["comments"]
new_comment = "Test 18 2"
same_comment_exist = False
new_comments = []
for comment in old_comments:
    new_comments.append(comment)
    if comment == new_comment:
        same_comment_exist = True
print(same_comment_exist)
if not same_comment_exist:
    new_comments.append(new_comment)
else:
    new_comments = new_comments
print(new_comments)

"""

cursor = projects.find(json_util.loads(query))
projects = list(cursor)
projects = json_util.loads(json_util.dumps(projects))


for item in projects:
    print(item["_id"])
    item["_id"] = item["_id"]["$oid"]


get_id_content = projects.find({"project_id": 14})
for x in get_id_content:
    old_comment = x['comments']

all_data = projects.find().sort('project_id', pymongo.DESCENDING)
for x in all_data:
    print("ids: ", x["_id"])

projectFormId = '6317cf5a5fb772b8a8eae811'

tst = projects.find_one({"_id":bson.ObjectId(projectFormId)})
print("tst: ", tst)

# result = projects.delete_one({'project_id': 1})

query = { "budget": { "$gt": 900 } }
cnt_result = projects.count_documents(query)
result = projects.find(query)
print("res_cnt: ", cnt_result)

for rec in result:
    print("records: ", rec)


# Finds the last used (maximum of project ids) project_id
cnt_doc = projects.count_documents({})
if cnt_doc > 0:
    last_doc = projects.find().sort('project_id', pymongo.DESCENDING).limit(1)
    for record in last_doc:
        max_project_id = int(record['project_id'])
else:
    max_project_id = 0

print("max_prj", max_project_id)


current_id_doc = projects.find({ "project_id": 1 }).limit(1)
for record in current_id_doc:
    print(record)


comment = []
if check_id > 0:
    comment = comment.append('ttttt')
else:
    comment = ['YYY']
print(comment)
"""