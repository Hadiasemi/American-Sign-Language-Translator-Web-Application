import uvicorn
from fastapi import FastAPI
import sqlite3
import pandas as pd



app = FastAPI()
#database init



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/data/{dtype}")
async def data(dtype):
    connection = sqlite3.connect("test3.db")
    cursor = connection.cursor()
    data = None
    if dtype == "test":
       data = cursor.execute("select * from ImageTest").fetchall()
    else:
        data = cursor.execute("select * from ImageTrain").fetchall()

    df = pd.DataFrame( data, columns=["Idx", "Label", "Pics"])
    df = df[df.columns[1:]]

    
    return df.to_json()


# @app.get("/data")
# async def data():
#     connection = sqlite3.connect("test3.db")
#     cursor = connection.cursor()
#     data = None

#     data = cursor.execute("select * from Image").fetchall()
#     # print(data)


#     df = pd.DataFrame( data, columns=["Idx", "Label", "Pics"])
#     df = df[df.columns[1:]]
#     # print(df)
    
#     return df.to_json()




# @app.get("/")

"""
    1. ML to DB -> get{data[training]} -> SELECT * from DB
    1. ML to DB -> get{data[testting]} -> SELECT * from DB
"""