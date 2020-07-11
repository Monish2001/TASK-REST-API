from fastapi import FastAPI
import uvicorn
import motor.motor_asyncio
import asyncio
from bson.objectid import ObjectId
import time

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["FindMind"]
collection = db["task"]

app = FastAPI()


@app.get('/api/v1/task')
async def retrieve_task():

    task_list = {}
    task_list["task"] = []
    for task in collection.find():
        task_list["task"].append(
            {"id": str(task["_id"]), "task_name": task["task_name"], "due_date": task["due"], "status": task["status"]})
    return{"task": tasks_list}


@app.get("/api/v1/task/{task_id}")
async def retrieve_task(task_id: str):

    tasks_list = {}
    tasks_list["tasks"] = []
    cursor = collection.find_one({"_id": ObjectId(task_id)})

    async for i in cursor:
        await tasks_list["tasks"].append(
            {"id": str(i["_id"]), "taskname": i["taskname"], "due": i["due"], "status": i["status"]})
    return {"task": tasks_list}


@app.post('/api/v1/task')
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
    collection.delete_one({"_id": ObjectId(task_id)})
    return{"Message": "Task is deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
