import uvicorn
import sqlite3
import pandas as pd
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas import AwesomeForm



app = FastAPI()
#database init
templates = Jinja2Templates(directory=".")




app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/data/{dtype}")
async def data(dtype):
    connection = sqlite3.connect("asl_img.db")
    cursor = connection.cursor()
    data = None
    if dtype == "test":
       data = cursor.execute("select * from ImageTest").fetchall()
    elif dtype == "train":
        data = cursor.execute("select * from ImageTrain").fetchall()
    else:
        raise HTTPException(status_code=404, detail="Item not found")

    df = pd.DataFrame( data, columns=["Idx", "Label", "Pics"])
    df = df[df.columns[1:]]

    
    return df.to_json()


@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @app.post('/', response_class = HTMLResponse)
# def post_form(request: Request, file: UploadFile):
    

@app.post('/ASL')
def image_to_text(request: Request, file: UploadFile):
    print(file.filename)
    print(file.content_type)
    print(file.file)
    # model 
    # predection = model
    
    pred = file.filename
    
    
    
    return {"pred": pred}


if __name__ == '__main__':
    uvicorn.run(app)
