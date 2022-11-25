import uvicorn
import sqlite3
import pandas as pd
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import keras
import PIL.Image as Image
from fastapi.middleware.cors import CORSMiddleware
from skimage.transform import resize
import numpy as np

alpha = "abcdefghiklmnopqrstuvwxy"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    

    

@app.post('/translate')
async def upload_file(file: UploadFile = File(...)):

    im = Image.open(file.file).convert("L")
    print(type(im))
    img = np.array(im)
    
    img = resize(img, (28, 28))
    img = img.flatten()
    model = keras.models.load_model("./asl_cnn_saved_model")
    pred = model.predict(img)
    ind = np.argmax(pred)
    return {"text", alpha[ind].upper()}


   
if __name__ == '__main__':
    uvicorn.run(app)
