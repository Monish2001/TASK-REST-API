from fastapi import FastAPI
import uvicorn
import motor.motor_asyncio
import asyncio
from bson.objectid import ObjectId


DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["FindMind"]
collection = db["task"]

app = FastAPI()


#Viewing the complete task list
@app.get('/api/v1/task')
async def retrieve_task():

    task_list = {}
    task_list["task"] = []
    for task in collection.find():
        task_list["task"].append(
            {"id": str(task["_id"]), "task_name": task["task_name"], "due_date": task["due_date"], "status": task["status"]})
    return{"task": task_list}


#View a particular task with task_id
@app.get("/api/v1/task/{task_id}")
async def retrieve_task(task_id: str):

    task_list = {}
    task_list["task"] = []
    cursor = collection.find_one({"_id": ObjectId(task_id)})

    async for i in cursor:
        await task_list["task"].append(
            {"id": str(i["_id"]), "task_name": i["task_name"], "due_date": i["due_date"], "status": i["status"]})
    return {"task": task_list}


#Add a task
@app.post('/api/v1/task')
async def add_new_task(task, due_date):

    if task and due_date:
        mydict = {"task_name": task, "due_date": due_date, "status": "Active"}
        dbResponse = collection.insert_one(mydict)
        return{"Message": "Task added successfully"}

    return{"Message": "Task is not added"}


#Update a task with task_id
@app.put("/api/v1/task/{task_id}")
async def update_task(task_id: str, task, due_date, status):

    collection.update_one({"_id": ObjectId(task_id)}, {"$set": {
        "task_name": task, "due_date": due_date, "status": status}})
    return{"Message": "Updated Successfully"}


#Delete a task with task_id
@app.delete("/api/v1/task/{task_id}")
async def delete_task(task_id: str):
    collection.delete_one({"_id": ObjectId(task_id)})
    return{"Message": "Task is deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
