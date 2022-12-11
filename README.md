# Project Upload Service

Develop a project upload service in Python (e.g. using flask) which creates, updates and retrieves project entries in a local MongoDB instance.

A project entry shall contain the following information:
- ProjectId: number -> unique individual id of a project
- ProjectName: string
- CompanyName: string
- CreationDate: date
- Budget: number
- Comments: string[] -> array of string for multiple Comments

The service shall store all project entries in the collection projects in the MongoDB.
The API should have the following API endpoints (API receives and sends JSON):
- POST /project -> Creates new project or updates existing one
- PUT /project/{ProjectId} -> Updates existing project or creates new one
- GET /project -> Get all projects as array
- GET /project/{ProjectId} -> Get project by ProjectId
- DELETE /project/{ProjectId} -> Delete project by ProjectId
- GET /project/budget/greater/{Budget} -> Get all projects as array with budget greater than Budget
- GET /project/budget/less/{Budget} -> Get all projects as array with budget less than Budget
- POST /project/budget -> Receives Filter object {"greater": number, "less": number} and returns all projects as array with budget greather than "greater" and budget less than "less"
