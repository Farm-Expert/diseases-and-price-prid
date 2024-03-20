from fastapi import FastAPI
from pydantic import BaseModel
import requests
import PIL.Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyDOXBMS4S_x3rrVsrq66QfZ7zDKAiHStLE")

def read(text):
    res=""
    for chunks in text:
        chunks.text.replace('*','')
        res=res+ chunks.text
    return res

model=genai.GenerativeModel("gemini-pro")
vision=genai.GenerativeModel("gemini-pro-vision")

history=[]
chat= model.start_chat(history=history)

app=FastAPI()

def chatting(text):
    try:
        text=chat.send_message(text)
        return {"Success":read(text)}
    except:
        return {"Error": "Harmfull words found in chat"}

def viewmodel(text,img):
    try:
        res=vision.generate_content([text,img])
        res.resolve()
        return {"Success":read(res)}
    except:
        return {"Error": "Harmfull words found in chat"}
# crop name location crop price 


class Textmessage(BaseModel):
    CropName:str
    Location:str

class Viewmessage(BaseModel):
    imgurl:str
    # message:str


@app.get("/")
def home():
    return {"Kate": "Welcome to kate"}

@app.post("/priceprediction")
def chatAPI(message:Textmessage):
    prediction=message.CropName + message.Location
    message=f"I will provide you crop name and location {prediction} as input please provide the price of the crop at that location. Give some suggestive crops which have best price for that location and suggest me higer price loactions for that particular crop. provide response in json format with keys as crop name, price, location, suggested crop, locations with higher price in india"
    return chatting(message)

@app.post("/vision")
def visionAPI(view:Viewmessage):
    imgurl=view.imgurl
    print(imgurl)
    if(len(imgurl)>6 and imgurl[:6]=="https:"):
        imgurl=requests.get(imgurl)
        image_blob = imgurl.content

        with open('image.jpg', 'wb') as f:
            f.write(image_blob)
        imgurl='image.jpg'
    imgurl = PIL.Image.open(imgurl)

    message="I will provide you an image of infected plant leaf, you have to return a json with success:pass, plant name, disease name, symptoms, precautions, treatment and if image is not plant leaf then print this in a json format with key as success:fail, message: this is not a plant leaf. please provide plant leaf "
        
    # print(message)
    return viewmodel(message,imgurl)
