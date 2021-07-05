from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)


todos = {
            "Task1":{
                "_id":1,
                "Task": "Analysing the requirement",
                "Summary": "Before starting the execution need to analyse the requirement firstly"
            },
            "Task2":{
                "_id":2,
                "Task":"Research",
                "Summary":"Research about the technologies which we need to implement in the project"
            },
            "Task3":{
                "_id":3,
                "Task":"development",
                "Summary":"Start developing the project"
            },
            "Task4":{
                "_id":4,
                "Task":"Testing",
                "Summary":"Testing the developed project"
            },
            "Task5":{
                "_id":5,
                "Task":"Deployment",
                "Summary":"Deploying the developed project into production"
            }

        }

task_get_args = reqparse.RequestParser()
task_get_args.add_argument("task_id", required=False)

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task_id", required=True, type=str, help="task id is needed")
task_post_args.add_argument("id", required=True, type=int, help="id is needed")
task_post_args.add_argument("task_name", required=True, type=str, help="task name is needed")
task_post_args.add_argument("summary", required=True, type=str, help="summary is needed")

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task_id", required=True, type=str, help="task id is needed")
task_put_args.add_argument("task_name", required=False)
task_put_args.add_argument("summary", required=False)

task_delete_args = reqparse.RequestParser()
task_delete_args.add_argument("task_id", required=True, type=str, help="task id is needed")

class TODO(Resource):
    def get(self):
        args = task_get_args.parse_args()
        _id = args["task_id"]
        if args["task_id"] in todos:
            return jsonify({"success":True, "result":todos[_id]})
        return jsonify({"success":True, "result":todos})

    def post(self):
        args = task_post_args.parse_args()
        if args["task_id"] in todos:
            abort(409, message="Task name already exists")
        else:
            task_id = args["task_id"]
            _id = args["id"]
            task = args["task_name"]
            summary = args["summary"]
            todos[task_id] = {"_id":_id, "Task":task, "Summary":summary}
        return todos

    def put(self):
        args = task_put_args.parse_args()
        if args["task_id"] not in todos:
            abort(409, message="Task id doesnt exists")

        task_id = args["task_id"]
        if "task_name" in args:
            if args["task_name"] != None:
                todos[task_id]["Task"] = args["task_name"]
        if "summary" in args:
            if args["summary"] != None:
                todos[task_id]["Summary"] = args["summary"]
        return todos

    def delete(self):
        args = task_delete_args.parse_args()
        task_id =  args["task_id"]
        if task_id not in todos:
            abort(409, message="task_id is missing")
        del todos[task_id]
        return todos

api.add_resource(TODO, "/todos")

if __name__ == "__main__":
    app.run(debug=True)
