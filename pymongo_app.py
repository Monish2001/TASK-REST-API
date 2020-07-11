from fastapi import FastAPI
import pymongo
import uvicorn
from bson.objectid import ObjectId

mongo = pymongo.MongoClient(
    host='localhost',
    port=27017,
    serverSelectionTimeoutMS=1000
)
db = mongo["intern"]
collection = db["tasks"]

app = FastAPI()


@app.get("/api/v1/task")
async def retrieve_task():
    task_list = {}
    task_list["task"] = []
    for task in collection.find():
        task_list["task"].append(
            {"id": str(task["_id"]), "task_name": task["task_name"], "due_date": task["due_date"], "status": task["status"]})
    return task_list


@app.get("/api/v1/task/{task_id}")
async def read_task(task_id: str):
    task_list = {}
    task_list["task"] = []
    for task in collection.find({"_id": ObjectId(task_id)}):
        task_list["task"].append(
            {"id": str(task["_id"]), "task_name": task["task_name"], "due_date": task["due_date"], "status": task["status"]})
    return{"task": task_list}


@app.post("/api/v1/task")
async def add_new_task(task, due_date):
    if task and due_date:
        mydict = {"task_name": task, "due_date": due_date, "status": "Active"}
        dbResponse = collection.insert_one(mydict)
        return{"Message": "Task added successfully"}

    return{"Message": "Task is not added"}


@app.put("/api/v1/task/{task_id}")
async def update_task(task_id: str, task, due_date, status):
    collection.update_one({"_id": ObjectId(task_id)}, {"$set": {
        "task_name": task, "due_date": due_date, "status": status}})
    return{"Message": "Updated Successfully"}


@app.delete("/api/v1/task/{task_id}")
async def delete_task(task_id: str):
    collection.remove({"_id": ObjectId(task_id)})
    return{"Message": "Task is deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
